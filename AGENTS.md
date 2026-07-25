# llm-meta-bench Agent Instructions

This project aggregates LLM benchmark scores across major public leaderboards into a single comprehensive scoreboard.

## Project Overview

The llm-meta-bench project provides a unified view of LLM performance across three main domains:
- **Planning**: Tau2-bench, Vending-Bench 2, GAIA, ARC-AGI-2
- **Security**: Cybench defensive and Endor SecPass
- **Coding**: SWE-bench Pro/Verified, Terminal-Bench, LiveCodeBench

## Key Files and Structure

```
data/benchmarks.json     # Canonical data store (sources, models, pillars, scores, insights)
scripts/refresh_data.py  # Refresh script — fetches sources, merges, re-injects
site/index.html          # PRIMARY: Planning / Security / Coding comparison (single slide)
site/methodology.html    # How each pillar is scored, benchmark by benchmark
site/headtohead.html     # Fable 5 vs Sol Pro (Extra High) across the 3 pillars
site/underworld.html     # Risk assessment: uncensored open-weight LLMs vs frontier attack capability
```

## Data Structure

The core data is stored in `data/benchmarks.json` which contains:
- **Sources**: Benchmark providers with their URLs and methods
- **Vendors**: Model creators (Anthropic, OpenAI, Google, etc.)
- **Models**: Specific LLMs being compared with vendor affiliations
- **Pillars**: The three main categories (Planning, Security, Coding)
- **Benchmarks**: Individual tests within each pillar
- **Scores**: Actual performance data with source URLs and notes

## Workflow

### Refreshing Data
```sh
python3 scripts/refresh_data.py              # fetch + merge + inject
python3 scripts/refresh_data.py --offline    # re-inject after hand-editing the JSON
python3 scripts/refresh_data.py --dry-run    # fetch and report, write nothing
python3 scripts/refresh_data.py --only swebench,lmarena
```

### Environment Variables
- `AA_API_KEY` - Set to enable the Artificial Analysis adapter

## Key Features

- **Self-contained pages**: All HTML files include the JSON data inline, so they work as local files or hosted artifacts with no runtime fetches
- **Automated refresh**: Scheduled weekly updates (Mondays at 06:00 UTC) plus manual triggers
- **Data reliability**: Failed adapters keep last known-good values and mark sources as stale
- **Transparency**: Each score links to its data origin, and predecessor model scores are shown with daggered notation

## Documentation

- [Methodology](site/methodology.html) - Detailed explanation of how benchmarks are scored
- [Head-to-Head Comparison](site/headtohead.html) - Claude Fable 5 vs GPT-5.6 Sol Pro
- [Underworld Risk Assessment](site/underworld.html) - Risk assessment of uncensored models

## Development Notes

The project is designed to be fully self-contained, making it easy to work with locally. The refresh script handles fetching data from various sources and merging them into the canonical JSON file.

### Adapter Types
- **auto**: Automatically fetches data from APIs or web scraping
- **auto-with-key**: Requires API key for access (e.g., Artificial Analysis)
- **manual**: Data must be entered by hand

### Key Adapters
- Artificial Analysis API (requires AA_API_KEY)
- LMArena (Chatbot Arena) - Crowd-sourced pairwise Elo
- SWE-bench Verified/Pro - Human-reviewed GitHub issues
- Terminal-Bench 2.1 - Agentic terminal task benchmark
- LiveBench/LiveCodeBench - Contamination-resistant rolling releases
- Humanity's Last Exam (Scale/CAIS) - Frontier academic knowledge
- Endor Labs Agent Security League - Real-world vulnerability-fix tasks
- Tau2-bench (Sierra, via Artificial Analysis) - Multi-turn tool-use agents
- Vending-Bench 2 (Andon Labs) - Simulated year running a vending business
- GAIA (Princeton HAL) - General assistant tasks in the HAL scaffold
- Cybench defensive subset (CoTool) - Defensive tasks from professional CTF challenges

## Implementation Details

The refresh script (`scripts/refresh_data.py`) is designed to be robust:
- It handles failures gracefully by keeping last known-good values and marking sources as stale
- It supports multiple modes: fetch + merge + inject, offline re-injection, and dry-run
- It uses a mapping system for model aliases to ensure consistent naming across different sources
- It includes proper error handling and logging throughout the process

## Website Pages

All HTML pages are designed to be self-contained:
- `index.html`: Main comparison page showing the three pillars (Planning, Security, Coding)
- `methodology.html`: Detailed explanation of how each benchmark is scored
- `headtohead.html`: Head-to-head comparison between Claude Fable 5 and GPT-5.6 Sol Pro
- `underworld.html`: Risk assessment of uncensored open-weight LLMs vs frontier attack capability

Each page includes the JSON data inline in a `<script id="benchmark-data" type="application/json">` block, making them work as local files or hosted artifacts with no runtime fetches.