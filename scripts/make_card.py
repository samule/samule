"""Build the neofetch-style profile card SVGs (dark + light) from the ASCII portrait.

Usage: python3 scripts/make_card.py
Reads assets/portrait-{dark,light}.txt, writes assets/card-{dark,light}.svg.
Edit the INFO list below to change the text on the right-hand side.
Standard library only.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIDTH = 60  # characters in the right-hand column

# (key, value) rows. A str is a section header, None is a blank spacer line.
INFO = [
    "santiago@mule",
    ("OS", "Buenos Aires, Argentina (UTC-3)"),
    ("Uptime", "10+ years shipping projects"),
    ("Host", "Gappify, Lead Project Manager"),
    ("Kernel", "Project & Program Management"),
    ("Shell", "AI-enabled operator, builder after hours"),
    ("IDE", "Claude Code, Cursor, VS Code"),
    None,
    ("Languages.Spoken", "Spanish, English"),
    ("Languages.Code", "JavaScript, HTML/CSS, SQL, Python"),
    ("Stack.Favorite", "n8n, Postgres, React + Vite, three.js"),
    ("Hobbies.Hardware", "3D printing, ESP32 tinkering"),
    ("Hobbies.Other", "F1 data, puzzle games"),
    None,
    "Experience",
    ("Gappify", "Lead Project Manager, 2022-now"),
    ("Cognizant", "Program Mgmt Manager, Google Cloud"),
    ("Banco Provincia", "Business Planning & Control"),
    ("Accenture", "PMO Lead, TechStar Award"),
    None,
    "Contact",
    ("LinkedIn", "in/santiagomule"),
    ("Web", "samule.github.io"),
]

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", text="#c9d1d9", key="#ffa657",
                 value="#a5d6ff", dots="#616e7f", ascii="#c9d1d9"),
    "light": dict(bg="#f6f8fa", border="#d0d7de", text="#24292f", key="#953800",
                  value="#0a3069", dots="#c2cfde", ascii="#24292f"),
}

FONT = 15
LINE = 19
CHAR = FONT * 0.6  # monospace advance width (approximate)
PAD = 18


def info_line(item):
    """Return a list of (text, role) segments for one right-hand row."""
    if item is None:
        return [("", "text")]
    if isinstance(item, str):
        head = f"- {item} " if item != INFO[0] else f"{item} "
        return [(head, "text"), ("-" * max(3, WIDTH - len(head)), "dots")]
    key, value = item
    dots = WIDTH - len(key) - len(value) - 5
    return [(". ", "text"), (key, "key"), (": ", "text"),
            ("." * max(1, dots), "dots"), (" " + value, "value")]


def build(theme):
    c = THEMES[theme]
    art = (ROOT / f"assets/portrait-{theme}.txt").read_text().rstrip("\n").split("\n")
    art_cols = max(len(l) for l in art)
    rows = max(len(art), len(INFO))
    x_info = PAD + (art_cols + 3) * CHAR
    width = int(x_info + WIDTH * CHAR + PAD * 2)
    height = int(PAD * 2 + rows * LINE)
    art_top = PAD + LINE + (rows - len(art)) * LINE // 2
    info_top = PAD + LINE + (rows - len(INFO)) * LINE // 2

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ConsolasFallback,Consolas,Menlo,'
        f'\'DejaVu Sans Mono\',\'Courier New\',monospace" font-size="{FONT}px">',
        f"<style>.k{{fill:{c['key']}}}.v{{fill:{c['value']}}}.d{{fill:{c['dots']}}}"
        f"text,tspan{{white-space:pre}}</style>",
        f'<rect width="{width}" height="{height}" rx="12" fill="{c["bg"]}" '
        f'stroke="{c["border"]}"/>',
        f'<text x="{PAD}" y="{art_top}" fill="{c["ascii"]}" xml:space="preserve">',
    ]
    for i, line in enumerate(art):
        out.append(f'<tspan x="{PAD}" dy="{0 if i == 0 else LINE}">{escape(line)}</tspan>')
    out.append("</text>")
    out.append(f'<text x="{x_info:.0f}" y="{info_top}" fill="{c["text"]}" xml:space="preserve">')
    cls = {"key": "k", "value": "v", "dots": "d"}
    for i, item in enumerate(INFO):
        segs = "".join(
            f'<tspan class="{cls[r]}">{escape(t)}</tspan>' if r in cls else escape(t)
            for t, r in info_line(item)
        )
        out.append(f'<tspan x="{x_info:.0f}" dy="{0 if i == 0 else LINE}">{segs or " "}</tspan>')
    out.append("</text></svg>")
    (ROOT / f"assets/card-{theme}.svg").write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    for t in THEMES:
        build(t)
    print("wrote assets/card-dark.svg, assets/card-light.svg")
