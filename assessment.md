# Solar-bench — common assessment sheet

A single scoring rubric for every build in `../solar-bench/`, judged against the
shared brief (`../solar-bench/PROMPT.md`) on two axes:

- **The what (explicit)** — did the build deliver what the brief literally asks for?
- **The intent (implicit)** — did it deliver what the brief *means*: "AAA game,
  not a website; something you'd leave running on a second monitor"?

## Method (same for every demo)

1. **Source audit** — map the brief's sections onto the codebase; verify claims
   in code, not READMEs.
2. **Run the build's own test suites** (unit + e2e if present); record pass/fail
   and flakiness.
3. **Serve the production build** and drive it with browser automation at
   1800×1012 — the gallery's standard capture procedure: boot → click the
   app's own navigation → let the fly-to settle → screenshot. Capture at
   minimum: Earth arrival, one gas giant, the Sun, a whole-system wide view,
   and a maximum-depth zoom on Earth. Record the actual graphics backend and
   adapter; use a project-owned Playwright stack when the in-app browser is
   unavailable.
4. **Spot-check scientific data** in the UI against NASA/JPL reference values.
5. Store evidence screenshots under the demo's `docs/assessment/` and record
   scores in the scorecard below.

Frame-rate targets cannot be verified under SwiftShader (~4 FPS regardless of
app quality); treat performance claims as self-reported unless measured on a
real GPU backend. Hardware-backed measurements must identify the backend,
adapter and viewport.

**Scale:** 0 = absent · 1 = token gesture · 2 = partial, significant gaps ·
3 = delivered with caveats · 4 = delivered well · 5 = delivered fully,
verified. Halves allowed. *(opt)* items are scored for the record but excluded
from subtotals.

### Axis normalization

Individual criteria stay on the evidence-rich 0–5 scale. The two axis
subtotals are normalized to 10 so explicit execution and implicit intent carry
equal weight in the headline result:

```text
Explicit /10 = A subtotal / 8
Implicit /10 = B subtotal / 5
Overall /10  = (Explicit /10 + Implicit /10) / 2
```

Headline scores use one decimal place. Raw subtotals remain visible for audit
and tie-breaking. Optional criteria remain separate and do not affect either
axis or the overall score.

### Reassessment run manifest

- **Run:** full reassessment, 2026-07-18 20:38 UTC, Codex
- **Paths:** meta-benchmark `/Users/stefletcher/Repos/agentic/llm-meta-bench`;
  bench root `/Users/stefletcher/Repos/agentic/solar-bench`
- **Frozen inputs:** prompt SHA-256
  `08397d7bc43e3cf0abc7997a2b5315d2d2022482be7a8927b07ddc1cbb9c9a7e`;
  rubric SHA-256
  `b18078dc889c1f1f3e5bf6bbfc2ac11d3ab2e9eba3e289a58c12f871aa601e41`
- **Environment:** macOS 26.5.2 (25F84), Node 24.15.0, npm 11.12.1;
  standard viewport 1800×1012; project browser suites used Chromium with
  SwiftShader/software rendering where configured.
- **Discovery:** nine valid `*-solar-demo` directories containing
  `package.json`; no malformed or excluded candidates. All share bench commit
  `e2409bdc6`. Fable, Gemini, Kimi 2.7 and Opus were clean at inventory time;
  GLM, Lunar, Sol, Kimi K3 and Sonnet were dirty or untracked and were assessed
  as found.
- **Browser limitation:** the required in-app browser exposed no available
  backend, so the standardized interactive capture sequence, including the
  60/120-second idle frames, was blocked. Supplied project browser suites and
  existing captures were used where available; visual claims without a current
  capture remain conservative and explicitly limited.

### Superseded working-tree verification — GPT-5.6 Sol

- **Run:** targeted reassessment, 2026-07-19 08:05 UTC, Codex. Only GPT-5.6
  Sol was rescored; every other field score remains frozen from the full run.
- **Frozen inputs:** prompt SHA-256
  `08397d7bc43e3cf0abc7997a2b5315d2d2022482be7a8927b07ddc1cbb9c9a7e`;
  rubric SHA-256
  `dc78386f47d7e50d095f0826c2d8054ed9956687f33ca51152339e9006039823`.
- **Runtime:** Chromium 149.0.7827.55, WebGL2 via ANGLE/SwiftShader,
  1800×1012, isolated production preview on port 41876. The in-app browser
  again exposed no backend, so the demo's installed Playwright/Chromium stack
  drove the equivalent capture sequence.
