<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/masthead-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/masthead-light.svg">
  <img src="assets/masthead-light.svg" width="100%" alt="Harthik Mallichetty — Data and AI engineer, Dallas, Texas. Building Room.">
</picture>

I build AI systems end to end, from ingestion jobs and warehouses to evaluations and the product people actually use. Right now I'm building [Room](https://joinaroom.app).

<samp>Dallas, TX&nbsp;·&ensp;<a href="https://www.harthik.dev">harthik.dev</a>&nbsp;·&ensp;<a href="https://www.linkedin.com/in/harthikmallichetty">LinkedIn</a>&nbsp;·&ensp;<a href="mailto:hrmallichetty@gmail.com">Email</a></samp>

<br>

### <samp>01</samp>&ensp;Room

<samp><sub>FOUNDER&ensp;·&ensp;SINCE 2026&ensp;·&ensp;PRIVATE EARLY ACCESS</sub></samp>

GPT, Claude and Gemini answer side by side in one project, each reading from a shared project memory. Decisions and constraints are proposed from the conversation, only the ones you confirm are kept, and each links back to the message it came from.

<samp>Next.js · TypeScript · PostgreSQL · Supabase · OpenRouter&ensp;→&ensp;<a href="https://joinaroom.app">joinaroom.app</a></samp>

### <samp>02</samp>&ensp;Signal

<samp><sub>FINANCIAL RESEARCH&ensp;·&ensp;2026&ensp;·&ensp;END TO END</sub></samp>

Ask about a company; get an answer cited to its filings. Airflow pulls SEC XBRL facts, filing text and prices for 70 companies, dbt models them through tested staging and mart layers, and filings are embedded into pgvector. On top sit a cited RAG chat and a LangGraph agent that plans, calls six data tools, checks its answer and replans.

<samp>Python · Airflow · dbt · pgvector · LangGraph · FastAPI · GCP&ensp;→&ensp;<a href="https://github.com/harthikrm/signal">source</a></samp>

### <samp>03</samp>&ensp;Mylonite

<samp><sub>RESEARCH&ensp;·&ensp;NOV 2026&ensp;·&ensp;PREPRINT</sub></samp>

A test harness for races that happen through Redis or Valkey state, not in memory. A delay-only proxy controls the order commands reach the store, a language model proposes which requests to race, and plain code decides what counts as a bug; every report must replay 20 times out of 20. In a pre-registered evaluation on two held-out bugs, the model, given the service's source, needed a median of **1** execution for each, against **764** and **97** for the strongest non-AI baseline. Without the source it was no better than search, and it lost on wall-clock time and dollars, because executions are cheap. The paper reports all of it.

<samp>Python · Valkey · RESP · 129 tests&ensp;→&ensp;<a href="https://github.com/harthikrm/mylonite">source</a> · <a href="https://www.harthik.dev/papers/mylonite_fewer_executions_more_seconds.pdf">paper</a></samp>

<br>

<samp><sub>ALSO</sub></samp>

**[Code Sentinel](https://github.com/harthikrm/code-sentinel)**&ensp;—&ensp;QLoRA fine-tune of Mistral-7B-Instruct on 143K code-review pairs, trained on an H100 on Vertex AI, with a GitHub Actions bot that sent each diff hunk to the model for review.<br>
**[Let the Solver Choose Its Data](https://github.com/harthikrm/arc-prize-2026-paper)**&ensp;—&ensp;ARC Prize 2026 Paper Track submission. Selects synthetic tasks for continued training of the NVARC solver by that solver's own likelihood, and argues from its runs that held-out loss was the wrong signal for choosing a checkpoint.<br>
**[Quant Risk Desk](https://github.com/harthikrm/quant-risk-desk)**&ensp;—&ensp;Airflow-orchestrated ingest into Postgres, with dbt models computing VaR, CVaR, drawdowns and macro-regime overlays across 11 sectors.

<samp><sub>WRITING</sub></samp>

[When feedback backfires](https://medium.com/@hrmallichetty/when-feedback-backfires-can-better-feedback-teach-ai-agents-to-game-the-system-5a03d05d9262): can better feedback teach AI agents to game their graders?&ensp;<sub>Sep 2026</sub><br>
[From code review to ARC-AGI-2](https://medium.com/@hrmallichetty/from-code-review-to-arc-agi-2-reusing-the-same-ml-muscle-on-a-harder-reasoning-problem-a4be66501d3b): reusing the same ML muscle on a harder reasoning problem.&ensp;<sub>Oct 2026</sub>

<samp><sub>BEFORE THIS</sub></samp>

Associate data engineer at Prolifics, building SQL pipelines over 250K+ engineering records and a TensorFlow sprint-risk service behind a Flask API. Before that, a data-analyst internship at HeiDigi. MS in Business Analytics & AI, UT Dallas, 2026; B.Tech, GITAM.
