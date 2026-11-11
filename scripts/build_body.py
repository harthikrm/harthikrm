"""Generate the README body: section headers, project plates and index rows.

Every item is written four times (light/dark x desktop/phone) to assets/,
and the README text between the body markers is regenerated from CONTENT
below, so alt text, links and images cannot drift apart.

    python scripts/build_body.py ~/fonts

Facts here must already be public: on harthik.dev, in a published paper,
or in the linked repository. Nothing is drawn that the source does not say.
"""

import re
import sys
from html import escape
from pathlib import Path

from figures import figures
from outline import Face

FONTS = Path(sys.argv[1]).expanduser()
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "body"

THEMES = {
    "light": {"bg": "#ffffff", "ink": "#1f2328", "muted": "#59636e", "rule": "#d1d9e0", "surf": "#f6f8fa", "accent": "#2b45ff"},
    "dark": {"bg": "#0d1117", "ink": "#f0f6fc", "muted": "#9198a1", "rule": "#3d444d", "surf": "#151b23", "accent": "#7c8cff"},
}

sans = Face(FONTS, "Geist[wght].ttf", 600)
text = Face(FONTS, "Geist[wght].ttf", 400)
mono = Face(FONTS, "GeistMono[wght].ttf", 400)

SITE = "https://www.harthik.dev"
PAPERS = f"{SITE}/papers"
GH = "https://github.com/harthikrm"

# ── Content ───────────────────────────────────────────────────────

PLATES = [
    {
        "id": "room", "fig": "room", "title": "Room",
        "meta": "MAY 2026 — PRESENT · FOUNDER", "tag": "PRIVATE EARLY ACCESS",
        "line": "GPT, Claude and Gemini answer side by side, each briefed from one confirmed project memory.",
        # As published on harthik.dev; the app's repository is private.
        "stats": [("971", "AUTOMATED TESTS"), ("24/24", "MEMORY-RECALL EVALS"), ("0/30", "PROMPT INJECTIONS SUCCEEDED")],
        "caption": "FIG.01 — THREE MODELS, ONE PROJECT MEMORY",
        "href": "https://joinaroom.app",
        "body": "Decisions and constraints are proposed from the conversation, only the ones you confirm are kept, and each links back to the message it came from. Up to three models stream in parallel, with failures isolated per model.",
        "stack": "Next.js · TypeScript · PostgreSQL · Supabase · OpenRouter",
        "links": [("joinaroom.app", "https://joinaroom.app")],
    },
    {
        "id": "mylonite", "fig": "mylonite", "title": "Mylonite",
        "meta": "NOV 2026 · RESEARCH · SOLO", "tag": "PREPRINT",
        "line": "Finds races through Redis or Valkey state by controlling the order commands reach the store.",
        "stats": [("1", "MEDIAN RUNS TO BUG, WITH SOURCE"), ("764 / 97", "STRONGEST NON-AI BASELINE"), ("41.8–59.9 s", "MEDIAN TIME; SEARCH 1.0–6.5S")],
        "caption": "FIG.02 — COMMAND ORDERINGS UNDER TEST",
        "href": f"{GH}/mylonite",
        "body": "A delay-only proxy controls the order commands reach the store, Meta's Muse Spark proposes which requests to race, and plain code decides what counts as a bug; every report must replay 20 times out of 20. In a pre-registered evaluation on two held-out bugs, the model with the service's source needed a median of **1** execution for each, against **764** and **97** for the strongest non-AI baseline. Even with the source it was slower and more expensive than systematic search (median 41.8 s and 59.9 s against 1.0–6.5 s), because one execution costs about 9 ms. Without the source it was not better than the conventional baselines on any metric. The paper reports all of it.",
        "stack": "Python · Valkey · RESP · Docker",
        "links": [("source", f"{GH}/mylonite"), ("paper", f"{PAPERS}/mylonite_fewer_executions_more_seconds.pdf")],
    },
    {
        "id": "harness", "fig": "gemma", "title": "Measure the Harness First",
        "meta": "NOV 2026 · PAPER · WITH SRIRAM KATRAPALLY", "tag": "GEMMA 4 DEVELOPER AGENT",
        "line": "What can be learned about a configuration-only Gemma 4 coding agent before tuning it.",
        "stats": [("16 → 92", "OF 129 TASKS GRADABLE AFTER FIXES"), ("70%", "GOLD FILE IN BM25 TOP FIVE"), ("−42%", "TOOL CALLS, TWO-AGENT SETUP")],
        "caption": "FIG.03 — AGENT LOOP UNDER A TOOL-CALL BUDGET",
        "href": f"{PAPERS}/measure_the_harness_first.pdf",
        "body": "Entrants ship an agent as configuration only, which the competition's fixed harness runs on one quantized 31B Gemma 4 model. As shipped, the public dev environment could grade just 16 of 129 tasks with their own reference patches; three environment fixes raised that to 92. A BM25 index put a gold file in the top five for 70% of tasks, while the harness's embedding search returned any result on only 2 of 129, because queries had to match a fully qualified name exactly. With everything else fixed, the per-task tool-call budget, not the prompt, moved the public leaderboard.",
        "stack": "Gemma 4 · vLLM · SWE-bench-style tasks · BM25",
        "links": [("paper", f"{PAPERS}/measure_the_harness_first.pdf")],
    },
]