- **Evidence:**
  `../solar-bench/gpt56sol-solar-demo/docs/assessment/2026-07-19/` contains
  opening, Earth arrival/max-zoom/night-side, Jupiter, Saturn, Uranus,
  Neptune, Sun, whole-system, and 60/120-second frames plus the reproducible
  capture script and criterion ledger.
- **Checks:** production build, ESLint and Vitest 6/6 pass; no E2E suite is
  supplied. Prettier initially found only the prior assessment ledger
  unformatted; evidence formatting was corrected and the full check passed.
  The production bundle warns about a 626.77 kB minified JavaScript chunk.
- **Provenance correction:** this run exercised uncommitted product changes
  made after the sole repository commit, including downloaded 2K planetary
  maps and camera/material revisions. It is retained as an audit record but is
  excluded from the fair model comparison below.

### Provenance-clean reassessment — GPT-5.6 Sol

- **Run:** targeted reassessment, 2026-07-19 09:43 UTC, Codex. Only GPT-5.6
  Sol was rescored; every other field score remains frozen from the full run.
- **Frozen inputs:** prompt SHA-256
  `08397d7bc43e3cf0abc7997a2b5315d2d2022482be7a8927b07ddc1cbb9c9a7e`;
  rubric SHA-256
  `ba25da90042c59297e89df4a49e2d95f194f04bd1c82a6dbfc02c5db67c81f7a`.
- **Provenance:** the GPT-5.6 Sol product source and generated build were
  restored to the repository's sole commit,
  `e2409bdc6dff7537c6767b3da5df5f346bb417a7`. The uncommitted photographic
  texture set, replacement material loader, camera revisions and associated
  product edits were removed. Assessment evidence was preserved separately.
- **Runtime:** Chromium 149.0.7827.55, WebGL2 via ANGLE/SwiftShader,
  1800×1012, isolated production preview on port 41876. The in-app browser
  exposed no backend; the reproducible local Playwright harness drove the same
  capture sequence.
- **Evidence:**
  `../solar-bench/gpt56sol-solar-demo/docs/assessment/2026-07-19-original-head/`
  contains opening, Earth arrival/max-zoom/night-side, Jupiter, Saturn,
  Uranus, Neptune, Sun, whole-system and 60/120-second frames, plus the capture
  script and runtime ledger.
- **Checks:** production build, ESLint and Vitest 6/6 pass; no E2E suite ships.
  The original production bundle is 621.08 kB minified and triggers Vite's
  chunk-size warning. SwiftShader frame rate was not used to score quality.

### New-entrant assessment — Claude Opus 5

- **Run:** targeted new-entrant assessment, 2026-07-25, Codex. Claude Opus 5
  was added to the frozen nine-build field; prior scores were not changed.
- **Frozen inputs:** prompt SHA-256
  `08397d7bc43e3cf0abc7997a2b5315d2d2022482be7a8927b07ddc1cbb9c9a7e`;
  rubric SHA-256
  `a78384cd4453d78cb54873b8871993e02e742acee3c5e027b5c5b1b59141d4aa`.
- **Provenance:** `opus5-solar-demo` is an untracked new entrant under the
  shared Solar Bench tree whose repository parent remains
  `e2409bdc6dff7537c6767b3da5df5f346bb417a7`.
- **Runtime:** Chromium at 1800×1012 on a hardware-backed WebGPU path;
  reported pipeline `scene → bloom → ACES → MSAA`. The in-app browser exposed
  no available backend, so the demo's installed Playwright stack drove the
  equivalent visible-control capture sequence.
- **Evidence:**
  `../solar-bench/opus5-solar-demo/docs/assessment/2026-07-25/` contains
  opening, Earth arrival/max-zoom/night-side, Jupiter, Saturn, Uranus,
  Neptune, Sun, whole-system, live-stat and 60/120-second captures, plus
  reproducible scripts, runtime data and a criterion ledger.
- **Checks:** typecheck, ESLint, production build, Vitest 58/58 and Playwright
  44/44 pass. The only failed gate is Prettier on
  `tests/e2e/rendering.spec.ts`. Browser capture reported no console or page
  errors. The E2E performance sample measured roughly 121 FPS, 8.3 ms median
  and a 95 FPS 1% low on the assessment machine.

---

## A. The what — explicit criteria

