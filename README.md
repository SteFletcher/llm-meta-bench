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

The primary page groups benchmarks into three pillars (Planning: Tau2,
Vending-Bench 2, GAIA, ARC-AGI-2 · Security: Cybench defensive, Endor SecPass ·
Coding: SWE-bench Pro/Verified, Terminal-Bench, LiveCodeBench). Every score
cell hyperlinks to its data origin (`source_url` per score in the JSON).
Predecessor-model scores are shown daggered (†, `proxy` field) and no blended
composite is published — the methodology page explains why.

Both pages are fully self-contained: the JSON payload is inlined into a
`<script id="benchmark-data" type="application/json">` block, so they work as
local files or hosted artifacts with no runtime fetches.

## Data sourcing per pillar

The goal is one consistent source per pillar. That's fully achievable for
Coding but only partly for Planning and Security, because the specialized
benchmarks are each hosted by their own author and — more fundamentally —
**most current-generation frontier models have never been run on them.** Where
a single source can't cover a pillar, we use the minimum number of references
and explain each here. Every individual score still links to its own origin,
and predecessor-generation scores are daggered (†) with the tested model named.

- **Coding — single source (Artificial Analysis API).** Terminal-Bench (the
  flagship), plus GPQA/HLE/intelligence-index, are pulled per-model from the AA
  API at each model's highest published effort. SWE-bench Pro/Verified are not
  AA evals, so they stay on their original leaderboards (SWE-bench is not on
  AA). LiveCodeBench is intentionally left as-is: AA returns no LiveCodeBench
  value for our model set (it publishes a coding *index* instead).

- **Planning — one API + one aggregator + one harness board (3 refs, by
  necessity).** Tau2 comes from the AA API (same authoritative source as
  Coding). Vending-Bench 2 and ARC-AGI-2 are consolidated onto **llm-stats.com**,
  a single aggregator that hosts both specialized boards in one place (rather
  than citing Andon Labs and ARC Prize separately). GAIA stays on **Princeton
  HAL**, because GAIA scores are only meaningful inside a named agent scaffold —
  a HAL number and a bare-model number aren't the same measurement, so it can't
  be honestly folded into the aggregator. Vending-Bench and GAIA remain sparse
  and mostly daggered: only predecessor models have been evaluated on them.

- **Security — two references, by design (different questions).** Cybench
  (defensive subset, CoTool) measures offensive/analytic CTF capability; Endor
  Labs SecPass measures whether a model's *generated code is secure*. These are
  genuinely different security questions and no single site covers both, so
  both are cited. Current-generation coverage is thin — Cybench cells are
  daggered predecessor proxies and Endor has only run Fable 5 — because the
  frontier labs and benchmark authors haven't published current-model runs.

**Why so many N/A cells remain:** they are not gaps we can close by finding a
better site. Vending-Bench 2 (4 models ever), GAIA, and Cybench were run on
predecessor generations; Endor has tested one model; and several labs (OpenAI
for GPT-5.6, xAI for Grok 4.5, Anthropic for Fable 5) did not publish ARC-AGI-2
at launch. An N/A here means "not publicly measured anywhere," which is itself
the finding the Planning/Security pillars exist to surface.

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
- Terminal-Bench, HLE, and the Endor Labs study have no machine-readable feed —
  update `data/benchmarks.json` by hand and re-run with `--offline`.
- Any adapter failure keeps the last known-good values and marks the source
  `stale` (rendered as a dashed chip on the slide footer).

## Pages

- **Primary comparison** (`index.html`) — three flagship pillar charts, the
  full linked matrix (every score is a hyperlink to its origin), and insight
  callouts on the right rail. `→` / `Space` advances to the methodology.
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
