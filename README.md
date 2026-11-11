<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/masthead-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/masthead-light.svg">
  <img src="assets/masthead-light.svg" width="100%" alt="Harthik Mallichetty — Data and AI engineer, Dallas, Texas">
</picture>

I build AI systems that hold up outside the notebook — the data pipelines underneath, the models and evaluations in the middle, and the product on top. Right now that means [Room](https://joinaroom.app), a workspace where several models work from one shared project memory.

<samp>Dallas, TX&ensp;·&ensp;<a href="https://www.harthik.dev">harthik.dev</a>&ensp;·&ensp;<a href="https://www.linkedin.com/in/harthikmallichetty">LinkedIn</a>&ensp;·&ensp;<a href="https://medium.com/@hrmallichetty">Writing</a>&ensp;·&ensp;<a href="mailto:hrmallichetty@gmail.com">Email</a></samp>

<br>

### <samp>01</samp>&ensp;Room

<samp><sub>FOUNDER&ensp;·&ensp;2026 —&ensp;·&ensp;PRIVATE EARLY ACCESS</sub></samp>

Explain a project once, then work with whichever model you want. Room runs GPT, Claude and Gemini side by side, each answering independently from the same project memory: the decisions, constraints and open questions you have approved, linked back to the conversations they came from.

<samp><sub>Next.js · TypeScript · PostgreSQL · Supabase · OpenRouter · SSE</sub></samp>&ensp;→&ensp;[joinaroom.app](https://joinaroom.app)

### <samp>02</samp>&ensp;Signal

<samp><sub>FINANCIAL RESEARCH&ensp;·&ensp;2026&ensp;·&ensp;END TO END</sub></samp>

Ask about a company; get an answer cited to its filings. Airflow pulls SEC XBRL facts, filing text and daily prices for 70 public companies. dbt models them from staging to marts, under custom tests, and filings are embedded with a finance-tuned model into pgvector. On top sit a cited RAG chat and a LangGraph agent that plans, calls six data tools, checks its own work and replans before answering. CI runs dbt and API tests against a pgvector container, then deploys to Cloud Run and Vercel.

<samp><sub>Python · Airflow · dbt · PostgreSQL · pgvector · LangGraph · FastAPI · React · GCP</sub></samp>&ensp;→&ensp;[source](https://github.com/harthikrm/signal)

### <samp>03</samp>&ensp;Mylonite

<samp><sub>RESEARCH&ensp;·&ensp;NOV 2026&ensp;·&ensp;PREPRINT</sub></samp>

A test harness for races that happen through Redis or Valkey state rather than in memory. A delay-only proxy decides the order commands reach the store, a language model proposes which requests to race, and plain code decides what counts as a bug. A reported bug must replay 20 times out of 20 from its recorded schedule. In a pre-registered, held-out evaluation the model found each bug in a median of **1** execution, against **764** and **97** for the strongest non-AI baseline on the two held-out bugs. It still lost on wall-clock time, because executions are cheap. The paper reports both.

<samp><sub>Python · Valkey · RESP2/3 · 129 tests</sub></samp>&ensp;→&ensp;[source](https://github.com/harthikrm/mylonite)&ensp;·&ensp;[paper](https://www.harthik.dev/papers/mylonite_fewer_executions_more_seconds.pdf)

<br>

<samp><sub>ALSO</sub></samp>

**[Code Sentinel](https://github.com/harthikrm/code-sentinel)**&ensp;—&ensp;QLoRA fine-tune of Mistral-7B-Instruct on 144K code-review pairs, trained on an H100 on Vertex AI and served behind a GitHub Actions bot that reviews pull requests hunk by hunk.<br>
**[Let the Solver Choose Its Data](https://github.com/harthikrm/arc-prize-2026-paper)**&ensp;—&ensp;ARC Prize 2026 paper. Picks synthetic training tasks by the solver's own likelihood, and shows why held-out loss was the wrong signal for choosing a model.<br>
**[Quant Risk Desk](https://github.com/harthikrm/quant-risk-desk)**&ensp;—&ensp;Airflow → dbt → Postgres pipeline computing VaR, CVaR, drawdowns and macro-regime overlays across market sectors.

<samp><sub>WRITING</sub></samp>

[When feedback backfires](https://medium.com/@hrmallichetty/when-feedback-backfires-can-better-feedback-teach-ai-agents-to-game-the-system-5a03d05d9262) — can better feedback teach AI agents to game their graders?&ensp;<sub>Sep 2026</sub><br>
[From code review to ARC-AGI-2](https://medium.com/@hrmallichetty/from-code-review-to-arc-agi-2-reusing-the-same-ml-muscle-on-a-harder-reasoning-problem-a4be66501d3b) — reusing the same ML muscle on a harder reasoning problem.&ensp;<sub>Oct 2026</sub>

<samp><sub>BEFORE THIS</sub></samp>

Associate data engineer at Prolifics, building SQL pipelines over 250K+ engineering records and a TensorFlow sprint-risk service behind a Flask API. Before that, analytics at HeiDigi. MS in Business Analytics & AI from UT Dallas (2026, Scholar With Distinction); B.Tech from GITAM.