| # | Criterion | What to verify |
|---|-----------|----------------|
| A1 | Rendering stack | Three.js/TS/Vite; WebGPU attempt with WebGL2 fallback; PBR, tone mapping, shadow mapping, AA (TAA or an argued alternative); bloom/volumetric glow. |
| A2 | Architecture & modularity | Matches the brief's module layout in substance, not just folder names; no giant files; no empty scaffold directories. |
| A3 | Simulation completeness | All required bodies (Sun→Pluto, Moon, Phobos, Deimos, major moons), asteroid + Kuiper belts, comets; optional spacecraft/dwarfs counted as bonus. |
| A4 | Scientific accuracy & time | Real orbital mechanics (not circles); correct distances, periods, tilts, rotation, radii; all ten prescribed time scales plus reverse and jump-to-date; data panels correct on spot-check. |
| A5 | Camera system | Orbit, free, follow, cinematic fly-to, bookmarks, smooth interpolation/momentum, mouse/trackpad/keyboard/gamepad, double-click-to-fly. |
| A6 | Zoom | Wheel + pinch, logarithmic, animated, seamless whole-system → planet → continent → clouds; texture detail at the bottom of the range. |
| A7 | Planet visual quality | Textures (real or convincing), normal/roughness where visible, night lights, clouds, atmospheres, specular oceans, rings; Sun with animated corona/flares. |
| A8 | Space backdrop | Milky Way, dense instanced stars, nebulae, parallax/skybox. |
| A9 | UI feel | Dark glassmorphism sci-fi HUD, animated panels, icons, no plain HTML tables. |
| A10 | Widgets | Time, object browser, planet info, distance, scale, orbit toggles, lighting toggles, navigation, stats, educational — present *and functional* (check stats numbers are real). |
| A11 | Search | Instant, with aliases/nicknames ("red planet", "gas giant"). |
| A12 | Cinematic tours | Scripted fly-throughs matching the brief's examples; banner/UX. |
| A13 | Audio *(opt)* | Ambient + UI sounds, mute toggle, autoplay-safe. |
| A14 | Accessibility | Keyboard nav, colour-blind mode, reduced motion, ARIA/screen-reader effort. |
| A15 | Performance engineering | Instancing, LOD, culling, texture streaming, worker threads, lazy loading — as implemented, not as claimed. |
| A16 | Code quality & tests | Strict TS, ESLint, Prettier, unit + e2e suites that pass. |
| A17 | Deliverables | README, architecture/development/deployment/performance docs, diagrams, asset credits/licensing. |
| A18 | Nice extras *(opt)* | Which of the brief's "if time permits" list shipped (photo mode, NASA imagery, eclipses, VR…). |

**Explicit subtotal = A1–A17 (excluding A13) out of 80.**

## B. The intent — implicit criteria

The brief says "AAA game, not a website; something you'd leave running on a second monitor." That phrase hides a dozen requirements that are never spelled out. Score these by asking whether the build *behaves* like it understood the assignment, not just whether it ticked boxes.

