# Solar Bench post-run calibration — 2026-07-25

This review follows the frozen-score addition of Claude Opus 5. It does not
change the rubric, skill or any score from the run.

## Rubric proposals

### Proposal: Separate game interaction from idle behavior

- **Target:** `assessment.md`
- **Problem:** B4 and B8 can both reward the same tours, animation and
  second-monitor behavior, creating avoidable double counting.
- **Run evidence:** Opus 5's six tours and living scene supported both B4 and
  B8; the same overlap is visible in the existing Fable 5 and Kimi K3 notes.
- **Proposed change:** Narrow B4 to interaction vocabulary and responsiveness:
  HUD, camera feel, gamepad, audio, photo mode and visceral time/zoom controls.
  State explicitly that passive motion and tour persistence belong only to B8.
- **Why generalizable:** Every substantive demo implements some combination of
  tours and animation, so future assessors need a stable boundary between the
  criteria.
- **Expected impact:** Lower reasoning ambiguity with little expected rank
  movement. Top (Opus/Fable/Kimi), middle (Sol/GLM) and bottom (Gemini) still
  separate on interactive depth; only duplicated evidence is removed.
- **Migration:** Clean full rescore required because criterion wording changes.
- **Confidence:** high
- **Status:** suggested, not applied

### Proposal: Clarify the code-quality/test bundle

- **Target:** `assessment.md`
- **Problem:** A16 combines formatting, static analysis, unit depth and browser
  verification in one 0–5 score. Opus 5 passed 102 automated tests and all
  substantive gates but missed Prettier in one source file; other builds range
  from no E2E suite to missing lint dependencies. Half-point judgment is
  defensible but not deterministic.
- **Run evidence:** Opus 5 scored 4.5 after one formatting miss despite 58/58
  unit and 44/44 E2E passes. Fable passed all gates, Kimi K3 had no E2E suite,
  Sonnet passed only 7/29 isolated production E2E cases, and Gemini failed its
  build.
- **Proposed change:** Add score anchors: 5 requires all declared quality gates
  plus substantive unit and production E2E coverage; 4–4.5 permits a minor
  non-runtime gate failure or one missing test layer; 3 requires a clean build
  and at least one meaningful automated layer; 2 or below covers broken build,
  missing tests or mostly existence-only checks.
- **Why generalizable:** Package scripts vary across every entrant, and A16 is
  consistently one of the most judgment-heavy explicit criteria.
- **Expected impact:** More repeatable scoring. The current top, middle and
  bottom ordering should be stable; differences would reflect verification
  quality rather than new weighting.
- **Migration:** Next-run wording can use anchors, but comparable published
  scores require a clean full rescore.
- **Confidence:** high
- **Status:** suggested, not applied

## Skill proposals

### Proposal: Record graphics capability as structured evidence

- **Target:** `references/runbook.md` and `scripts/inventory_solar_bench.py`
- **Problem:** A project can report “WebGPU adapter” without identifying the
  actual adapter. Hardware performance then looks more comparable than it is,
  while SwiftShader results correctly remain excluded.
- **Run evidence:** Opus 5 exercised an actual WebGPU backend and supplied useful
  frame metrics, but its public runtime string was only `WebGPU adapter`.
  Previous field captures used SwiftShader and could not support performance
  ranking.
- **Proposed change:** Require a structured runtime block containing backend,
  browser version, adapter/vendor/device when exposed, viewport, DPR, pipeline,
  sample scene and whether FPS is score-bearing. If adapter identity is not
  exposed, label the measurement “hardware-backed, device unspecified.”
- **Why generalizable:** Rendering backends and browser launch flags differ
  across demos and materially affect any performance evidence.
- **Expected impact:** Small evidence burden; prevents accidental cross-machine
  FPS comparison. No current ranking change because only implementation
  evidence, not raw FPS, determined A15.
- **Migration:** Next-run only.
- **Confidence:** high
- **Status:** suggested, not applied

### Proposal: Add a reusable static-page consistency check

- **Target:** `scripts/` in the assessment skill
- **Problem:** Scorecard math validated, but the generated comparison resources
  still required manual checks for model count, ranking, image availability,
  browser errors and stale “nine builds” copy.
- **Run evidence:** Adding Opus 5 touched the canonical scorecard, three Solar
  pages, one gallery asset, README and three JSON-injected pages. Browser
  validation found missing document metadata in the injected pages and caught
  the exact rendered top-five ordering.
- **Proposed change:** Add a helper that serves the static directory, opens each
  declared Solar page, records console/page errors, verifies image loads,
  compares model counts and checks the first three rendered names against
  scorecard order.
- **Why generalizable:** Every new entrant changes the same denormalized set of
  artifacts.
- **Expected impact:** Moderate one-time implementation, very low per-run cost,
  and fewer stale-copy or broken-asset failures. No scoring impact.
- **Migration:** Next-run only.
- **Confidence:** high
- **Status:** suggested, not applied

## No-change decisions

- **Keep equal explicit/implicit weighting.** Opus 5 does not expose evidence
  that the 50/50 design is distorted; changing it after a new winner would be
  ranking-driven.
- **Keep the real-Earth and maximum-zoom probes difficult.** Opus 5 fails them
  despite exceptional engineering, which is useful discrimination rather than
  a rubric defect.
- **Do not add raw FPS to the score.** Only one current entrant has a
  hardware-backed capture with unspecified device identity.
- **Do not reward model recency or implementation size.** Opus 5 leads because
  behavior and verification support its scores, not because it is newer or
  larger.
