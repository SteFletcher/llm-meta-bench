#!/usr/bin/env python3
"""Refresh llm-meta-bench data.

Pulls the latest scores from each upstream leaderboard (best-effort — these
sites change markup and APIs frequently), merges them into
data/benchmarks.json, and re-injects the JSON payload into the two site pages
so they stay self-contained (the pages read an inline
<script type="application/json"> block, no runtime fetches).

Usage:
    python3 scripts/refresh_data.py              # fetch + merge + inject
    python3 scripts/refresh_data.py --offline    # skip fetching, re-inject only
    python3 scripts/refresh_data.py --dry-run    # fetch, report, write nothing

Environment:
    AA_API_KEY   Artificial Analysis API key (enables the AA adapter).

Any adapter that fails leaves existing values untouched and marks the source
stale — the site always renders the last known-good data.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "benchmarks.json"
SITE_PAGES = [
    ROOT / "site" / "index.html",
    ROOT / "site" / "methodology.html",
    ROOT / "site" / "headtohead.html",
    ROOT / "site" / "underworld.html",
]

UA = "llm-meta-bench/1.0 (+data refresh script)"
TIMEOUT = 30

# Map upstream display names to our canonical model ids.
MODEL_ALIASES = {
    "claude mythos 5": "mythos-5",
    "claude fable 5": "fable-5",
    "claude-fable-5": "fable-5",
    "claude opus 4.8": "opus-4-8",
    "claude-opus-4-8": "opus-4-8",
    "claude sonnet 5": "sonnet-5",
    "claude-sonnet-5": "sonnet-5",
    "gpt-5.6 sol": "gpt-5-6-sol",
    "gpt-5.6 terra": "gpt-5-6-terra",
    "gpt-5.5": "gpt-5-5",
    "gpt-5.5 pro": "gpt-5-5",
    "gemini 3.1 pro": "gemini-3-1-pro",
    "grok 4.5": "grok-4-5",
    "deepseek v4 pro": "deepseek-v4-pro",
    "glm-5.2": "glm-5-2",
    "kimi k2.5": "kimi-k2-5",
    "kimi k3": "kimi-k3",
}


def log(msg: str) -> None:
    print(f"[refresh] {msg}", file=sys.stderr)


def fetch(url: str, headers: dict | None = None) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def canonical_model(name: str) -> str | None:
    return MODEL_ALIASES.get(name.strip().lower())


def set_score(data: dict, model: str, benchmark: str, value: float, note: str | None = None) -> None:
    for row in data["scores"]:
        if row["model"] == model and row["benchmark"] == benchmark:
            row["value"] = value
            if note:
                row["note"] = note
            return
    row = {"model": model, "benchmark": benchmark, "value": value}
    if note:
        row["note"] = note
    data["scores"].append(row)


# --------------------------------------------------------------------------
# Adapters — each returns the number of scores it updated, or raises.
# --------------------------------------------------------------------------

# Benchmarks sourced from the Artificial Analysis API — our benchmark id ->
# (AA `evaluations` field name, citation URL). AA is the single source of truth
# for every benchmark listed here: a keyed refresh overwrites those cells from
# one place. The AA leaderboard *page* renders its table in JavaScript (an
# automated page-fetch sees only the top line), but the *API* returns raw
# per-model numbers. Scoped to Tau2 for now; add rows (gpqa, hle, livecodebench,
# terminalbench_v2_1, artificial_analysis_intelligence_index) to single-source
# more benchmarks from AA.
AA_MODELS_URL = "https://artificialanalysis.ai/leaderboards/models"
AA_EVAL_MAP = {
    "tau2-bench": ("tau2", "https://artificialanalysis.ai/evaluations/tau2-bench"),
    "terminal-bench": ("terminalbench_v2_1", AA_MODELS_URL),
    "aa-index": ("artificial_analysis_intelligence_index", AA_MODELS_URL),
    "gpqa-diamond": ("gpqa", AA_MODELS_URL),
    "hle": ("hle", AA_MODELS_URL),
}
# Note: livecodebench is intentionally absent — AA returns no LiveCodeBench
# value for any model in our set (it publishes a coding *index* instead), so
# mapping it would only null the one figure we do have. SWE-bench, Cybench,
# Endor, Vending-Bench, GAIA, ARC-AGI-2 and LMArena are not AA evals at all.

# AA lists each model at several reasoning-effort tiers with different scores.
# We compare models at their strongest published configuration, so we pick the
# highest-effort variant that actually carries the eval. Ranked best-first.
AA_EFFORT_ORDER = ["max", "xhigh", "x-high", "high", "medium", "low", "minimal", "default", "non-reasoning", "none"]


def _aa_effort_rank(name: str) -> int:
    # Variants with no recognized effort suffix (e.g. a bare "(Reasoning)")
    # rank as "default": above non-reasoning/none, below the explicit tiers.
    n = name.lower()
    for i, kw in enumerate(AA_EFFORT_ORDER):
        if kw != "default" and kw in n:
            return i
    return AA_EFFORT_ORDER.index("default")


def _aa_effort_label(name: str) -> str:
    n = name.lower()
    for kw in AA_EFFORT_ORDER:
        if kw in n:
            return kw
    return "default"


def _aa_model_id(name: str) -> str | None:
    """Map an AA model name (which carries effort/variant suffixes, e.g.
    'Claude Opus 4.8 (Adaptive Reasoning, Max Effort)') to our canonical id."""
    base = re.sub(r"\(.*?\)", "", name).strip().lower()
    base = re.sub(r"\s+", " ", base)
    for alias in sorted(MODEL_ALIASES, key=len, reverse=True):  # longest first
        if base == alias or base.startswith(alias + " "):
            return MODEL_ALIASES[alias]
    return None


def refresh_artificial_analysis(data: dict) -> int:
    """Pull every AA_EVAL_MAP benchmark per model from the AA API. Requires AA_API_KEY."""
    key = os.environ.get("AA_API_KEY")
    if not key:
        raise RuntimeError("AA_API_KEY not set — skipping (get one at artificialanalysis.ai)")
    body = fetch(
        "https://artificialanalysis.ai/api/v2/data/llms/models",
        headers={"x-api-key": key},
    )
    payload = json.loads(body)

    # group AA's per-effort variants under our canonical model ids
    groups: dict[str, list] = {}
    for entry in payload.get("data", []):
        mid = _aa_model_id(entry.get("name", ""))
        if mid:
            groups.setdefault(mid, []).append(entry)

    updated = 0
    for mid, variants in groups.items():
        for bench_id, (field, url) in AA_EVAL_MAP.items():
            have = [v for v in variants if (v.get("evaluations") or {}).get(field) is not None]
            if not have:
                continue
            best = min(have, key=lambda v: _aa_effort_rank(v["name"]))
            raw = float(best["evaluations"][field])
            if raw <= 1.0:  # AA reports pass-rate evals (tau2) as 0–1 fractions
                raw *= 100.0
            note = f"Artificial Analysis API; highest-effort published variant ({_aa_effort_label(best['name'])})."
            set_score(data, mid, bench_id, round(raw, 1), note=note)
            for row in data["scores"]:  # pin citation to AA, drop any proxy flag
                if row["model"] == mid and row["benchmark"] == bench_id:
                    row["source_url"] = url
                    row.pop("proxy", None)
                    break
            updated += 1
    return updated


def refresh_lmarena(data: dict) -> int:
    """Scrape the arena text leaderboard. Markup changes often; parse both the
    embedded Next.js payload and a plain-table fallback."""
    html = fetch("https://arena.ai/leaderboard/text")
    updated = 0
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if m:
        try:
            payload = json.loads(m.group(1))
            rows = _find_leaderboard_rows(payload)
            for row in rows:
                model_id = canonical_model(str(row.get("model", row.get("name", ""))))
                elo = row.get("rating", row.get("elo", row.get("score")))
                if model_id and elo:
                    set_score(data, model_id, "lmarena-elo", round(float(elo)))
                    updated += 1
        except (json.JSONDecodeError, TypeError):
            pass
    if not updated:
        # crude fallback: "Model Name ... 1510" table rows
        for name, alias in MODEL_ALIASES.items():
            pat = re.escape(name) + r"[^0-9]{0,80}(1[45]\d{2})"
            hit = re.search(pat, html, re.I)
            if hit:
                set_score(data, alias, "lmarena-elo", int(hit.group(1)))
                updated += 1
    if not updated:
        raise RuntimeError("no recognizable models found in page")
    return updated


def _find_leaderboard_rows(node):
    """Walk arbitrary JSON looking for a list of dicts with model+rating keys."""
    if isinstance(node, list):
        if node and isinstance(node[0], dict) and (
            {"model", "rating"} <= node[0].keys() or {"name", "elo"} <= node[0].keys()
        ):
            return node
        for item in node:
            found = _find_leaderboard_rows(item)
            if found:
                return found
    elif isinstance(node, dict):
        for value in node.values():
            found = _find_leaderboard_rows(value)
            if found:
                return found
    return []


def refresh_swebench(data: dict) -> int:
    """SWE-bench publishes leaderboard JSON in its website repo."""
    body = fetch(
        "https://raw.githubusercontent.com/swe-bench/swe-bench.github.io/main/data/leaderboards.json"
    )
    payload = json.loads(body)
    updated = 0
    boards = payload if isinstance(payload, list) else payload.get("leaderboards", [])
    for board in boards:
        name = str(board.get("name", "")).lower()
        if "verified" in name:
            bench = "swe-verified"
        elif "pro" in name:
            bench = "swe-pro"
        else:
            continue
        for entry in board.get("results", []):
            model_id = canonical_model(str(entry.get("name", "")))
            resolved = entry.get("resolved", entry.get("score"))
            if model_id and resolved is not None:
                set_score(data, model_id, bench, round(float(resolved), 1))
                updated += 1
    if not updated:
        raise RuntimeError("no recognizable models in leaderboard JSON")
    return updated


def refresh_livebench(data: dict) -> int:
    """LiveBench ships per-release CSVs; grab the ground-truth judgement CSV
    from the HF-hosted mirror the site itself reads."""
    html = fetch("https://livebench.ai/")
    hit = re.search(r'(https://[^"\']*livebench[^"\']*\.csv)', html)
    if not hit:
        raise RuntimeError("no CSV link found on livebench.ai")
    csv_body = fetch(hit.group(1))
    updated = 0
    lines = csv_body.strip().splitlines()
    header = [h.strip().lower() for h in lines[0].split(",")]
    try:
        model_col = header.index("model")
        avg_col = next(i for i, h in enumerate(header) if "average" in h or "global" in h)
    except (ValueError, StopIteration):
        raise RuntimeError("unexpected CSV header: " + ",".join(header))
    for line in lines[1:]:
        cells = line.split(",")
        if len(cells) <= max(model_col, avg_col):
            continue
        model_id = canonical_model(cells[model_col])
        if model_id:
            set_score(data, model_id, "livebench-avg", round(float(cells[avg_col]), 1))
            updated += 1
    if not updated:
        raise RuntimeError("no recognizable models in CSV")
    return updated


# Manual-only sources: Terminal-Bench, HLE, and the Endor Labs study have no
# stable machine-readable feed. Update data/benchmarks.json by hand and re-run
# with --offline to re-inject.
ADAPTERS = {
    "artificial-analysis": refresh_artificial_analysis,
    "lmarena": refresh_lmarena,
    "swebench": refresh_swebench,
    "livebench": refresh_livebench,
}


# --------------------------------------------------------------------------
# Injection — keep the site pages self-contained.
# --------------------------------------------------------------------------

INJECT_RE = re.compile(
    r'(<script id="benchmark-data" type="application/json">)(.*?)(</script>)', re.S
)


def inject(pages: list[Path], data: dict) -> None:
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> inside a JSON string would terminate the block early
    blob = blob.replace("</", "<\\/")
    for page in pages:
        if not page.exists():
            log(f"skip inject: {page} not found")
            continue
        html = page.read_text(encoding="utf-8")
        new_html, count = INJECT_RE.subn(rf"\g<1>{blob}\g<3>", html)
        if count == 0:
            log(f"skip inject: no benchmark-data block in {page.name}")
            continue
        page.write_text(new_html, encoding="utf-8")
        log(f"injected data into {page.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="skip fetching; re-inject only")
    parser.add_argument("--dry-run", action="store_true", help="fetch and report, write nothing")
    parser.add_argument("--only", help="comma-separated source ids to refresh")
    args = parser.parse_args()

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    if not args.offline:
        wanted = set(args.only.split(",")) if args.only else set(ADAPTERS)
        for source_id, adapter in ADAPTERS.items():
            if source_id not in wanted:
                continue
            source = next((s for s in data["sources"] if s["id"] == source_id), None)
            try:
                n = adapter(data)
                log(f"{source_id}: updated {n} scores")
                if source is not None:
                    source["last_fetched"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    source.pop("stale", None)
            except Exception as exc:  # noqa: BLE001 — any failure means "keep old data"
                log(f"{source_id}: FAILED ({exc}) — keeping existing values")
                if source is not None:
                    source["stale"] = True
        data["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if args.dry_run:
        log("dry run — nothing written")
        return 0

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"wrote {DATA_FILE.relative_to(ROOT)}")
    inject(SITE_PAGES, data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
