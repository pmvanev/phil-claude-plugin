# `/phil:work` — Scoping Brief

**Date:** 2026-07-13
**Status:** Scoped for nwave. This brief is the raw material for nwave's DISCUSS wave, not a finished internal design — nwave does the real design and build.

---

## One-liner

A wave-based orchestrator for technical initiatives that are transparent to the end user — refactoring, re-architecting, cleanup, migrations, dependency and performance work, tech-debt paydown. nwave's sibling for invisible work.

## Why it exists

nwave assumes a user-facing feature: personas, UX journeys, acceptance criteria derived from user stories. Invisible work has none of those, so nwave fits awkwardly. The *discipline* is the same — discuss, plan, execute in waves, respect TDD/BDD/ATDD, document decisions — but the user-story frame gets in the way. `/phil:work` provides that discipline without forcing a user-story frame.

## Model: general contractor

`/phil:work` does not re-implement execution. It discusses, plans, sequences waves, and gates them — then delegates the actual work to the tactical skills that already exist in this plugin and shares the existing rules.

- **Delegates to:** `refactor-loop`, `refactor`, `review-code`, `extract-method`, `redesign-tests`, `refactor-tests`, `clean-comments`, `spirit-walk`.
- **Shares rules:** `refactoring`, `refactoring-catalog`, `testing`, `architecture`, `coding`.

Its unique value is the connective tissue those skills lack: framing, cross-wave planning, and a decision/progress trail. This mirrors nwave's own structure, where the orchestrator sequences waves and specialist agents execute.

## Verification spine (the ATDD analog for invisible work)

Two gates on every wave:

1. **Preservation floor** — non-negotiable. Observable behavior is unchanged: the existing suite stays green, plus characterization / golden-master / contract tests added where a seam is thin.
2. **Initiative goal** — declared up front during FRAME. The specific target for *this* initiative (e.g. "cut module coupling," "remove dependency X," "p95 < 200ms"). Becomes an explicit gate.

Every wave must clear both.

## Tentative wave shape

nwave will finalize the wave set. Starting point:

1. **FRAME** — clarify the initiative: what, why, boundaries, constraints. Declare the goal metric and the preservation contract.
2. **MAP** — survey current state (spirit-walk / review-code / hotspot). Produce a wave-by-wave roadmap. Decide which tactical skill each step calls.
3. **SAFETY-NET** — establish behavior-preservation coverage *before* any structural change.
4. **EXECUTE** — run the roadmap wave by wave, delegating to tactical skills, gating each on both floor and goal.
5. **VERIFY & DOCUMENT** — confirm the goal is met and no regression occurred. Write the decision / progress / evolution trail. Archive.

## Documentation

Mirrors nwave's per-feature doc convention under a technical namespace (e.g. `docs/work/<initiative>/`): frame, roadmap, decisions log, progress, evolution summary.

## Out of scope

- User-facing features — that is nwave.
- Small one-shot tidyups that a single tactical skill already handles well. `/phil:work` is for initiatives large enough to warrant framing and multiple waves.

## Success criteria

Takes a vague technical itch → a scoped initiative with an explicit goal and preservation contract → an executed wave roadmap (via existing skills) → a decision trail — all without ever needing a persona or UX journey.

## Open questions for nwave to resolve

- Final wave names and count.
- Exact doc namespace and artifact schema (`docs/work/` vs. reuse `docs/feature/`).
- Threshold heuristics for "large enough to warrant `/phil:work`" vs. a direct tactical skill.
- How the goal metric is captured and checked per work type (coupling, dependency count, benchmark, etc.).
