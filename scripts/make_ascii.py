"""Turn Santiago's portrait photo into dithered ASCII art for the profile card.

Usage:
  python3 scripts/make_ascii.py PHOTO > assets/portrait-dark.txt
  python3 scripts/make_ascii.py PHOTO --light > assets/portrait-light.txt

How it works: mask the head with a hand-traced silhouette, mix global brightness with
local-contrast-normalised detail (so the bright forehead doesn't become one flat block),
then Floyd-Steinberg dither onto a short ramp. Dithering with few characters leaves real
gaps between them, which keeps the portrait crisp instead of fuzzy.
The silhouette polygon is traced for DSC_0248.png (square crop); a new photo needs a new one.
Needs Pillow + numpy.
"""
import argparse
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument('photo')
ap.add_argument('--cols', type=int, default=84)
ap.add_argument('--box', default='140,35,560,640', help='crop in 700px-preview coords')
ap.add_argument('--mix', type=float, default=0.4, help='weight of local-contrast detail')
ap.add_argument('--rad', type=float, default=0.05, help='local window, fraction of width')
ap.add_argument('--gamma', type=float, help='tone gamma (default 1.3 dark, 1.0 light)')
ap.add_argument('--ramp', default=' .:+*#@')
ap.add_argument('--light', action='store_true', help='ink on light background')
ap.add_argument('--inkgamma', type=float, default=1.8, help='light only: thins the ink')
a = ap.parse_args()
gamma = a.gamma if a.gamma is not None else (1.0 if a.light else 1.3)

photo = Image.open(a.photo).convert('RGB')
S = photo.width / 700
sil = [(330, 42), (420, 55), (480, 90), (515, 150), (525, 215), (530, 280), (522, 350),
       (510, 420), (495, 480), (470, 540), (480, 560), (540, 600), (560, 660), (140, 660),
       (95, 575), (170, 545), (215, 500), (200, 420), (175, 395), (152, 330), (150, 290),
       (170, 275), (168, 200), (185, 140), (230, 90), (280, 55)]
m = Image.new('L', photo.size, 0)
ImageDraw.Draw(m).polygon([(x * S, y * S) for x, y in sil], fill=255)
box = [int(int(v) * S) for v in a.box.split(',')]
rows = round(a.cols * (box[3] - box[1]) / (box[2] - box[0]) * 0.5)  # chars are ~2x tall
W, H = a.cols * 6, rows * 12

g = np.asarray(ImageOps.grayscale(photo.crop(box)).resize((W, H), Image.LANCZOS), float) / 255
mk = np.asarray(m.crop(box).resize((W, H)).filter(ImageFilter.GaussianBlur(W / 150)), float) / 255


def blur(x, r):
    return np.asarray(Image.fromarray(np.uint8(np.clip(x, 0, 1) * 255))
                      .filter(ImageFilter.GaussianBlur(r)), float) / 255


r = W * a.rad
mean = blur(g, r)
var = blur((g - mean) ** 2 * 4, r) / 4
local = 1 / (1 + np.exp(-1.2 * (g - mean) / (np.sqrt(var) + 0.04)))
inside = mk > .5
lo, hi = np.percentile(g[inside], [1, 99])
v = (1 - a.mix) * np.clip((g - lo) / (hi - lo), 0, 1) + a.mix * local
lo, hi = np.percentile(v[inside], [1, 99.5])
v = np.clip((v - lo) / (hi - lo), 0, 1) ** gamma
v = ((1 - v) ** a.inkgamma if a.light else v) * mk

img = np.asarray(Image.fromarray(np.uint8(v * 255)).resize((a.cols, rows), Image.BOX), float) / 255
R, n = a.ramp, len(a.ramp) - 1
for y in range(rows):  # Floyd-Steinberg error diffusion onto the ramp
    line = ''
    for x in range(a.cols):
        q = min(n, max(0, int(round(img[y, x] * n))))
        line += R[q]
        err = img[y, x] - q / n
        if x + 1 < a.cols:
            img[y, x + 1] += err * 7 / 16
        if y + 1 < rows:
            if x > 0:
                img[y + 1, x - 1] += err * 3 / 16
            img[y + 1, x] += err * 5 / 16
            if x + 1 < a.cols:
                img[y + 1, x + 1] += err / 16
    print(line.rstrip())