INDEX = [
    {"id": "signal", "fig": "signal", "title": "Signal", "meta": "2026 · AIRFLOW · DBT · PGVECTOR · LANGGRAPH", "tag": "SOURCE",
     "href": f"{GH}/signal", "alt": "Signal: ask about a company and get an answer cited to its filings, built on Airflow, dbt, pgvector and LangGraph."},
    {"id": "arc", "fig": "arc", "title": "Let the Solver Choose Its Data", "meta": "NOV 2026 · ARC PRIZE 2026 PAPER TRACK", "tag": "PAPER",
     "href": f"{GH}/arc-prize-2026-paper", "alt": "Let the Solver Choose Its Data: ARC Prize 2026 paper on selecting synthetic tasks by the NVARC solver's own likelihood."},
    {"id": "sentinel", "fig": "code_sentinel", "title": "Code Sentinel", "meta": "2026 · MISTRAL-7B · QLORA · 143K PAIRS", "tag": "SOURCE",
     "href": f"{GH}/code-sentinel", "alt": "Code Sentinel: QLoRA fine-tune of Mistral-7B-Instruct on 143K code-review pairs, with a GitHub Actions review bot."},
    {"id": "quant", "fig": "quant", "title": "Quant Risk Desk", "meta": "2026 · AIRFLOW · POSTGRES · DBT · 11 SECTORS", "tag": "SOURCE",
     "href": f"{GH}/quant-risk-desk", "alt": "Quant Risk Desk: Airflow ingest into Postgres with dbt models computing VaR, CVaR and drawdowns across 11 sectors."},
]

WRITING = [
    {"id": "feedback", "title": "When feedback backfires", "meta": "MEDIUM · REWARD HACKING & EVALUATION", "tag": "SEP 2026", "boxed": False,
     "href": "https://medium.com/@hrmallichetty/when-feedback-backfires-can-better-feedback-teach-ai-agents-to-game-the-system-5a03d05d9262",
     "alt": "When feedback backfires: can better feedback teach AI agents to game their graders? Medium, September 2026."},
    {"id": "arc-essay", "title": "From code review to ARC-AGI-2", "meta": "MEDIUM · FINE-TUNING → REASONING", "tag": "OCT 2026", "boxed": False,
     "href": "https://medium.com/@hrmallichetty/from-code-review-to-arc-agi-2-reusing-the-same-ml-muscle-on-a-harder-reasoning-problem-a4be66501d3b",
     "alt": "From code review to ARC-AGI-2: reusing the same ML muscle on a harder reasoning problem. Medium, October 2026."},
]

