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
site/methodology.html   deep dive: how each pillar is scored, benchmark by benchmark
site/fable.html         Claude Fable 5 deep dive
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
- **Fable deep dive** (`fable.html`) — how Claude Fable 5 holds up in the
  field: SWE-bench Pro lead vs. the Endor Labs reality check (solve rates,
  timeouts, contamination, hall-of-fame CVE fixes) and the cybersecurity
  safeguard architecture.
