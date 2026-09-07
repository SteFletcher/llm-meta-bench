# llm-meta-bench

**Live report: <https://stefletcher.github.io/llm-meta-bench/>**

Aggregates LLM benchmark scores across the major public leaderboards into a
single-slide scoreboard, plus focused model comparisons and Solar Bench's
same-prompt implementation assessment. Claude Opus 5 is included in both the
public benchmark board and the ten-build Solar Bench field.

Deployed to GitHub Pages by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) on
every push to `main`, plus a weekly scheduled data refresh (Mondays 06:00 UTC;
set an `AA_API_KEY` repo secret to enable the Artificial Analysis adapter).

## Layout

```
data/benchmarks.json    canonical data store (sources, models, pillars, scores, insights)
scripts/refresh_data.py refresh script — fetches sources, merges, re-injects
site/index.html         PRIMARY: Coding / Security comparison (single slide)
site/headtohead.html    Fable 5 vs Sol Pro (Extra High), pillar by pillar
site/solar-benchmark.html  Solar Bench scoring, all 10 models and 26 criteria
site/solar.html         Solar Bench top-three visual comparison
site/solar-field.html   Solar Bench intent-loss gallery
```

The primary page groups a deliberately small metric set into two pillars
(Coding: Artificial Analysis Coding Index, Terminal-Bench v2.1, SciCode ·
Security: Cybench defensive, Endor SecPass). Every score cell hyperlinks to its data
origin (`source_url` per score in the JSON).
Predecessor-model scores are shown daggered (†, `proxy` field); sourcing and
comparison caveats are explained inline.

As of the 25 July 2026 update, Claude Opus 5 leads the primary board's
Artificial Analysis Agentic Index (55.3) and Coding Index (78.0) among the
included models. It has no compatible current-generation security result, so
those cells remain N/A rather than inheriting a predecessor score.

The published pages are fully self-contained: the JSON payload is inlined into a
`<script id="benchmark-data" type="application/json">` block, so they work as
local files or hosted artifacts with no runtime fetches.

## Data sourcing per pillar

The goal is one consistent source per pillar. Artificial Analysis provides the
complete Coding view. Security remains the deliberate exception because Artificial Analysis does not publish a security capability
index and the two retained benchmarks answer genuinely different questions.
Every individual score links to its own origin, and predecessor-generation
security scores are daggered (†) with the tested model named.

- **Coding — single source (Artificial Analysis).** The headline Coding Index
  is displayed with both components: Terminal-Bench v2.1 for agentic terminal
  execution and SciCode for scientific code generation. Values are refreshed
  at each model's highest published effort and link to the matching AA page.

- **Planning — retired from the overview (2026-09-07).** Artificial Analysis
  retired the Agentic Index page, so the pillar's flagship metric is no longer
  published for any model and could never be filled for a newly released one.
  Rather than show a pillar that is permanently half-empty, the overview now
  runs on Coding and Security. GDPval-AA v2 and τ³-Banking still refresh and
  their scores are retained in `data/benchmarks.json`, so restoring the pillar
  is a matter of putting the entry back in `pillars` — but it needs a flagship
  that is still published.

- **Security — two references, by design (different questions).** Cybench
  (defensive subset, CoTool) measures offensive/analytic CTF capability; Endor
  Labs SecPass measures whether a model's *generated code is secure*. These are
  genuinely different security questions and no single site covers both, so
  both are cited. Current-generation coverage is thin — Cybench cells are
  daggered predecessor proxies and Endor has only run Fable 5 — because the
  frontier labs and benchmark authors haven't published current-model runs.

**Why Security still has N/A cells:** Cybench was run on predecessor
generations and Endor has tested only one current model. An N/A means "not
publicly measured," not a zero.

## Refreshing the data

```sh
python3 scripts/refresh_data.py            # fetch + merge + inject
python3 scripts/refresh_data.py --offline  # re-inject after hand-editing the JSON
python3 scripts/refresh_data.py --dry-run  # fetch and report, write nothing
python3 scripts/refresh_data.py --only swebench,lmarena
```

- Set `AA_API_KEY` to enable the Artificial Analysis adapter.
- LMArena, SWE-bench, and LiveBench adapters scrape/fetch public endpoints and
  will need occasional maintenance as those sites change.
- Endor Labs and the retained Cybench security study have no stable
  machine-readable feed — update `data/benchmarks.json` by hand and re-run with
  `--offline`.
- Any adapter failure keeps the last known-good values and marks the source
  `stale` (rendered as a dashed chip on the slide footer).

## Pages

- **Primary comparison** (`index.html`) — two headline charts, a compact
  sortable matrix of five key metrics, and focused interpretation on the right
  rail. Every score is a hyperlink to its origin.
- **Head to head** (`headtohead.html`) — Claude Fable 5 vs GPT-5.6 Sol Pro
  (xhigh / "Ultra") scored pillar by pillar, including Planning, which the
  overview no longer carries. Coding is the only pillar with real two-sided
  data (it splits); Planning and Security are largely N/A for both current
  models, which is the honest headline. Every present score
  links to its origin.
- **Solar Bench** (`solar-benchmark.html`) — ten implementations of one
  identical simulator brief, scored on 16 required delivery criteria and ten
  implicit-intent probes. Claude Opus 5 leads at 9.3/10 after passing 58 unit
  and 44 production browser tests.
- **Solar top three** (`solar.html`) — the current Opus 5, Fable 5 and Kimi K3
  cohort compared through Earth captures, criterion scores and implementation
  trade-offs.
- **Intent-loss gallery** (`solar-field.html`) — all ten Earth outcomes,
  evidence provenance and implicit-intent scores.