EXPERIENCE = [
    {"id": "prolifics", "title": "Prolifics", "meta": "ASSOCIATE DATA ENGINEER · FROM INTERN", "tag": "2023 — 2024", "boxed": False,
     "alt": "Prolifics, associate data engineer (joined as an intern), 2023 to 2024."},
    {"id": "heidigi", "title": "HeiDigi", "meta": "DATA ANALYST INTERN", "tag": "2022", "boxed": False,
     "alt": "HeiDigi, data analyst intern, 2022."},
    {"id": "utd", "title": "UT Dallas", "meta": "MS, BUSINESS ANALYTICS & AI · DISTINCTION", "tag": "2026", "boxed": False,
     "alt": "University of Texas at Dallas, MS in Business Analytics and Artificial Intelligence, Scholar With Distinction, 2026."},
    {"id": "gitam", "title": "GITAM", "meta": "B.TECH, COMPUTER SCIENCE & BUSINESS SYSTEMS", "tag": "2024", "boxed": False,
     "alt": "GITAM University, B.Tech in Computer Science and Business Systems, 2024."},
]
for e in EXPERIENCE:
    e["href"] = f"{SITE}/#experience"

SECTIONS = [
    ("01", "Selected work", f"{len(PLATES)} ENTRIES"),
    ("02", "Index", f"{len(INDEX)} MORE"),
    ("03", "Writing", "MEDIUM"),
    ("04", "Experience", "RÉSUMÉ ON HARTHIK.DEV"),
]

# ── Drawing ───────────────────────────────────────────────────────


def path(face, s, size, x, y, fill, tracking=0.0, opacity=1, anchor="start"):
    d, w = face.run(s, size, tracking=tracking)
    if anchor == "end":
        x -= w
    op = f' fill-opacity="{opacity}"' if opacity != 1 else ""
    return f'<path transform="translate({x:.1f} {y:.1f})" fill="{fill}"{op} d="{d}"/>', w


def wrap(face, s, size, width, tracking=0.0):
    lines, cur = [], ""
    for word in s.split():
        t = f"{cur} {word}".strip()
        if cur and face.run(t, size, tracking)[1] > width:
            lines.append(cur)
            cur = word
        else:
            cur = t
    return lines + [cur]


def tag(x, y, s, c, size, accent=False, anchor="start"):
    """Boxed mono status tag with its baseline at y, like the site's [PRIVATE EARLY ACCESS]."""
    d, w = mono.run(s, size, tracking=size * 0.13)
    pad, h = size * 0.75, size * 2
    bw = w + 2 * pad
    if anchor == "end":
        x -= bw
    col = c["accent"] if accent else c["muted"]
    return (f'<rect x="{x:.1f}" y="{y - size * 1.35:.1f}" width="{bw:.1f}" height="{h:.1f}" stroke="{col}" stroke-opacity=".6"/>'
            f'<path transform="translate({x + pad:.1f} {y:.1f})" fill="{col}" d="{d}"/>'), bw


def figure(name, c, F, x, y, w):
    h = w * 400 / 640
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" fill="{c["surf"]}"/>'
            f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="0 0 640 400">{F[name]}</svg>'), h


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h:.0f}" width="{w}" height="{h:.0f}" fill="none" role="img" aria-label="{escape(label)}">'
            f"<title>{escape(label)}</title>{body}</svg>\n")


def header(c, no, word, right, phone):
    W = 600 if phone else 900
    k = 1.4 if phone else 1
    s = path(mono, f"/{no}", (13 if phone else 14) * k, 0, 26 * k, c["accent"], tracking=1.5)[0]
    s += path(sans, word, 34 * k, 44 * k, 34 * k, c["ink"], tracking=-1)[0]
    if not phone:
        s += path(mono, right, 13.5, W, 26, c["muted"], tracking=1.4, anchor="end")[0]
    H = 60 * k
    s += f'<path d="M0 {H - 5.5:.1f}H{W}" stroke="{c["rule"]}"/>'
    return svg(W, H, s, f"{no} — {word}")


def balanced(face, s, size, width, tracking=0.0):
    """One line if it fits, else the two-line split whose longer line is shortest."""
    if face.run(s, size, tracking)[1] <= width:
        return [s]
    words = s.split()
    splits = [(" ".join(words[:i]), " ".join(words[i:])) for i in range(1, len(words))]
    return list(min(splits, key=lambda ab: max(face.run(t, size, tracking)[1] for t in ab)))


