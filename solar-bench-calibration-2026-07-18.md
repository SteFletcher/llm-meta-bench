# Solar Bench post-run calibration — 2026-07-18

These are proposals only. The frozen rubric and assessment skill were not
changed during the run.

## Rubric proposals

### Proposal: Anchor engineering-assurance scores

- **Target:** `assessment.md`, A16
- **Problem:** “Strict TS, ESLint, Prettier, unit + e2e suites that pass” bundles
  several independent checks without stating how missing or partly failing
  suites cap the score.
- **Run evidence:** Opus and GLM build/test successfully but cannot run declared
  lint; Lunar declares Playwright but has no tests; Gemini has an undeclared
  shallow suite but a failing build; Sonnet passes strict checks and units but
  only 7/29 isolated production E2E cases.
- **Proposed change:** append: “Use these anchors: 5 requires all supplied
  static, unit and production-browser checks to pass; no browser suite caps at
  4; a broken declared check caps at 3.5; a production-browser suite below 50%
  pass caps at 3. Missing checks are not failures, but cannot earn their part of
  full verification.”
- **Why generalizable:** it removes assessor discretion from a recurring
  cross-project pattern without changing the axis formula.
- **Expected impact:** likely no top-three reorder; Sonnet remains about 8.0,
  while Opus/GLM/Lunar become more reproducible. Exact historical deltas require
  applying the anchors to every demo.
- **Migration:** clean full rescore required for comparable results.
- **Confidence:** high
- **Status:** suggested, not applied

### Proposal: Require capture/source provenance for visual credit

- **Target:** `assessment.md`, method plus B2/B3/B8/B10
- **Problem:** an old screenshot can contradict the assessed source and still
  look like runtime evidence.
- **Run evidence:** GPT-5.6 Sol's available gallery capture predates its real
  texture upgrade; Kimi 2.7 and Gemini have no trustworthy Earth still; several
  other captures use different dates and dimensions.
- **Proposed change:** add: “For visual criteria, record capture timestamp,
  viewport, renderer and the assessed source commit/dirty-state fingerprint. A
  capture that predates material source changes is historical context only and
  cannot establish current visual quality.”
- **Why generalizable:** every visual benchmark can otherwise be gamed or
  accidentally mis-scored by stale artifacts.
- **Expected impact:** evidence confidence falls for Sol, Kimi 2.7 and Gemini;
  rankings need not change if scores were already conservative.
- **Migration:** clean full rescore required where current visual scores rely on
  unmatched captures.
- **Confidence:** high
- **Status:** suggested, not applied

### Proposal: Separate Earth identity from planet-system breadth

- **Target:** `assessment.md`, A7 and B2 wording
- **Problem:** the same Earth texture evidence can influence both “Planet visual
  quality” and “Money-shot believability” without a clear boundary.
- **Run evidence:** Fable, Kimi K3, Sonnet and Sol all forced repeated judgment
  about whether real/invented Earth geography belonged in A7, B2, or both.
- **Proposed change:** add to A7: “Judge breadth and rendering systems across at
  least Earth, one gas giant, one ringed body and one ice giant; do not score
  geographic recognizability here.” Add to B2: “Judge Earth identity, coastline,
  night-light density, cloud independence and maximum-depth fidelity only.”
- **Why generalizable:** it preserves both useful dimensions while preventing
  accidental double counting.
- **Expected impact:** little expected ranking movement; stronger rationale and
  slightly lower assessor variance.
- **Migration:** clean full rescore required for strict comparability.
- **Confidence:** medium
- **Status:** suggested, not applied

## Skill proposals

### Proposal: Inventory all visual-evidence locations and dimensions

- **Target:** `scripts/inventory_solar_bench.py`
- **Problem:** the helper reported zero evidence for demos whose useful captures
  live under `test-results/` or `docs/screenshots/`, and it did not expose mixed
  viewport sizes.
- **Run evidence:** Fable and Kimi K3 had project captures outside
  `docs/assessment/`; the refreshed Fable, Kimi K3 and standard gallery images
  are 1440×900, 1600×1000 and 1800×1012 respectively.
- **Proposed change:** scan `docs/assessment/`, `docs/screenshots/`,
  `test-results/` and Playwright attachments; emit image path, dimensions,
  modification time and a “standard viewport” flag.
- **Why generalizable:** evidence discovery and comparability are deterministic.
- **Expected impact:** modest runtime cost; materially better preflight and fewer
  stale/mismatched captures.
- **Migration:** next-run only; no rescore by itself.
- **Confidence:** high
- **Status:** suggested, not applied

### Proposal: Add an isolated production-suite helper

- **Target:** new `scripts/run_production_suite.py` plus `references/runbook.md`
- **Problem:** fixed Playwright ports allowed cross-demo contamination, and a
  Playwright-owned Sonnet preview exited mid-suite.
- **Run evidence:** Kimi 2.7 correctly rejected Kimi K3 on port 5173, then passed
  20/20 on an isolated production preview. Sonnet's first run cascaded to 29/29
  failures after its preview disappeared; a separately owned unique-port rerun
  produced the meaningful 7/29 result.
- **Proposed change:** allocate a free port, start `npm run preview`, verify title
  and app-root selectors, keep PID ownership, set a project base URL through a
  temporary assessment config, run the declared suite, then stop only that PID.
- **Why generalizable:** it converts a repeated, high-risk manual procedure into
  a deterministic one.
- **Expected impact:** fewer false passes/failures; small setup cost per demo.
- **Migration:** next-run only; rescore only if it changes test outcomes.
- **Confidence:** high
- **Status:** suggested, not applied

### Proposal: Define blocked-browser run status

- **Target:** `SKILL.md`, operation choice and completion report
- **Problem:** the workflow permits conservative scoring for a blocked runtime
  check but does not clearly name a run that covers every demo while the common
  interactive capture backend is unavailable.
- **Run evidence:** all nine demos were inventoried, audited and tested, but the
  required in-app browser exposed no backend, so standardized navigation and
  60/120-second idle captures could not run.
- **Proposed change:** add: “Call this a full-field, browser-partial
  reassessment. Do not change B2/B3/B8/B10 from prior current-commit evidence
  solely from source. The completion report must distinguish field coverage
  from runtime-evidence coverage.”
- **Why generalizable:** it avoids both abandoning useful work and overstating
  completeness.
- **Expected impact:** clearer provenance; no automatic scoring change.
- **Migration:** next-run only.
- **Confidence:** high
- **Status:** suggested, not applied

## No-change list

- Keep explicit and implicit axes equally weighted; this run did not show a
  distortion strong enough to justify changing the 50/50 headline.
- Keep difficult 60/120-second idle probes; the browser outage is an execution
  limitation, not evidence that the screen-saver requirement is unimportant.
- Do not add real-GPU FPS thresholds until a comparable hardware runner exists;
  SwiftShader timings remain unsuitable for ranking.
- Do not promote the current top-three cohort into the rubric. The deep
  comparison is editorial output, not a scoring rule.
