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

W, H = 900, 160

THEMES = {
    # GitHub's own foreground and border tokens, so the type sits in the page.
    "light": {"ink": "#1f2328", "muted": "#59636e", "rule": "#d1d9e0", "accent": "#2b45ff"},
    "dark": {"ink": "#f0f6fc", "muted": "#9198a1", "rule": "#3d444d", "accent": "#7c8cff"},
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

role_d, _ = mono.run("DATA & AI ENGINEER", 17, tracking=2.4)
city_d, city_w = mono.run("DALLAS, TX", 17, tracking=2.4)
name_d, name_w = sans.run("Harthik Mallichetty", 82, tracking=-3.2)
stop_d, _ = sans.run(".", 82)


def render(theme):
    c = THEMES[theme]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Harthik Mallichetty — Data and AI engineer, Dallas, Texas">
<g fill="{c['muted']}">
<path transform="translate(2 28)" d="{role_d}"/>
<path transform="translate({W - 2 - city_w:.1f} 28)" d="{city_d}"/>
</g>
<path fill="{c['ink']}" transform="translate(-2 114)" d="{name_d}"/>
<path fill="{c['accent']}" transform="translate({name_w - 1:.1f} 114)" d="{stop_d}"/>
<path d="M1 150.5H{W - 1}" stroke="{c['rule']}" stroke-width="1.5"/>
</svg>
"""


OUT.mkdir(exist_ok=True)
for theme in THEMES:
    (OUT / f"masthead-{theme}.svg").write_text(render(theme))
print(f"name width {name_w:.0f}px of {W}")