def stats_row(c, stats, x0, y, width, k, ls):
    """Big numbers with mono labels that wrap inside their column; returns (svg, depth)."""
    s, col, depth = "", width / len(stats), 0
    for i, (v, label) in enumerate(stats):
        x = x0 + i * col
        s += path(sans, v, 26 * k, x, y, c["ink"], tracking=-0.6)[0]
        lines = wrap(mono, label, ls, col - 16, tracking=1.0)
        for j, line in enumerate(lines):
            s += path(mono, line, ls, x, y + 22 * k + j * ls * 1.45, c["muted"], tracking=1.0)[0]
        depth = max(depth, 22 * k + (len(lines) - 1) * ls * 1.45)
    return s, depth


def plate(c, p, F, phone):
    # The FIG caption numbers the plate; the section header carries the /0N.
    if phone:
        W, k, tw = 600, 1.45, 600
        f, fh = figure(p["fig"], c, F, 0, 0, W)
        s = f + path(mono, p["caption"], 18, 0, fh + 34, c["muted"], tracking=1.2)[0]
        y, ms, ts, ls_label = fh + 84, 19, 17, 17
    else:
        W, k, tw = 900, 1, 420
        f, fh = figure(p["fig"], c, F, 460, 0, 440)
        s = f + path(mono, p["caption"], 12, 460, fh + 30, c["muted"], tracking=1.2)[0]
        y, ms, ts, ls_label = 22, 13.5, 11.5, 11.5
    s += path(mono, p["meta"], ms, 0, y, c["muted"], tracking=1.4)[0]
    y += ms * 3
    s += tag(0, y, p["tag"], c, ts, accent=True)[0]
    size = 46 * (1.15 if phone else 1)
    y += 18 + size * 0.95
    for line in balanced(sans, p["title"], size, tw, tracking=-size * 0.035):
        s += path(sans, line, size, -1, y, c["ink"], tracking=-size * 0.035)[0]
        y += size * 1.04
    ls = 22 if phone else 18
    y += 4
    for line in wrap(text, p["line"], ls, tw - 10):
        s += path(text, line, ls, 0, y, c["muted"])[0]
        y += ls * 1.45
    # On desktop the stats rule continues the figure's bottom edge.
    sy = y + 16 if phone else max(y + 16, fh)
    s += f'<path d="M0 {sy + 0.5:.1f}H{tw}" stroke="{c["rule"]}"/>'
    st, depth = stats_row(c, p["stats"], 0, sy + 30 * k, tw, k, ls_label)
    s += st
    H = sy + 30 * k + depth + 18
    return svg(W, H, s, f"{p['title']} — {p['line']}")


def row(c, r, F, phone):
    """Index, writing and experience rows; dates print plain, statuses get a box."""
    W = 600 if phone else 900
    thumb = "fig" in r and not phone
    boxed = r.get("boxed", True)
    k = 1.45 if phone else 1
    s = path(mono, r["no"], 18 if phone else 13.5, 0, 40 * k, c["muted"], tracking=1.3)[0]
    x = 64 * k
    if thumb:
        f, _ = figure(r["fig"], c, F, 64, 12, 128)
        s += f
        x = 220
    s += path(sans, r["title"], 24 * k, x, 40 * k, c["ink"], tracking=-0.7 * k)[0]
    if phone:
        lines = [r["meta"]]
        if not boxed:
            joined = f'{r["meta"]} · {r["tag"]}'
            lines = [joined] if mono.run(joined, 17, 1.2)[1] <= W - x else [r["meta"], r["tag"]]
        for j, line in enumerate(lines):
            s += path(mono, line, 17, x, 40 * k + 34 + j * 26, c["muted"], tracking=1.2)[0]
        if boxed:
            s += tag(x, 40 * k + 76, r["tag"], c, 15)[0]
            H = 40 * k + 100
        else:
            H = 40 * k + 32 + 26 * len(lines)
    else:
        s += path(mono, r["meta"], 13.5, x, 72, c["muted"], tracking=1.2)[0]
        if boxed:
            s += tag(W, 40, r["tag"], c, 12.5, anchor="end")[0]
        else:
            s += path(mono, r["tag"], 13.5, W, 40, c["muted"], tracking=1.2, anchor="end")[0]
        H = 106 if thumb else 94
    s += f'<path d="M0 {H - 0.5:.1f}H{W}" stroke="{c["rule"]}"/>'
    return svg(W, H, s, r["alt"])