| # | Criterion | What to verify | Concrete discriminating examples |
|---|-----------|----------------|----------------------------------|
| B1 | Resourcefulness | Acts like the brief's "senior graphics programmer" persona: exploits legitimate shortcuts (real assets, clever fallbacks) instead of grinding everything by hand; attributes what it borrows. | Did the build download real NASA/USGS/Solar-System-Scope maps (Earth's Blue Marble, Saturn ring alpha maps, Jupiter cloud bands) instead of procedurally inventing a planet? Did it wire up an existing Space.js / NASA Horizons feed for orbital elements rather than hardcoding keplerian elements by hand? Attribution in the README / LICENSE is the honesty signal — silence means either not used or not credited. |
| B2 | Money-shot believability | Fly to Earth and look: is this *the* Earth (coastlines, night lights, clouds) or an invented planet? | Zoom to continental scale: can you distinguish the Iberian Peninsula from a blob? Is the Sahara visibly tan, the Amazon basin green, Antarctica white? Night-lights should show population density bands (US east coast, central Europe, Nile delta), not a uniform glow. Clouds should be semi-transparent and rotate at a slightly different rate than the surface. A build that passes these is using real data; one that fails invented it. |
| B3 | Cinematic staging | Do arrivals compose a deliberate frame — day-side bias, sensible distance, hero framing — or is a good shot luck? Check multiple bodies, not just Earth. | **Earth:** arrival should land you on the day-side with the terminator visible on one edge — full dark side means the renderer has no staging awareness. **Saturn:** the canonical view is ~30° above the equatorial plane so the rings sweep across the foreground; arriving at 0° inclination gives you a thin line. **Jupiter:** the Great Red Spot should be rotated to face the camera, or at least be on the visible hemisphere — arriving to a plain banded face without the GRS is a staging miss. **Sun:** a close approach should use the corona and flare system as the hero element, not just a big white ball. |
| B4 | Game, not website | Interaction vocabulary of a game: HUD, tours, gamepad, audio, fluid zoom, photo mode. | The "second monitor" test: launch the build, wait 60 seconds without touching anything. Does it stay compelling (animated clouds, rotating bodies, comet trails in motion, a tour cycling) or does it go static? A website delivers its information and waits; a game is alive. Bonus: does holding a key accelerate time and create a visceral sense of planetary motion? Does zooming all the way in on Earth reveal city-level texture detail, making the zoom feel like a journey rather than a slider? |
| B5 | Honesty / self-knowledge | Disclosed scale factors, measured-vs-claimed performance, argued deviations, correct licensing — versus silent shortcuts and decorative numbers. | Stats HUD is a key tell: open it and check the numbers. Draw-call counts that never change as you add/remove objects, triangle counts that read zero or a static value, FPS locked to exactly 60 with no variance — these are decorative readouts, not measurements. Scale: if the build shows all 8 planets simultaneously with visible disc size on all of them, it has inflated planet radii — does it say so? The brief explicitly permits scale inflation if disclosed; it forbids silent distortion. |
| B6 | Substance over scaffolding | No empty directories, orphaned assets, dead toggles, or readouts that exist to look complete. | Walk the source tree: `src/workers/` with no `.ts` files in it, `src/assets/textures/` with placeholder filenames, a "Spacecraft" toggle in the UI that renders nothing, a distance readout that doesn't change as you move — each is a scaffolding tell. Count the ratio of implemented features to mentioned features in the README; a gap > 20% is a red flag. |
| B7 | Scientific soul | Accuracy is load-bearing (tested mechanics, real reference data, citations) rather than a checkbox. | Time-lapse test at 1000× speed: do inner planets lap outer ones at visibly correct relative rates? (Mercury should complete ~4 orbits for every Earth orbit; Jupiter should barely move.) Tilt test: is Uranus rolling on its side (~98° axial tilt) or standing upright like a default sphere? Ring plane test: do Saturn's rings cast a shadow on the planet body, and vice versa, at the correct seasonal angle? Moon phase test: is the Moon phase in the UI consistent with the lit hemisphere visible from Earth at that date? These are the checks that separate a sim from an illustration. |
| B8 | The idle / screen-saver test | "Leave running on a second monitor" implies the sim must be beautiful *without interaction*. | Start the build and step away. After 2 minutes: is something still moving and worth watching? Comet tails should be tracing arcs; cloud layers rotating; tours cycling through dramatic views. A sim that goes visually static after load has failed this implicit contract. Does the default camera position and initial zoom level result in a compelling opening frame, or does the user have to hunt for a good view? |
| B9 | Scale honesty and the void | Real scale means the void must *feel* like void. | Zoom all the way out to see Neptune. At that zoom level, Earth should be invisible or a single pixel — if Earth is still a thumb-sized disc while Neptune is also visible, planet radii are unrealistically inflated. Conversely, if the build uses a realistic scale *and* discloses it, does it provide a scale-exaggeration toggle so users can still see the planets? The implicit requirement is that the scale choice is intentional and communicated, not an accident. |
| B10 | The hard-body test | The bodies that separate a serious renderer from a quick demo are Saturn's rings, Jupiter's cloud system, and Neptune's colour. | **Saturn rings:** not a flat disc — should show Cassini Division as a dark gap, ring shadow on the planet body, ring alpha fade at inner and outer edges, and backscatter glow when the Sun is behind. **Jupiter:** cloud bands should have relief (normal map or displacement), the GRS should be a visible oval vortex, not a smear. **Neptune vs Uranus colour:** Neptune is deep cobalt blue (#1a3a6b range); Uranus is pale cyan-green (#5fddcd range) — builds that make both the same shade have used placeholder colours. |

**Implicit subtotal = B1–B10 out of 50.**

### Implicit requirement probes (quick-check list)

Run these targeted observations before scoring. Each is a specific, falsifiable test designed to surface implicit quality.

