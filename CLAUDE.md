# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, data-driven report aggregating LLM benchmark scores across three pillars — **Planning**, **Security**, **Coding** — for a fixed set of ~12 frontier models. It is four self-contained HTML pages plus a Python refresh script, deployed to GitHub Pages. There is no build step, no framework, no dependencies beyond the Python standard library.

Live site: <https://stefletcher.github.io/llm-meta-bench/>

## The one architectural rule that governs everything

**`data/benchmarks.json` is the single source of truth. The HTML pages are self-contained snapshots of it.** Each page in `site/` carries the entire dataset inlined in a `<script id="benchmark-data" type="application/json">…</script>` block and renders it client-side with vanilla JS — no runtime fetches, so the pages work as local files or hosted artifacts.

Because of this, **never hand-edit the JSON inside an HTML file.** The workflow is always:

1. Edit `data/benchmarks.json`.
2. Run `python3 scripts/refresh_data.py --offline` — this re-injects the JSON into all four pages via a regex on the `benchmark-data` anchor (`INJECT_RE` in the script).
3. Then commit both the JSON and the regenerated HTML.

Editing a page's inlined JSON directly will be silently overwritten on the next refresh, and the pages will disagree with each other. If you change page *markup/logic* (not data), edit the HTML and still run `--offline` afterward so the data block stays current.

## Common commands

```sh
# Re-inject data into all pages after editing the JSON (the usual command)
python3 scripts/refresh_data.py --offline

# Full refresh: run every fetch adapter, merge, re-inject, bump generated_at
python3 scripts/refresh_data.py

# Refresh a single source (adapter ids: artificial-analysis, lmarena, swebench, livebench)
python3 scripts/refresh_data.py --only artificial-analysis

# Fetch + report what would change, write nothing
python3 scripts/refresh_data.py --dry-run

# Validate the data file (there is no test suite; this is the integrity check)
python3 -c "import json; json.load(open('data/benchmarks.json')); print('valid')"

# Local preview
python3 -m http.server 8000 --directory site   # then open http://localhost:8000/
```

Deploy is automatic: pushing to `main` triggers `.github/workflows/deploy-pages.yml`, which runs the `--offline` re-inject and publishes `site/` to Pages. A weekly cron (Mon 06:00 UTC) and manual `workflow_dispatch` additionally run the full fetch first (the fetch step is gated to non-`push` events).

## Data model (`data/benchmarks.json`)

Understanding this relational shape is prerequisite to any data change:

- **`models`** — the fixed comparison set; each has an `id`, display `name`, and `vendor`.
- **`vendors`** — model creators; drive the per-vendor chart colors.
- **`benchmarks`** — individual tests; each has an `id`, `unit` (`%`, `$`, `elo`, `index`), and a fallback `url`.
- **`pillars`** — the three groups; each lists its member benchmark ids and a `flagship` benchmark (the one charted on the primary page).
- **`scores`** — the cells: `{model, benchmark, value, source_url, note?, proxy?}`. This is what you edit most.
- **`head_to_head`** and **`risk`** — bespoke datasets consumed only by `headtohead.html` and `underworld.html` respectively (not part of the pillar/matrix structure).

### Load-bearing conventions on scores (enforced editorially across all pages)

- **Every score links to its origin.** `source_url` is mandatory; the pages render each value as a hyperlink to it. If you can't cite it, don't add it.
- **`proxy` marks a predecessor-model score.** When only an older generation was tested (e.g. Opus 4.6 standing in for Opus 4.8), set `proxy` to the tested model's name. The pages render these daggered (†). Do not silently attribute an old score to a current model.
- **N/A means "not measured anywhere,"** not "we didn't look." Leaving a cell absent is a deliberate, honest signal — especially in Planning/Security, where current-gen models often have no published data on any site.
- **No blended composite score exists, by design.** Models are tested on different subsets, so ranking happens only within a benchmark. Do not add an "overall" number.

## The refresh adapters (`scripts/refresh_data.py`)

`ADAPTERS` maps a source id to a function `fn(data) -> int` (count of updated cells). Each adapter mutates `data["scores"]` in place via `set_score(...)`. **Failures are swallowed per-adapter**: on exception the source is marked `stale` (rendered as a dashed chip in the UI) and last-known-good values are kept — so a single broken scraper never blanks the report.

**Artificial Analysis is the primary, preferred source.** It is the only adapter that pulls many benchmarks from one authoritative API. Key mechanics:

- `AA_EVAL_MAP` maps our benchmark id → the AA `evaluations` field name. To source a new benchmark from AA, add a row here — that's the whole change.
- AA lists each model at multiple reasoning-effort tiers (names carry suffixes like `Claude Opus 4.8 (Adaptive Reasoning, Max Effort)` or `GPT-5.6 Sol (xhigh)`). `_aa_model_id` strips the suffix to match our canonical id; the adapter then picks the **highest-effort variant** (`AA_EFFORT_ORDER`) that actually carries the eval.
- AA pass-rate evals come back as 0–1 fractions and are normalized to percent.
- Only benchmarks AA actually publishes for our set belong in the map. LiveCodeBench is deliberately excluded (AA returns none for our models); SWE-bench, Cybench, Endor, Vending-Bench, GAIA, ARC-AGI-2 and LMArena are not AA evals at all.

**Model name matching:** `MODEL_ALIASES` maps upstream display names → our canonical model ids; `canonical_model()` is the entry point for the non-AA adapters, `_aa_model_id()` for AA (which additionally handles effort suffixes).

**Manual-only sources:** Terminal-Bench blogs, Cybench, Vending-Bench, GAIA, ARC-AGI-2, Endor, and llm-stats aggregations have no machine feed. Their JS-rendered leaderboards can't be scraped, so those scores are hand-entered in the JSON with per-cell `source_url`s and refreshed with `--offline`.

## Sourcing strategy (why some pillars use multiple sites)

The goal is one consistent source per pillar; the README's "Data sourcing per pillar" section is the authoritative writeup, but in short:

- **Coding** is single-sourced from the AA API for Terminal-Bench (the flagship); SWE-bench stays on its own leaderboards (not an AA eval).
- **Planning** uses three sources by necessity: Tau2 (AA API), Vending-Bench 2 + ARC-AGI-2 (consolidated onto llm-stats.com), and GAIA (Princeton HAL — its scores are only meaningful inside a named scaffold and can't be pooled).
- **Security** intentionally uses two references answering different questions: Cybench (capability) and Endor SecPass (whether generated code is secure). No single site covers both.

When adding or moving data, preserve this per-pillar consistency and update the rationale in `README.md` if the source set changes.

## Secrets

`.env` (gitignored — this is a **public** repo) holds the AA token as `artificial_intelligence_token`. The refresh script reads the key from the `AA_API_KEY` environment variable, so export it from `.env` before a keyed run:

```sh
set -a; . ./.env; set +a; export AA_API_KEY="$artificial_intelligence_token"
python3 scripts/refresh_data.py --only artificial-analysis
```

In CI the same value lives in the `AA_API_KEY` GitHub Actions secret. Never commit `.env` or echo the token into files.
