# llm-meta-bench

**Live report: <https://stefletcher.github.io/llm-meta-bench/>**

Aggregates LLM benchmark scores across the major public leaderboards into a
single-slide scoreboard, plus a deep-dive page on Claude Fable 5's real-world
performance in cybersecurity and software engineering.

Deployed to GitHub Pages by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) on
every push to `main`, plus a weekly scheduled data refresh (Mondays 06:00 UTC;
set an `AA_API_KEY` repo secret to enable the Artificial Analysis adapter).

## Layout

```
data/benchmarks.json    canonical data store (sources, models, pillars, scores, insights)
scripts/refresh_data.py refresh script — fetches sources, merges, re-injects
site/index.html         PRIMARY: Planning / Security / Coding comparison (single slide)
site/methodology.html   how each pillar is scored, benchmark by benchmark
site/headtohead.html    Fable 5 vs Sol Pro (Extra High) across the 3 pillars
site/underworld.html    risk assessment: uncensored open-weight LLMs vs frontier attack capability
```

The primary page groups a deliberately small metric set into three pillars
(Planning: Artificial Analysis Agentic Index, GDPval-AA v2, τ³-Banking ·
Security: Cybench defensive, Endor SecPass · Coding: Artificial Analysis Coding
Index, Terminal-Bench v2.1, SciCode). Every score cell hyperlinks to its data
origin (`source_url` per score in the JSON).
Predecessor-model scores are shown daggered (†, `proxy` field) and no blended
composite is published — the methodology page explains why.

Both pages are fully self-contained: the JSON payload is inlined into a
`<script id="benchmark-data" type="application/json">` block, so they work as
local files or hosted artifacts with no runtime fetches.

## Data sourcing per pillar

The goal is one consistent source per pillar. Artificial Analysis now provides
the complete Planning and Coding views. Security remains the deliberate
exception because Artificial Analysis does not publish a security capability
index and the two retained benchmarks answer genuinely different questions.
Every individual score links to its own origin, and predecessor-generation
security scores are daggered (†) with the tested model named.

- **Coding — single source (Artificial Analysis).** The headline Coding Index
  is displayed with both components: Terminal-Bench v2.1 for agentic terminal
  execution and SciCode for scientific code generation. Values are refreshed
  at each model's highest published effort and link to the matching AA page.

- **Planning — single source (Artificial Analysis).** The headline Agentic
  Index is displayed with both equal-weighted components: GDPval-AA v2 for
  real-world knowledge-work deliverables and τ³-Banking for multi-step tool use
  over a large policy knowledge base.

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

- **Primary comparison** (`index.html`) — three headline charts, a compact
  sortable matrix of eight key metrics, and focused interpretation on the right
  rail. Every score is a hyperlink to its origin. `→` / `Space` advances to the
  methodology.
- **Methodology** (`methodology.html`) — the four comparison rules, then each
  benchmark per pillar: what it measures, how it scores, current data, caveats.
  `←` returns to the comparison.
- **Head to head** (`headtohead.html`) — Claude Fable 5 vs GPT-5.6 Sol Pro
  (xhigh / "Ultra") scored across all three pillars. Coding is the only pillar
  with real two-sided data (it splits); Planning and Security are largely N/A
  for both current models, which is the honest headline. Every present score
  links to its origin.
- **Uncensored underworld** (`underworld.html`) — risk assessment: with
  abliteration now a one-command job, can uncensored open-weight models attack
  like a frontier model? Two 2026 studies (TrustedSec's 4,800-run field
  benchmark; OpenAI's worst-case weaponization of gpt-oss) converge: reliable
  single-step exploit validation with zero refusals, but 0% on multi-step
  chains — the frontier gap is long-horizon execution, not knowledge. Includes
  a defender's control set.
