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
        "id": "room", "no": "01", "fig": "room", "title": "Room",
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
        "id": "mylonite", "no": "02", "fig": "mylonite", "title": "Mylonite",
        "meta": "NOV 2026 · RESEARCH · SOLO", "tag": "PREPRINT",
        "line": "Finds races that happen through Redis or Valkey state by controlling the order commands reach the store.",
        "stats": [("1", "MEDIAN EXECUTIONS TO BUG, WITH SOURCE"), ("764 / 97", "STRONGEST NON-AI BASELINE"), ("41.8–59.9 s", "MEDIAN TIME TO BUG; SEARCH 1.0–6.5 S")],
        "caption": "FIG.02 — COMMAND ORDERINGS UNDER TEST",
        "href": f"{GH}/mylonite",
        "body": "A delay-only proxy controls the order commands reach the store, Meta's Muse Spark proposes which requests to race, and plain code decides what counts as a bug; every report must replay 20 times out of 20. In a pre-registered evaluation on two held-out bugs, the model with the service's source needed a median of **1** execution for each, against **764** and **97** for the strongest non-AI baseline. Without the source it was no better than search, and it lost on wall-clock time and dollars, because executions are cheap. The paper reports all of it.",
        "stack": "Python · Valkey · RESP · Docker",
        "links": [("source", f"{GH}/mylonite"), ("paper", f"{PAPERS}/mylonite_fewer_executions_more_seconds.pdf")],
    },
    {
        "id": "harness", "no": "03", "fig": "gemma", "title": "Measure the Harness First",
        "meta": "NOV 2026 · PAPER · WITH SRIRAM KATRAPALLY", "tag": "GEMMA 4 DEVELOPER AGENT",
        "line": "What can be learned about a configuration-only Gemma 4 coding agent before tuning it.",
        "stats": [("16 → 92", "OF 129 TASKS GRADABLE AFTER FIXES"), ("70%", "GOLD FILE IN BM25 TOP FIVE"), ("−42%", "TOOL CALLS, TWO-AGENT SETUP")],
        "caption": "FIG.03 — AGENT LOOP UNDER A TOOL-CALL BUDGET",
        "href": f"{PAPERS}/measure_the_harness_first.pdf",
        "body": "The competition ships an agent as configuration only, run by a fixed harness on one quantized 31B Gemma 4 model. As shipped, the public dev environment could grade just 16 of 129 tasks with their own reference patches; three environment fixes raised that to 92. A BM25 index put a gold file in the top five for 70% of tasks, while the harness's embedding search resolved 2 of 129. With everything else fixed, the per-task tool-call budget, not the prompt, moved the public leaderboard.",
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
    {"id": "feedback", "title": "When feedback backfires", "meta": "MEDIUM · REWARD HACKING & EVALUATION", "tag": "SEP 2026",
     "href": "https://medium.com/@hrmallichetty/when-feedback-backfires-can-better-feedback-teach-ai-agents-to-game-the-system-5a03d05d9262",
     "alt": "When feedback backfires: can better feedback teach AI agents to game their graders? Medium, September 2026."},
    {"id": "arc-essay", "title": "From code review to ARC-AGI-2", "meta": "MEDIUM · FINE-TUNING → REASONING", "tag": "OCT 2026",
     "href": "https://medium.com/@hrmallichetty/from-code-review-to-arc-agi-2-reusing-the-same-ml-muscle-on-a-harder-reasoning-problem-a4be66501d3b",
     "alt": "From code review to ARC-AGI-2: reusing the same ML muscle on a harder reasoning problem. Medium, October 2026."},
]

