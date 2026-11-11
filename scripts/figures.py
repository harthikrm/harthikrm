"""Project figures, ported from harthik.dev's src/figures.js.

Same drawing system as the site (640x400, 1.5 strokes, dotted guides,
one accent reserved for each diagram's signal), with labels outlined so
they render inside <img>. Labels that the code does not back up were
dropped or reworded (see each figure's comment).
"""



def figures(mono, c):
    """Return {name: svg body} for theme colours `c` using outlined font `mono`."""
    INK, ACC = c["ink"], c["accent"]

    def txt(x, y, s, fill=None, size=13, o=1, anchor="start"):
        d, w = mono.run(s, size, tracking=1)
        if anchor == "middle":
            x -= w / 2
        op = f' fill-opacity="{o}"' if o != 1 else ""
        return f'<path transform="translate({x:.1f} {y})" fill="{fill or INK}"{op} d="{d}"/>'

    guide = f'stroke="{INK}" stroke-opacity="0.25" stroke-dasharray="2 5"'

    F = {}

    F["room"] = f"""
    <g stroke="{INK}" stroke-width="1.5">
      <path d="M60 80 H300 Q340 80 360 130 L380 180"/>
      <path d="M60 200 H340 L380 200"/>
      <path d="M60 320 H300 Q340 320 360 270 L380 220"/>
      <path d="M380 200 H580" stroke-width="3"/>
    </g>
    {txt(60, 66, 'GPT')}{txt(60, 186, 'CLAUDE')}{txt(60, 306, 'GEMINI')}{txt(420, 186, 'PROJECT MEMORY')}
    <g fill="{ACC}"><circle cx="60" cy="80" r="4"/><circle cx="60" cy="200" r="4"/><circle cx="60" cy="320" r="4"/><circle cx="580" cy="200" r="5"/></g>
    <g {guide}><path d="M60 120 H280"/><path d="M60 240 H280"/><path d="M60 280 H280"/></g>"""

    # Signal: the site's "65 METRICS/CO" and "10-STEP RAG" are not backed by
    # the repo; this keeps only what the code shows.
    F["signal"] = f"""
    <g stroke="{INK}" stroke-width="1.5">
      <rect x="50" y="128" width="104" height="34"/><rect x="50" y="218" width="104" height="34"/>
      <path d="M154 145 H180 L206 178"/><path d="M154 235 H180 L206 202"/>
      <rect x="206" y="172" width="84" height="36"/>
      <path d="M290 190 H330"/>
      <ellipse cx="368" cy="172" rx="38" ry="11"/>
      <path d="M330 172 V236 M406 172 V236"/><ellipse cx="368" cy="236" rx="38" ry="11"/>
      <path d="M406 204 H444"/>
      <rect x="444" y="162" width="76" height="14"/><rect x="444" y="184" width="76" height="14"/><rect x="444" y="206" width="76" height="14"/>
    </g>
    {txt(58, 149, 'SEC EDGAR', size=12)}{txt(58, 239, 'PRICES', size=12)}{txt(214, 194, 'AIRFLOW', size=12)}
    {txt(330, 268, 'PGVECTOR', size=12)}{txt(444, 240, 'DBT', size=12)}{txt(540, 194, '70', size=22)}{txt(540, 212, 'COMPANIES', size=10, o=0.55)}
    <g stroke="{ACC}" stroke-width="1.5">
      <path d="M560 60 V96 H390 V158"/><path d="M400 120 H624 V330 H480" stroke-dasharray="5 5"/>
    </g>
    <circle cx="390" cy="158" r="4" fill="{ACC}"/><circle cx="480" cy="330" r="4" fill="{ACC}"/>
    {txt(432, 52, 'QUESTION', fill=ACC)}{txt(56, 334, 'CITED ANSWER · RAG + LANGGRAPH AGENT', fill=ACC, size=11)}
    <path d="M470 330 H360" {guide}/>"""

    # Code Sentinel: "<1% trained" and "every PR" dropped; the bot is past tense.
    F["code_sentinel"] = f"""
    <g stroke="{INK}" stroke-width="1.5">
      <rect x="62" y="162" width="104" height="52"/><rect x="54" y="154" width="104" height="52"/><rect x="46" y="146" width="104" height="52"/>
      <path d="M166 190 H228"/>
      <rect x="228" y="130" width="124" height="120"/>
      <path d="M352 190 H414"/>
      <rect x="414" y="96" width="172" height="208"/>
      <path d="M414 126 H586"/>
    </g>
    <rect x="229" y="231" width="122" height="18" fill="{ACC}" fill-opacity="0.9"/>
    {txt(46, 232, '143K PAIRS', size=11)}{txt(240, 160, 'MISTRAL-7B', size=12)}{txt(240, 180, 'QLORA · H100', size=10, o=0.55)}
    {txt(238, 244, 'ADAPTERS', size=10, fill=c['bg'])}
    {txt(424, 116, 'PULL REQUEST', size=11)}
    {txt(430, 152, '- old_check()', size=12, o=0.55)}{txt(430, 172, '+ new_check()', size=12)}
    {txt(430, 192, '- retries = 0', size=12, o=0.55)}{txt(430, 212, '+ retries = 3', size=12)}
    <circle cx="594" cy="168" r="4" fill="{ACC}"/>
    <path d="M594 172 V252 H586" stroke="{ACC}" stroke-width="1.5"/>
    <rect x="430" y="238" width="140" height="28" stroke="{ACC}" stroke-width="1.5"/>
    {txt(440, 256, 'AI REVIEW', size=11, fill=ACC)}
    {txt(169, 180, 'FINE-TUNE', size=8, o=0.55)}{txt(46, 330, 'VERTEX AI · GITHUB ACTIONS REVIEW BOT', size=11, o=0.55)}
    <path d="M46 344 H394" {guide}/>"""

    # Mylonite is about the order requests' commands reach the store, not
    # thread interleavings, so the lanes are requests and the check is the contract.
    F["mylonite"] = f"""
    <g stroke="{INK}" stroke-width="1.5">
      <path d="M60 130 H230 L290 190 H400 L460 130 H580"/>
      <path d="M60 190 H230 L290 130 H400 L460 190 H510"/>
      <path d="M60 270 H580" stroke-opacity="0.3"/>
    </g>
    <path d="M510 190 L580 250" stroke="{ACC}" stroke-width="2"/>
    {txt(60, 116, 'REQUEST A')}{txt(60, 176, 'REQUEST B')}{txt(60, 256, 'CONTRACT', o=0.4)}{txt(470, 286, 'VIOLATION', fill=ACC)}
    {txt(236, 330, 'PROXY REORDERS COMMANDS', size=10, o=0.55)}
    <circle cx="580" cy="250" r="5" fill="{ACC}"/>
    <g {guide}><path d="M230 90 V310"/><path d="M400 90 V310"/></g>"""

    F["arc"] = f"""
    <g stroke="{INK}" stroke-width="1.5">
      <path d="M70 130 H214 M70 178 H214 M70 226 H214 M70 274 H214 M70 130 V274 M118 130 V274 M166 130 V274 M214 130 V274"/>
    </g>
    <g fill="{INK}"><rect x="70" y="130" width="48" height="48"/><rect x="118" y="178" width="48" height="48"/><rect x="166" y="226" width="48" height="48"/></g>
    <path d="M214 202 H258" stroke="{INK}" stroke-width="1.5"/>
    <rect x="258" y="170" width="128" height="64" stroke="{INK}" stroke-width="1.5"/>
    {txt(272, 198, 'SOLVER')}{txt(272, 218, 'NVARC', size=10, o=0.55)}
    <path d="M386 202 H430" stroke="{INK}" stroke-width="1.5"/>
    <g stroke="{INK}" stroke-width="1.5">
      <path d="M430 130 H574 M430 178 H574 M430 226 H574 M430 274 H574 M430 130 V274 M478 130 V274 M526 130 V274 M574 130 V274"/>
    </g>
    <g fill="{ACC}"><rect x="526" y="130" width="48" height="48"/><rect x="478" y="178" width="48" height="48"/><rect x="430" y="226" width="48" height="48"/></g>
    {txt(70, 112, 'SYNTHETIC TASKS', size=11, o=0.55)}{txt(430, 112, 'KEPT BY LIKELIHOOD', size=11, o=0.55)}
    {txt(70, 330, 'SOLVER-IN-THE-LOOP DATA SELECTION', size=11)}
    <path d="M70 344 H574" {guide}/>"""

    F["gemma"] = f"""
    <g stroke="{INK}" stroke-width="1.5">
      <rect x="48" y="166" width="124" height="68"/>
      <path d="M172 200 H226"/>
      <circle cx="320" cy="200" r="64"/>
      <path d="M384 200 H454"/>
      <rect x="454" y="178" width="92" height="44"/>
    </g>
    {txt(60, 192, 'REPO@COMMIT', size=11)}{txt(60, 212, '+ ISSUE', size=11, o=0.55)}
    {txt(320, 196, 'AGENT', anchor='middle')}{txt(320, 216, 'GEMMA 4', size=10, o=0.55, anchor='middle')}
    {txt(466, 204, 'PATCH', size=12)}
    {txt(480, 246, 'submit_patch', size=11, fill=ACC)}
    <g stroke="{INK}" stroke-width="1.5">
      <path d="M268 158 A66 66 0 0 1 372 158"/><path d="M372 242 A66 66 0 0 1 268 242"/>
    </g>
    <path d="M369 155 l6 -8 M369 155 l10 1 M271 245 l-6 8 M271 245 l-10 -1" stroke="{INK}" stroke-width="1.5"/>
    {txt(320, 96, 'PLAN → ACT → OBSERVE', size=10, o=0.55, anchor='middle')}
    <rect x="236" y="320" width="168" height="30" stroke="{INK}" stroke-opacity="0.45" stroke-width="1.5"/>
    {txt(320, 339, 'TOOL-CALL BUDGET', size=10, o=0.55, anchor='middle')}
    <path d="M320 264 V320" stroke="{INK}" stroke-opacity="0.45" stroke-width="1.5" stroke-dasharray="5 5"/>
    <circle cx="546" cy="200" r="4" fill="{ACC}"/>"""

    # Quant Risk Desk: a return series against its VaR line, the breaches marked.
    # Abstract on purpose: no numbers from the repo are drawn.
    F["quant"] = f"""
    <path d="M60 300 H580" stroke="{INK}" stroke-opacity="0.3" stroke-width="1.5"/>
    <path d="M60 170 L100 150 L140 186 L180 160 L220 204 L260 176 L300 262 L340 214 L380 230 L420 192 L460 276 L500 210 L540 180 L580 196"
          stroke="{INK}" stroke-width="1.5"/>
    <path d="M60 248 H580" stroke="{ACC}" stroke-width="1.5" stroke-dasharray="5 5"/>
    <g fill="{ACC}"><circle cx="300" cy="262" r="5"/><circle cx="460" cy="276" r="5"/></g>
    {txt(60, 120, 'SECTOR RETURNS', size=11, o=0.55)}{txt(470, 238, 'VAR', size=11, fill=ACC)}
    {txt(60, 340, 'VAR · CVAR · DRAWDOWN · 11 SECTORS', size=11)}
    <path d="M60 354 H580" {guide}/>"""

    return F