| Probe | Pass | Fail |
|-------|------|------|
| **Day-side arrival** | Fly to Jupiter: lit hemisphere occupies > 60% of the frame on arrival | Jupiter arrives as a dark crescent |
| **Real coastlines** | Zoom to Europe at max detail: Mediterranean coastline is recognisable | Coastline is a blob or procedurally generated |
| **Night lights density** | Earth night-side shows bright node at US east coast, bright arc across Europe | Uniform or absent night lights |
| **Retrograde motion** | Speed to 500×, watch Mars from above ecliptic: inner planets visibly lap it | All planets appear to orbit at similar angular rates |
| **Uranus tilt** | Uranus's north pole points roughly toward the Sun | Uranus upright like all other planets |
| **Ring shadow** | Saturn's rings cast a curved shadow on the planet's cloud tops at off-equinox dates | No ring shadow, or shadow is a straight line |
| **Cassini Division** | Saturn rings show a distinct dark gap at ~90 000 km radius | Uniform ring disc |
| **Stats are live** | Open stats HUD; navigate from Jupiter to Sun; draw calls / triangle count changes | Count is static or zero |
| **Neptune blue ≠ Uranus blue** | The two ice giants are visibly different hues | Same shade of blue |
| **Cloud rotation offset** | Earth's cloud layer has independent slower/faster rotation than the surface | Clouds locked to surface |
| **Moon phase consistency** | Moon phase indicator matches the lit hemisphere visible from Earth | Phase readout contradicts geometry |
| **Empty source dirs** | `find src/ -type d -empty` returns nothing | Returns one or more empty directories |
| **Void at scale** | Full-system view: inner planets are dots or invisible | All 8 planets have visible disc size simultaneously |
| **60-second idle beauty** | After 60 s hands-off the scene is still in motion and compelling | Scene is visually static |

---

## Scorecard

Scores per demo; fill a column per assessed build. Evidence lives in each
demo's `docs/assessment/`; narrative per build in the notes sections below.

| Criterion | sonnet5 | fable5 | opus5 | opus48 | gpt56sol | gpt56lunar | gemini31pro | glm52 | kimi27 | kimi3 |
|-----------|:-------:|:------:|:-----:|:------:|:--------:|:----------:|:-----------:|:-----:|:------:|:-----:|
| A1 Rendering stack | 4 | 4 | 5 | 4 | 3 | 3 | 2 | 3.5 | 4 | 3.5 |
| A2 Architecture | 4 | 5 | 5 | 4.5 | 4.5 | 2.5 | 0.5 | 3.5 | 4 | 5 |
| A3 Completeness | 5 | 5 | 5 | 4.5 | 4.5 | 3.5 | 0.5 | 4 | 3 | 5 |
| A4 Science & time | 4.5 | 5 | 5 | 4.5 | 4.5 | 3.5 | 0.5 | 4 | 4 | 4.5 |
| A5 Camera | 5 | 5 | 5 | 4.5 | 4.5 | 2.5 | 1 | 4 | 4.5 | 5 |
| A6 Zoom | 3.5 | 4.5 | 3.5 | 3.5 | 2.5 | 2 | 1 | 3.5 | 3.5 | 4 |
| A7 Planet visuals | 4 | 4.5 | 4 | 3 | 2.5 | 1.5 | 1 | 2.5 | 3 | 4 |
| A8 Backdrop | 4 | 5 | 5 | 3.5 | 4 | 2.5 | 1 | 3 | 3 | 4.5 |
| A9 UI feel | 5 | 5 | 5 | 4 | 5 | 4 | 2.5 | 4 | 3.5 | 4.5 |
| A10 Widgets | 4.5 | 4.5 | 5 | 4.5 | 4 | 3.5 | 1 | 4.5 | 4 | 5 |
| A11 Search | 5 | 5 | 5 | 5 | 5 | 3.5 | 0.5 | 4 | 4 | 5 |
| A12 Tours | 4 | 5 | 5 | 3.5 | 4 | 2 | 0 | 3.5 | 0.5 | 5 |
| A13 Audio *(opt)* | 5 | 4.5 | 4.5 | 4 | 1 | 1 | 0 | 0.5 | 4 | 4 |
| A14 Accessibility | 5 | 4.5 | 5 | 3 | 4 | 2.5 | 1 | 2.5 | 2.5 | 4 |
| A15 Perf engineering | 3 | 5 | 5 | 4 | 3.5 | 1.5 | 1 | 3 | 5 | 4.5 |
| A16 Code & tests | 3 | 5 | 4.5 | 3.5 | 4 | 1.5 | 0.5 | 3.5 | 4.5 | 4 |
| A17 Deliverables | 4 | 4 | 5 | 4.5 | 4.5 | 3.5 | 0 | 2.5 | 2 | 4.5 |
| **Explicit (A) / 80** | **67.5** | **76** | **77** | **64** | **64** | **43** | **14** | **55.5** | **55** | **72** |
| **Explicit / 10** | **8.4** | **9.5** | **9.6** | **8.0** | **8.0** | **5.4** | **1.8** | **6.9** | **6.9** | **9.0** |
| B1 Resourcefulness | 5 | 4 | 4 | 3.5 | 2.5 | 2.5 | 1 | 3 | 3 | 3.5 |
| B2 Money shot | 4.5 | 3.5 | 3 | 2.5 | 1.5 | 1.5 | 0.5 | 2.5 | 2 | 3 |
| B3 Cinematic staging | 2 | 4.5 | 4 | 2 | 3 | 1.5 | 0.5 | 2.5 | 2.5 | 4 |
| B4 Game feel | 4 | 4.5 | 5 | 4 | 4 | 2.5 | 1 | 3.5 | 4 | 5 |
| B5 Honesty | 4 | 4 | 5 | 3.5 | 3 | 3 | 1 | 3 | 3.5 | 3.5 |
| B6 Substance | 3 | 5 | 5 | 4 | 3.5 | 2.5 | 0.5 | 3.5 | 4 | 4.5 |
| B7 Scientific soul | 5 | 4.5 | 5 | 4 | 4 | 3 | 1 | 3.5 | 3.5 | 4.5 |
| B8 Idle/screen-saver | 4 | 4.5 | 5 | 4 | 4 | 2.5 | 1 | 3.5 | 4 | 4.5 |
| B9 Scale honesty | 3 | 5 | 5 | 5 | 4 | 2 | 0.5 | 3 | 2.5 | 5 |
| B10 Hard-body test | 3.5 | 4 | 4 | 2.5 | 1.5 | 1 | 0 | 2.5 | 2 | 4 |
| **Implicit (B) / 50** | **38** | **43.5** | **45** | **35** | **31** | **22** | **7** | **30.5** | **31** | **41.5** |
| **Implicit / 10** | **7.6** | **8.7** | **9.0** | **7.0** | **6.2** | **4.4** | **1.4** | **6.1** | **6.2** | **8.3** |
| **Overall / 10** | **8.0** | **9.1** | **9.3** | **7.5** | **7.1** | **4.9** | **1.6** | **6.5** | **6.5** | **8.7** |

