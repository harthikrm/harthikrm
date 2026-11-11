"""Generate assets/masthead-{light,dark}.svg.

Type is converted to outlines so the masthead renders identically
everywhere: GitHub serves README images through <img>, which cannot load
web fonts. Fonts (OFL, from github.com/google/fonts) are read from the
directory given as the first argument:

    InstrumentSerif-Regular.ttf, IBMPlexMono-Regular.ttf

    pip install fonttools uharfbuzz
    python scripts/build_masthead.py ~/fonts
"""

import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS = Path(sys.argv[1]).expanduser()
OUT = Path(__file__).resolve().parent.parent / "assets"

W, H = 900, 228

THEMES = {
    # GitHub's own foreground tokens, so the type sits in the page.
    "light": {"ink": "#1f2328", "muted": "#59636e", "accent": "#2b45ff"},
    "dark": {"ink": "#f0f6fc", "muted": "#9198a1", "accent": "#7c8cff"},
}


class Face:
    def __init__(self, filename):
        path = FONTS / filename
        self.tt = TTFont(path)
        self.glyphs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        self.hb = hb.Font(hb.Face(hb.Blob(path.read_bytes())))

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


serif = Face("InstrumentSerif-Regular.ttf")
mono = Face("IBMPlexMono-Regular.ttf")

name_d, name_w = serif.run("Harthik Mallichetty", 100, tracking=-0.8)
role_d, _ = mono.run("DATA & AI ENGINEER", 21, tracking=3)
city_d, city_w = mono.run("DALLAS, TEXAS", 21, tracking=3)

# The rule: three strands converge into one line that runs to the edge.
# It is the shape of the work — several sources, one system.
RULE_Y = 190
strands = [
    f"M1 {RULE_Y - 22} H96 C150 {RULE_Y - 22} 168 {RULE_Y} 214 {RULE_Y}",
    f"M1 {RULE_Y} H214",
    f"M1 {RULE_Y + 22} H96 C150 {RULE_Y + 22} 168 {RULE_Y} 214 {RULE_Y}",
]
main = f"M214 {RULE_Y} H{W - 14}"


def render(theme):
    c = THEMES[theme]
    # Deliberately static: browsers pause animation in <img> SVGs (hidden
    # tabs, Safari), and a paused draw-on would leave the rule invisible.
    strand_paths = "".join(f'<path d="{d}"/>' for d in strands)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Harthik Mallichetty — Data and AI engineer, Dallas, Texas">
<g fill="{c['muted']}">
<path transform="translate(2 36)" d="{role_d}"/>
<path transform="translate({W - 2 - city_w:.1f} 36)" d="{city_d}"/>
</g>
<path fill="{c['ink']}" transform="translate(0 134)" d="{name_d}"/>
<g fill="none" stroke="{c['ink']}" stroke-linecap="round">
<g stroke-width="1.5" stroke-opacity=".55">{strand_paths}</g>
<path stroke-width="2.5" d="{main}"/>
</g>
<circle cx="{W - 8}" cy="{RULE_Y}" r="5.5" fill="{c['accent']}"/>
</svg>
"""


OUT.mkdir(exist_ok=True)
for theme in THEMES:
    (OUT / f"masthead-{theme}.svg").write_text(render(theme))
print(f"name width {name_w:.0f}px of {W}")
