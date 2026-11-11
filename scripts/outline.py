"""Shaped, outlined type for the README's SVG assets.

GitHub serves README images through <img>, which cannot load web fonts,
so every label is converted to paths. Fonts are the OFL Geist and Geist
Mono variable fonts from github.com/google/fonts (ofl/geist, ofl/geistmono).
"""

from io import BytesIO
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


class Face:
    def __init__(self, fontdir, filename, weight):
        tt = TTFont(Path(fontdir) / filename)
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