---

## Notes per build

### Sonnet 5 — "SOL" *(assessed 2026-07-18, commit `e2409bd`)*

Evidence: `../solar-bench/sonnet5-solar-demo/docs/assessment/`. ESLint,
test typecheck, production build and Vitest 10/10 pass. The current declared
29-case Playwright suite first failed 29/29 after its owned preview server
exited; the clean-port production rerun kept the intended server alive and
passed 7/29. The remaining 22 cases timed out or failed assertions under
SwiftShader, including a blank-canvas probe, camera distance, accessibility,
time controls and widgets. Traces and failure screenshots are under
`docs/assessment/2026-07-18/e2e-results/`.

- **Signature move (B1):** the only build that cashed the brief's "Real NASA
  imagery" extra — downloaded 27 MB of Solar System Scope / New Horizons 2K
  maps and wrote correct CC-BY attribution unprompted. Real coastlines and
  real city lights on Earth as a direct result.
- **Signature miss (B3):** the fly-to has no day-side bias — Jupiter and
  Saturn arrive as dark crescents; Earth's lit arrival was orbital luck. Would
  beat Fable 5 on Earth, lose to it on Jupiter/Saturn under the gallery's own
  methodology.
- **Scaffolding debt (A2/A15/B6):** empty `src/workers/` and `src/assets/`
  dirs; no texture streaming/occlusion; three dwarf-planet textures downloaded
  but never modeled; stats HUD draw-call/triangle readouts are junk (sampled
  after frame reset).
- **Deviations argued honestly (A1/B5):** TAA swapped for MSAA+SMAA with a
  written ghosting rationale; WebGPU probed off-canvas with the WebGPU chunk
  lazy-loaded; render scale disclosed as non-1:1.
- **B8/B9/B10 addenda:** idle test passes (clouds + comet tails + asteroid belt all animate); scale is exaggerated but undisclosed (B9 = 3); ring shadow absent and Cassini Division barely visible (B10 = 3.5); GRS present but stationary.
- **Verification regression (A16):** strict checks and unit science remain
  healthy, but a 7/29 isolated production E2E result no longer supports the
  previous near-full test score. SwiftShader frame rate was not used to lower
  camera or visual criteria.
- **Verdict:** *smart outsourcing, unlucky lighting, unstable verification.*
  Explicit 8.4 · Intent 7.6 · Overall **8.0/10**.

### Fable 5 — "SOL" *(assessed 2026-07-18)*

Evidence: `../solar-bench/fable5-solar-demo/test-results/shots/`. Suites:
Vitest 11/11; Playwright 21/21; production build and ESLint pass.

- **Prior field winner:** a highly complete build, with a genuinely modular
  7k-line engine, full catalogue, tested Kepler propagation, camera modes,
  search, tours, audio, live widgets and worker-built belts.