# ── README ────────────────────────────────────────────────────────


def sources(a):
    """<source> lines for asset stem `a`, light/dark x desktop/phone.

    GitHub's <themed-picture> rewrites the whole media query of any source
    containing "prefers-color-scheme: light|dark" (with that space) so it
    follows the GitHub theme, which would drop a width condition. The phone
    sources leave the space out, so GitHub leaves them alone: they apply only
    to narrow screens and follow the OS scheme. The desktop pair is themed by GitHub.
    """
    return (f'  <source media="(max-width: 600px) and (prefers-color-scheme:dark)" srcset="{a}-dark-phone.svg">\n'
            f'  <source media="(max-width: 600px)" srcset="{a}-light-phone.svg">\n'
            f'  <source media="(prefers-color-scheme: dark)" srcset="{a}-dark.svg">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="{a}-light.svg">\n')


def picture(name, alt, href, width="100%"):
    a = f"assets/body/{name}"
    # <a> alone on its line opens an HTML block; inline, GitHub parses it as
    # a paragraph and pulls the <source> elements out of the <picture>.
    return (f'<a href="{href}">\n<picture>\n{sources(a)}'
            f'  <img src="{a}-light.svg" width="{width}" alt="{escape(alt)}">\n'
            f"</picture>\n</a>")


def readme_body():
    out = []
    sec = iter(SECTIONS)

    def section_header():
        no, word, _ = next(sec)
        out.append(picture(f"h{no}", f"{no} — {word}", f"{SITE}"))

    section_header()
    for i, p in enumerate(PLATES):
        if i:
            out.append("<br>")
        out.append(picture(f"plate-{p['id']}", f"{p['title']} — {p['line']}", p["href"]))
        links = " · ".join(f'<a href="{u}">{t}</a>' for t, u in p["links"])
        out.append(f"{p['body']}\n\n<samp>{p['stack']}&ensp;→&ensp;{links}</samp>")
    for items in (INDEX, WRITING, EXPERIENCE):
        out.append("<br>")
        section_header()
        out.extend(picture(f"row-{r['id']}", r["alt"], r["href"]) for r in items)
    out.append(f'<samp><sub><a href="{SITE}/Harthik_Mallichetty_Resume.pdf">Résumé (PDF)</a>&ensp;·&ensp;Also: McKinsey.org Forward Program · Anthropic Claude 101 and AI Fluency · IBM Data Analytics internship</sub></samp>')
    return "\n\n".join(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for theme, c in THEMES.items():
        # Plates show the figure at 440/640 on desktop; lift its smallest labels.
        F = figures(mono, c, min_label=15)
        F_phone = figures(mono, c, min_label=18)
        F_thumb = figures(mono, c, labels=False)
        for phone in (False, True):
            sfx = f"{theme}-phone" if phone else theme
            for no, word, right in SECTIONS:
                (OUT / f"h{no}-{sfx}.svg").write_text(header(c, no, word, right, phone))
            for p in PLATES:
                (OUT / f"plate-{p['id']}-{sfx}.svg").write_text(plate(c, p, F_phone if phone else F, phone))
            for sec_no, items in (("02", INDEX), ("03", WRITING), ("04", EXPERIENCE)):
                for i, r in enumerate(items, 1):
                    r.setdefault("no", f"{sec_no}.{i}")
                    (OUT / f"row-{r['id']}-{sfx}.svg").write_text(row(c, r, F_thumb, phone))
    readme = ROOT / "README.md"
    src = readme.read_text()
    src = re.sub(r"(<picture>\n)(?:  <source[^\n]*masthead[^\n]*\n)+", lambda m: m.group(1) + sources("assets/masthead"), src, count=1)
    new = re.sub(r"(<!-- body:start -->\n).*?(<!-- body:end -->)", lambda m: m.group(1) + readme_body() + "\n" + m.group(2), src, flags=re.S)
    readme.write_text(new)
    print(f"{len(list(OUT.glob('*.svg')))} assets")


main()
