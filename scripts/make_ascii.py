"""Turn a portrait photo into ASCII art.

Usage: python3 scripts/make_ascii.py PHOTO COLS ROWS LOCAL_CONTRAST GAMMA [--invert] > out.txt
Used for the profile card:  PHOTO 58 36 2.5 1.1  (dark)  and the same with --invert (light).
The silhouette polygon is hand-traced for Santiago's photo (DSC_0248.png, square crop).
Needs Pillow + numpy.
"""
import sys, numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw
src, cols, rows = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
LC, GAM = float(sys.argv[4]), float(sys.argv[5])
im = Image.open(src).convert('RGB').resize((700,700), Image.LANCZOS)
sil = [(330,42),(420,55),(480,90),(515,150),(525,215),(530,280),(522,350),(510,420),(495,480),
       (470,540),(480,560),(540,600),(560,660),(140,660),(95,575),(170,545),(215,500),(200,420),
       (175,395),(152,330),(150,290),(170,275),(168,200),(185,140),(230,90),(280,55)]
m = Image.new('L', im.size, 0); ImageDraw.Draw(m).polygon(sil, fill=255)
m = m.filter(ImageFilter.GaussianBlur(4))
box = (125, 30, 575, 655)
g = np.asarray(ImageOps.grayscale(im).crop(box), dtype=float)/255
mk = np.asarray(m.crop(box), dtype=float)/255
blur = np.asarray(Image.fromarray((g*255).astype('uint8')).filter(ImageFilter.GaussianBlur(25)), float)/255
v = g + LC*(g - blur)           # local contrast boost
inside = mk > 0.5
lo, hi = np.percentile(v[inside], [2, 98])
v = np.clip((v-lo)/(hi-lo), 0, 1) ** GAM
INVERT = '--invert' in sys.argv
v = ((1 - v) if INVERT else v) * mk
img = Image.fromarray((v*255).astype('uint8')).resize((cols, rows), Image.BOX)
ramp = " .`',:;~-+=*!|ijlrxkK%$mH#M&8B@"
a = np.asarray(img)
for y in range(rows):
    print(''.join(ramp[min(len(ramp)-1, int(a[y,x])*len(ramp)//256)] for x in range(cols)).rstrip())