- **Best staging:** day-side fly-to logic and the captured Saturn arrival both
  show deliberate camera direction. The rings have strong banding and a clear
  Cassini division.
- **Core limitation:** Earth is a technically impressive procedural shader,
  not Earth data. It reads as a convincing ocean world at orbital distance but
  its invented continents fail the Europe/coastline probe.
- **Verdict:** *the best product, one real texture set short of the brief's
  money shot.* Explicit 9.5 · Intent 8.7 · Overall **9.1/10**.

### Claude Opus 5 — "SOL" *(assessed 2026-07-25, bench commit `e2409bd`)*

Evidence:
`../solar-bench/opus5-solar-demo/docs/assessment/2026-07-25/`. Typecheck,
ESLint, production build, Vitest 58/58 and Playwright 44/44 pass. Prettier
finds one unformatted E2E source file.

- **New field winner:** the broadest verified implementation: actual WebGPU
  with fallback, 44 bodies, 160k stars, 27k minor bodies, strong Keplerian
  science, six tours, three camera modes, live widgets, procedural audio,
  accessibility modes, workers, LOD, streaming textures and a floating origin.
- **Best verification:** the 44-case production E2E run exercises the renderer,
  full catalogue, inputs, camera, tours, widgets, time, display modes,
  accessibility and photo capture. Hardware WebGPU sampling stayed smooth, and
  the independent evidence capture emitted no browser errors.
- **Deliberate staging:** Earth and Jupiter arrive on the lit side, Saturn is
  framed above its ring plane with the Cassini division and shadow visible,
  and the Sun uses its corona as the hero effect. Jupiter's Great Red Spot is
  not visible, so staging and hard-body quality stop short of full marks.
- **Core limitation:** every planetary surface is generated. Earth is
  attractive at orbital distance, with independent clouds and atmosphere, but
  has invented geography and no population-shaped night lights; at the 127 km
  maximum-depth capture it becomes a soft green field.
- **Second-monitor proof:** the Grand Tour was still progressing through
  distinct scenes at 60 and 120 seconds. Live draw-call and triangle counters
  changed between Jupiter and Sun, and the full-system view collapses inner
  planets to points at true scale.
- **Verdict:** *the strongest complete simulator in the field, with unusually
  deep engineering and verification; procedural surface art is the only clear
  ceiling.* Explicit 9.6 · Intent 9.0 · Overall **9.3/10**.

### Opus 4.8 — "SOL" *(assessed 2026-07-18)*

Evidence: `../solar-bench/opus48-solar-demo/docs/screenshots/`. Suites: Vitest
16/16; browser verification 26/26 plus widget verification 17/17 after serving
the production build; build passes; the declared lint command fails because
ESLint is not installed.

- Strong architecture, science, search and unusually good true-scale honesty.
- The renderer is overexposed in the supplied captures: stars and bloom wash
  out the scene, Earth is noise-like, and Saturn's rings clip nearly white.
- **Verdict:** *substantial simulator, weak art direction.* Explicit 8.0 ·
  Intent 7.0 · Overall **7.5/10**.

### GPT-5.6 Sol — "Celestial Navigation System" *(provenance-clean reassessment 2026-07-19)*

Evidence: original-commit production captures and ledger under
`../solar-bench/gpt56sol-solar-demo/docs/assessment/2026-07-19-original-head/`.
Production build, ESLint and Vitest 6/6 pass; no E2E suite ships.

- **Strong simulator shell:** 26 bodies, Keplerian motion, rich physical data,
  three camera modes, search aliases, four tours, time controls, layer toggles
  and a particularly polished sci-fi cockpit all work in the original build.
- **Original Earth fails the money shot:** its 512×256 canvas texture draws
  five green ellipses as continents and white strips as clouds. The arrival is
  washed out; maximum zoom becomes a soft abstract field; the night side has a
  uniform blue emissive tint rather than city-light density.
- **Staging is functional, not cinematic:** the Sun-vector camera does reach
  lit hemispheres and lifts above Saturn's ring plane, but Earth is overexposed,
  Jupiter's Great Red Spot is not visible, and the opaque uniform rings lack a
  Cassini division or convincing shadow.
- **Honesty gap:** the WebGPU badge only detects `navigator.gpu`; “bloom” is an
  exposure change; GPU/CPU timings are synthetic; audio has no engine; photo
  mode never exposes the captured frame. The README does honestly describe the
  surfaces as procedural and discloses logarithmic visual scaling.
- **Verdict:** *an excellent cockpit around an invented, low-detail universe.*
  Explicit 8.0 · Intent 6.2 · Overall **7.1/10**.