EXPERIENCE = [
    {"id": "prolifics", "title": "Prolifics", "meta": "ASSOCIATE DATA ENGINEER · FROM INTERN", "tag": "2023 — 2024",
     "alt": "Prolifics, associate data engineer (joined as an intern), 2023 to 2024."},
    {"id": "heidigi", "title": "HeiDigi", "meta": "DATA ANALYST INTERN", "tag": "2022",
     "alt": "HeiDigi, data analyst intern, 2022."},
    {"id": "utd", "title": "UT Dallas", "meta": "MS, BUSINESS ANALYTICS & AI · DISTINCTION", "tag": "2026",
     "alt": "University of Texas at Dallas, MS in Business Analytics and Artificial Intelligence, Scholar With Distinction, 2026."},
    {"id": "gitam", "title": "GITAM", "meta": "B.TECH, COMPUTER SCIENCE & BUSINESS SYSTEMS", "tag": "2024",
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
    s = path(mono, f"/{no}", 13 * k, 0, 26 * k, c["accent"], tracking=1.5)[0]
    s += path(sans, word, 34 * k, 44 * k, 34 * k, c["ink"], tracking=-1)[0]
    if not phone:
        s += path(mono, right, 12, W, 26, c["muted"], tracking=1.5, anchor="end")[0]
    H = 60 * k
    s += f'<path d="M0 {H - 5.5:.1f}H{W}" stroke="{c["rule"]}"/>'
    return svg(W, H, s, f"{no} — {word}")


def stats_row(c, stats, x0, y, width, k):
    """Big numbers with mono labels that wrap inside their column."""
    s, col = "", width / len(stats)
    for i, (v, label) in enumerate(stats):
        x = x0 + i * col
        s += path(sans, v, 26 * k, x, y, c["ink"], tracking=-0.6)[0]
        ls = 10.5 * min(k, 1.3)
        for j, line in enumerate(wrap(mono, label, ls, col - 16, tracking=1.0)):
            s += path(mono, line, ls, x, y + 22 * k + j * ls * 1.45, c["muted"], tracking=1.0)[0]
    return s


def plate(c, p, F, phone):
    if phone:
        W, k = 600, 1.45
        f, fh = figure(p["fig"], c, F, 0, 0, W)
        s = f + path(mono, p["caption"], 12, 0, fh + 26, c["muted"], tracking=1.2)[0]
        y = fh + 72
        tx = 0
        tw = W
    else:
        W, k = 900, 1
        f, fh = figure(p["fig"], c, F, 460, 0, 440)
        s = f + path(mono, p["caption"], 10.5, 460, fh + 22, c["muted"], tracking=1.3)[0]
        y = 22
        tw = 420
    s += path(mono, f"/{p['no']}", 12 * min(k, 1.25), 0, y, c["accent"], tracking=1.4)[0]
    s += path(mono, p["meta"], 12 * min(k, 1.25), 40 * min(k, 1.25), y, c["muted"], tracking=1.4)[0]
    y += 36 * min(k, 1.25)
    s += tag(0, y, p["tag"], c, 10.5 * min(k, 1.3), accent=True)[0]
    size = (52 if len(p["title"]) < 12 else 38) * (1.15 if phone else 1)
    y += 18 + size * 0.95
    for line in wrap(sans, p["title"], size, tw, tracking=-size * 0.035):
        s += path(sans, line, size, -1, y, c["ink"], tracking=-size * 0.035)[0]
        y += size * 1.04
    ls = 17 * (1.3 if phone else 1)
    y += 4
    for line in wrap(text, p["line"], ls, tw - 10):
        s += path(text, line, ls, 0, y, c["muted"])[0]
        y += ls * 1.45
    sy = max(y + 20, 0 if phone else 248)
    s += f'<path d="M0 {sy + 0.5:.1f}H{tw}" stroke="{c["rule"]}"/>'
    s += stats_row(c, p["stats"], 0, sy + 30 * k, tw, k)
    H = sy + (30 + 22 + 34) * k + 14
    if not phone:
        H = max(H, fh + 34)
    return svg(W, H, s, f"{p['title']} — {p['line']}")


def row(c, r, F, phone):
    W = 600 if phone else 900
    thumb = "fig" in r and not phone
    k = 1.45 if phone else 1
    s = path(mono, r["no"], 11 * k, 0, 40 * k, c["muted"], tracking=1.3)[0]
    x = 52 * k
    if thumb:
        f, _ = figure(r["fig"], c, F, 52, 12, 128)
        s += f
        x = 212
    s += path(sans, r["title"], 24 * k, x, 40 * k, c["ink"], tracking=-0.7 * k)[0]
    if phone:
        s += path(mono, r["meta"], 10.5 * 1.3, x, 40 * k + 32, c["muted"], tracking=1.2)[0]
        s += tag(x, 40 * k + 72, r["tag"], c, 10.5 * 1.3)[0]
        H = 40 * k + 96
    else:
        s += path(mono, r["meta"], 12, x, 70, c["muted"], tracking=1.3)[0]
        s += tag(W, 40, r["tag"], c, 11.5, anchor="end")[0]
        H = 106 if thumb else 94
    s += f'<path d="M0 {H - 0.5:.1f}H{W}" stroke="{c["rule"]}"/>'
    return svg(W, H, s, r["alt"])


# ── README ────────────────────────────────────────────────────────


def picture(name, alt, href, width="100%"):
    a = f"assets/body/{name}"
    # <a> alone on its line opens an HTML block; inline, GitHub parses it as
    # a paragraph and pulls the <source> elements out of the <picture>.
    return (f'<a href="{href}">\n<picture>\n'
            f'  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="{a}-dark-phone.svg">\n'
            f'  <source media="(max-width: 600px)" srcset="{a}-light-phone.svg">\n'
            f'  <source media="(prefers-color-scheme: dark)" srcset="{a}-dark.svg">\n'
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
        F = figures(mono, c)
        for phone in (False, True):
            sfx = f"{theme}-phone" if phone else theme
            for no, word, right in SECTIONS:
                (OUT / f"h{no}-{sfx}.svg").write_text(header(c, no, word, right, phone))
            for p in PLATES:
                (OUT / f"plate-{p['id']}-{sfx}.svg").write_text(plate(c, p, F, phone))
            for items in (INDEX, WRITING, EXPERIENCE):
                for i, r in enumerate(items, 1):
                    r.setdefault("no", f"/{i:02d}")
                    (OUT / f"row-{r['id']}-{sfx}.svg").write_text(row(c, r, F, phone))
    readme = ROOT / "README.md"
    src = readme.read_text()
    new = re.sub(r"(<!-- body:start -->\n).*?(<!-- body:end -->)", lambda m: m.group(1) + readme_body() + "\n" + m.group(2), src, flags=re.S)
    readme.write_text(new)
    print(f"{len(list(OUT.glob('*.svg')))} assets")


main()
