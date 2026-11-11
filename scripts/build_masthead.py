"""Generate assets/masthead-{light,dark}.svg.

Type is converted to outlines so the masthead renders identically
everywhere: GitHub serves README images through <img>, which cannot load
web fonts. The variable fonts (OFL, from github.com/google/fonts, under
ofl/geist and ofl/geistmono) are read from the directory given as the
first argument:

    Geist[wght].ttf, GeistMono[wght].ttf

    pip install fonttools uharfbuzz
    python scripts/build_masthead.py ~/fonts
"""

import sys
from io import BytesIO
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = Path(sys.argv[1]).expanduser()
OUT = Path(__file__).resolve().parent.parent / "assets"

W, H = 900, 190

THEMES = {
    # GitHub's own foreground tokens; the name fades from ink into the accent
    # and on to a violet, over a faint glow of the accent.
    "light": {"ink": "#1f2328", "muted": "#59636e", "accent": "#2b45ff", "violet": "#9b5cff", "glow": 0.14},
    "dark": {"ink": "#f0f6fc", "muted": "#9198a1", "accent": "#7c8cff", "violet": "#c08cff", "glow": 0.22},
}


class Face:
    def __init__(self, filename, weight):
        tt = TTFont(FONTS / filename)
        instantiateVariableFont(tt, {"wght": weight}, inplace=True)
        buf = BytesIO()
        tt.save(buf)
        self.tt = TTFont(BytesIO(buf.getvalue()))
        self.glyphs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(hb.Blob(buf.getvalue())))

    def run(self, text, size, tracking=0.0):
        """Shaped outline for `text`; returns (path data, advance width)."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        scale = size / self.upem
        order = self.tt.getGlyphOrder()
        pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        x = 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = order[info.codepoint]
            t = TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale))
            self.glyphs[name].draw(t)
            x += pos.x_advance * scale + tracking
        return pen.getCommands(), x - tracking


sans = Face("Geist[wght].ttf", 600)
mono = Face("GeistMono[wght].ttf", 400)

name_d, name_w = sans.run("Harthik Mallichetty", 88, tracking=-3.6)
# Mono subline, large enough to stay legible when GitHub scales the image to a phone.
LABELS = ("DATA & AI ENGINEER", "DALLAS, TX", "BUILDING ROOM")
labels = [mono.run(t, 19, tracking=2.4) for t in LABELS]
GAP = 30


def render(theme):
    c = THEMES[theme]
    x, sub, dots = 2.0, [], []
    for i, (d, w) in enumerate(labels):
        if i:
            dots.append(f'<circle cx="{x - GAP / 2:.1f}" cy="161" r="2.6"/>')
        sub.append(f'<path transform="translate({x:.1f} 168)" d="{d}"/>')
        x += w + GAP
    # Gradients and the glow use plain gradients rather than filters, which
    # some renderers clip to a hard-edged box.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Harthik Mallichetty — Data and AI engineer, Dallas, Texas. Building Room.">
<defs>
<linearGradient id="name" x1="0" x2="{name_w:.0f}" gradientUnits="userSpaceOnUse">
<stop offset=".35" stop-color="{c['ink']}"/><stop offset=".78" stop-color="{c['accent']}"/><stop offset="1" stop-color="{c['violet']}"/>
</linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{c['accent']}" stop-opacity="{c['glow']}"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></radialGradient>
</defs>
<ellipse cx="660" cy="70" rx="240" ry="80" fill="url(#glow)"/>
<path fill="url(#name)" transform="translate(-2 100)" d="{name_d}"/>
<g fill="{c['muted']}">{"".join(sub)}</g>
<g fill="{c['accent']}">{"".join(dots)}</g>
</svg>
"""


OUT.mkdir(exist_ok=True)
for theme in THEMES:
    (OUT / f"masthead-{theme}.svg").write_text(render(theme))
print(f"name width {name_w:.0f}px of {W}")