The uncommitted texture-map upgrade previously assessed at 8.4 is excluded from
model comparison. On the original submitted solution, Sol ranks fifth overall;
Sonnet 5 returns to the fair top three.

### GPT-5.6 Lunar — "Deep Space Atlas" *(assessed 2026-07-18)*

Evidence: `site/assets/gpt56lunar-earth.jpg`. Production build passes; the
declared Playwright command exits with “No tests found”.

- Broad, legible atlas UI and mostly sound reference data.
- Flat-shaded bodies, weak fly-to framing, compressed architecture and thin
  interaction depth leave it closer to an interactive diagram than a game.
- **Verdict:** *competent atlas, failed AAA brief.* Explicit 5.4 · Intent 4.4 ·
  Overall **4.9/10**.

### Gemini 3.1 Pro — "SOL" *(assessed 2026-07-18)*

No valid production evidence: `npm run build` fails TypeScript on an unused
`delta`; no test script is declared. The repository contains a 12-case
Playwright file that checks only whether static DOM elements exist.

- Only the Sun, Earth and Mars are rendered. Orbits are simple circles; nearly
  every requested widget is inert placeholder HTML with `Unknown` or zero data.
- Fourteen empty scaffold directories and leftover Vite starter assets make
  the implementation/scaffolding gap explicit.
- **Verdict:** *a mock-up wearing the brief's labels.* Explicit 1.8 · Intent
  1.4 · Overall **1.6/10**.

### GLM-5.2 — "SOL" *(assessed 2026-07-18)*

Evidence: `../solar-bench/glm52-solar-demo/test-results/`. Production build and
Playwright 22/22 pass; the declared lint command fails because ESLint is not
installed.

- Functional, accurate and well verified for its compact size: live stats,
  search aliases, time controls, fly-to and both belts work.
- Visuals remain schematic; Jupiter's procedural gradient and flat ring-like
  bands fail the hard-body probe, and the backdrop is busy rather than cinematic.
- **Verdict:** *excellent functional coverage, middling world-building.*
  Explicit 6.9 · Intent 6.1 · Overall **6.5/10**.

### Kimi 2.7 — "SOL" *(assessed 2026-07-18)*

Suites: Vitest 3/3; Playwright 20/20; production build and ESLint pass. The
first browser run accidentally attached to Kimi K3 on the shared fixed port;
the clean-port rerun passed every case.

- Serious performance work — four geometry LODs, instanced asteroids, a real
  ephemeris worker, postprocessing, audio and functional photo capture.
- Catalogue breadth and cinematic tours are the large misses: only three
  required moons are modeled and no scripted tour system exists.
- **Verdict:** *good engine fundamentals, incomplete universe.* Explicit 6.9 ·
  Intent 6.2 · Overall **6.5/10**.

### Kimi K3 — "S·O·L" *(assessed 2026-07-18)*

Production build, ESLint and Vitest 16/16 pass. No E2E suite ships despite the
README claiming browser-automation verification; current visual grades are
therefore source-audited rather than capture-verified.

- **Best engineering challenger:** 30 focused modules, a full catalogue, two
  comets, 8k worker-built asteroids, true-scale mode, live renderer counters,
  six tours, a day-side camera, gamepad, audio and a particularly complete HUD.
- **Best “game” interpretation:** moving belts, rotating clouds, comet tails,
  solar wind and curated tours keep the system alive without input.
- **Core limitation:** all surfaces are 512×256 generated canvases. Earth has
  invented geography and synthetic city-light density, so maximum zoom cannot
  satisfy the continent/city probes. WebGPU is detected but never attempted.
- **Verdict:** *the broadest game system after Fable, but procedural art caps
  the money shot.* Explicit 9.0 · Intent 8.3 · Overall **8.7/10**.

## Overall order

Equal-weight overall scores (optional criteria excluded): Claude Opus 5
**9.3/10**, Fable 5 **9.1**, Kimi K3 **8.7**, Sonnet 5 **8.0**, Opus 4.8
**7.5**, GPT-5.6 Sol **7.1**, GLM-5.2 **6.5**, Kimi 2.7 **6.5**, GPT-5.6
Lunar **4.9**, Gemini 3.1 Pro **1.6**. Raw A and B subtotals above remain the
tie-breakers.

Assessment caveat: the in-app browser runtime was unavailable for both the
2026-07-18 field run and the Opus 5 addition. Existing repository captures and
project-owned Playwright stacks were used where present; otherwise visual
scores were conservatively source-audited and are identified above.
SwiftShader FPS was never used as a quality discriminator; Opus 5's separately
identified WebGPU measurement used a hardware-backed runtime.
