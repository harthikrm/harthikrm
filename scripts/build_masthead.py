"""Generate assets/masthead-{light,dark}[-phone].svg.

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
from pathlib import Path

from outline import Face

FONTS = Path(sys.argv[1]).expanduser()
OUT = Path(__file__).resolve().parent.parent / "assets"

W, H = 900, 190

THEMES = {
    # GitHub's own foreground tokens; the name fades from ink into the accent
    # and on to a violet, over a faint glow of the accent.
    "light": {"ink": "#1f2328", "muted": "#59636e", "accent": "#2b45ff", "violet": "#9b5cff", "glow": 0.14},
    "dark": {"ink": "#f0f6fc", "muted": "#9198a1", "accent": "#7c8cff", "violet": "#c08cff", "glow": 0.22},
}


sans = Face(FONTS, "Geist[wght].ttf", 600)
mono = Face(FONTS, "GeistMono[wght].ttf", 400)

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


# Phone layout: the name stacks so it can stay large at 375px wide.
PW, PH = 600, 330
first_d, _ = sans.run("Harthik", 112, tracking=-4.4)
last_d, last_w = sans.run("Mallichetty", 112, tracking=-4.4)
p_labels = [mono.run(t, 24, tracking=2.6) for t in LABELS]


def render_phone(theme):
    c = THEMES[theme]
    (d0, w0), (d1, w1), (d2, _) = p_labels
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" role="img" aria-label="Harthik Mallichetty — Data and AI engineer, Dallas, Texas. Building Room.">
<defs>
<linearGradient id="name" x1="0" y1="20" x2="{last_w:.0f}" y2="220" gradientUnits="userSpaceOnUse">
<stop offset=".3" stop-color="{c['ink']}"/><stop offset=".78" stop-color="{c['accent']}"/><stop offset="1" stop-color="{c['violet']}"/>
</linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{c['accent']}" stop-opacity="{c['glow']}"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></radialGradient>
</defs>
<ellipse cx="420" cy="170" rx="220" ry="110" fill="url(#glow)"/>
<g fill="url(#name)"><path transform="translate(-3 100)" d="{first_d}"/><path transform="translate(-3 210)" d="{last_d}"/></g>
<g fill="{c['muted']}"><path transform="translate(2 272)" d="{d0}"/><path transform="translate({2 + w0 + 34:.1f} 272)" d="{d1}"/><path transform="translate(2 312)" d="{d2}"/></g>
<circle cx="{2 + w0 + 17:.1f}" cy="263" r="3" fill="{c['accent']}"/>
</svg>
"""


OUT.mkdir(exist_ok=True)
for theme in THEMES:
    (OUT / f"masthead-{theme}.svg").write_text(render(theme))
    (OUT / f"masthead-{theme}-phone.svg").write_text(render_phone(theme))
print(f"name width {name_w:.0f}px of {W}; phone {last_w:.0f}px of {PW}")
