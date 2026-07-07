<!-- markdownlint-disable MD024 -->
# Feature Delta — mobile-web-standards

DISCUSS wave output (lean density). This feature adds **mobile web coverage** to the plugin's
design standards. It extends the existing `rules/ux.md` (usability + accessibility) and
`rules/ui.md` (aesthetics) rather than adding new rule files, and updates the `/phil:ux-review`
audit command to catch the new mobile always-flag items. It is the mobile facet of the same job
the `ux-standards-rule` feature established — see `docs/feature/ux-standards-rule/`.

---

## Wave: DISCUSS / [REF] Pre-requisites

- **Research precursor (D1, hard prerequisite):** `docs/research/ux/mobile-web-best-practices.md`
  must exist before the rule wording is authored in DELIVER. Produced by `/nw-research`. Mirrors
  how `ux.md` was authored against `docs/research/ux/general-ux-design-best-practices.md`. The
  research doc is `@infrastructure` — it lands as a **precursor commit**, not a shipped slice
  (slice-composition gate: a slice of only `@infrastructure` stories is a structural failure).
- **Parent feature:** `ux-standards-rule` (shipped `rules/ux.md`) — this feature depends on that
  rule's two-tier structure, voice, and path globs already existing.
- **Existing artifacts touched:** `rules/ux.md`, `rules/ui.md`, `skills/ux-review/SKILL.md`,
  `commands/ux-review.md`.

## Wave: DISCUSS / [REF] Persona

- **Devon (`devon-ui-developer`)** — UI-building developer, editing files matching the UI globs,
  heads-down on behavior. Wants objective UX/a11y defects — now including **mobile web** defects —
  caught in-flow without recalling the whole WCAG + heuristics checklist.
  (Note: `docs/product/personas/devon-ui-developer.yaml` is referenced by `jobs.yaml` but the
  persona file is missing — a pre-existing gap, out of scope for this feature.)

## Wave: DISCUSS / [REF] JTBD one-liner

Registered job (refined this wave, not duplicated): **`catch-ux-violations-while-building-ui`** —
"When I'm building or editing a UI, I want the plugin to flag concrete UX/usability and
accessibility violations and name the preferred form, so I can catch defects before they ship."
**Mobile facet:** the surface now explicitly includes mobile web rendering (reflow, zoom,
orientation, pointer gestures, motion, touch). Dimension/force refinements recorded in
`docs/product/jobs.yaml` under that job.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Research wave is a precursor** — author `docs/research/ux/mobile-web-best-practices.md` before rule wording. | Evidence-based bar set by the parent; CLAUDE.md "empirical design over speculation". User-selected. |
| D2 | **Extend `ux.md` + `ui.md`; no new rule files.** Responsive/touch tier → `ux.md`; mobile aesthetic guardrails → `ui.md`. | Preserves the ux=usability / ui=aesthetics axis; `/phil:ux-review` inherits the `ux.md` additions for free; no new inter-rule boundary to police. User-selected. |
| D3 | **Always-flag ⊆ citable WCAG 2.2 SC**; advisory tier + completeness sourced from the research doc. | Objective mobile defects (1.4.10, 1.4.4, 1.3.4, 2.5.1, 2.5.4, 2.5.8) are knowable and citable now; softer guidance (thumb zones, safe-area, hover-on-touch, on-screen keyboard, constrained-device perf) comes from research. |
| D4 | **Refine the existing job**, do not create a duplicate. | Devon's job is unchanged; only its surface widened. Precedent: `redesign-tests` refined forces of `keep-test-suite-trustworthy` rather than adding a job. |
| D5 | **Length/voice discipline preserved** — react.md voice, terse, Prefer/Over tables, "Do not flag" closing; net additions ~15–25 lines across both files. | The parent's scannability norm; auto-loaded rules must stay < 2-min reads or they won't be internalised. |
| D6 | **`/phil:ux-review` updated** to add the new mobile always-flag items to its must-fix list. | The parent deferred the review skill; it now exists, so the audit touchpoint (T3) must catch the new items, not only in-flow (T1/T2). User approved all 3 slices. |

## Wave: DISCUSS / [REF] Driving ports

- **Auto-loaded rule** (`ux.md`, `ui.md`) — fires on the UI path globs during editing (T1) and
  review (T2). No manifest change; the existing rule loader discovers the additions.
- **`/phil:ux-review` command** — on-demand audit (T3) writing `.ux-review-backlog.md`.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Additive, isolated, brownfield edits to existing files. No walking-skeleton wiring;
no env-switching. Slice 1 (the `ux.md` mobile tier) is the thinnest end-to-end value slice.

## Wave: DISCUSS / [REF] Scope Assessment: PASS

Right-sized. 3 thin slices + 1 precursor commit, across 3 existing files, 1 context (the rules /
review system), 0 cross-context integration, well under 2 weeks. No oversized signal fires. No
split required. Carpaccio taste tests: each slice ships end-to-end in ≤1 day, carries a learning
hypothesis, uses a real dogfood fixture (not synthetic), and has explicit IN/OUT scope. The
research doc is correctly a precursor, not a decorative slice.

## Wave: DISCUSS / [REF] User stories

All stories trace to `job_id: catch-ux-violations-while-building-ui` (mobile facet).

### US-01 — `ux.md` gains a mobile/responsive always-flag + advisory tier *(walking-skeleton slice)*

**Problem.** Devon builds a responsive component. A fixed-width container that breaks reflow at
320px, an orientation-locked view, or a gesture-only/hover-only control reaches manual review or a
real phone — because today only touch-target size (`ux.md:27`) covers mobile at all.

**Who.** Devon, editing UI-glob files, wants mobile defects flagged in-flow with the preferred form.

**Solution.** A mobile/responsive block in `ux.md` — always-flag items anchored to WCAG SC, plus an
advisory sub-tier for judgment calls — in the existing react.md voice.

#### Elevator Pitch
- **Before**: Devon edits UI with no mobile feedback — reflow, orientation, and gesture defects
  surface only on a real device or in production.
- **After**: run the editor on `ProductGrid.tsx` → the plugin flags *"fixed `width: 1200px`
  container breaks reflow below 320px — use max-width / fluid units (WCAG 1.4.10)"* and
  *"swipe-only carousel has no single-pointer alternative (WCAG 2.5.1)"*, each naming the fix.
- **Decision enabled**: whether to fix each mobile defect before committing.

#### Acceptance Criteria
- [ ] `ux.md` gains a mobile/responsive section within its existing two-tier structure (no new file).
- [ ] Always-flag items name the violation **and** preferred form for, at minimum: content that
      breaks **reflow** at 320px CSS width / 400% zoom (1.4.10); **text that can't resize** to 200%
      without loss (1.4.4); **orientation lock** with no essential-use exception (1.3.4);
      **path/multipoint gesture** with no single-pointer alternative (2.5.1); **motion-actuated**
      action with no UI-control alternative (2.5.4).
- [ ] Each always-flag item cites its WCAG 2.2 SC number (per D3).
- [ ] An advisory sub-tier covers judgment calls (thumb-reach, hover-on-touch affordance,
      on-screen-keyboard obscuring inputs) without hard-blocking.
- [ ] Net addition ≤ ~15 lines; react.md voice preserved; no duplication of the existing
      target-size line.

#### Outcome KPIs
- **Who**: developers editing UI files with the plugin active.
- **Does what**: catch mobile reflow/orientation/gesture/motion defects during editing/review.
- **By how much**: all 5 always-flag mobile classes surfaced on a seeded fixture (5/5); baseline 0.
- **Measured by**: a dogfood fixture with one instance of each mobile defect class.
- **Baseline**: only touch-target size is covered today.

### US-02 — `ui.md` gains mobile aesthetic guardrails

**Problem.** `ui.md` pushes rich aesthetics (glassmorphism, heavy micro-animations, "wow at first
glance") with no mobile caveat, so its advice can degrade mobile: motion that ignores
`prefers-reduced-motion`, effects that tank performance on constrained devices, type/contrast that
fails at small sizes.

**Who.** Devon applying `ui.md`'s aesthetic guidance to a UI that will render on phones.

**Solution.** A short mobile-guardrails note in `ui.md` scoping its aesthetic advice: honour
`prefers-reduced-motion`, budget heavy effects on constrained devices, keep type/contrast legible
at mobile sizes. Aesthetics stay `ui.md`'s remit — this adds guardrails, not usability rules.

#### Elevator Pitch
- **Before**: `ui.md` implies desktop-grade polish everywhere; nothing warns it can hurt mobile.
- **After**: Devon reads `ui.md` → sees "honour `prefers-reduced-motion`; heavy blur/gradient
  stacks cost frames on low-end phones; verify type/contrast at mobile sizes" alongside the
  aesthetic push.
- **Decision enabled**: whether an aesthetic choice is safe to ship to mobile as-is.

#### Acceptance Criteria
- [ ] `ui.md` gains a brief mobile-guardrails note (≤ ~8 lines) qualifying its aesthetic advice.
- [ ] Covers at minimum: `prefers-reduced-motion`, effect/animation performance on constrained
      devices, small-screen type/contrast legibility.
- [ ] Does **not** restate `ux.md`'s usability/a11y items (complement, not duplicate) — boundary held.
- [ ] `ui.md` remains passive (no review command added for it).

### US-03 — `/phil:ux-review` audits the new mobile always-flag items

**Problem.** The audit touchpoint (T3, on-demand review) won't catch the mobile defects unless the
review skill's must-fix list is extended; today it enumerates only the parent's defect classes.

**Who.** Devon (or a maintainer) running `/phil:ux-review` on a mobile UI or a diff.

**Solution.** Add the US-01 mobile always-flag items to the must-fix list in
`skills/ux-review/SKILL.md`, tracing each to its `ux.md` principle + WCAG SC, with a
"verify at runtime" note where a rendered check is needed (actual reflow/zoom behaviour).

#### Elevator Pitch
- **Before**: `/phil:ux-review` on a mobile screen reports desktop-era UX defects but misses reflow,
  orientation, and gesture violations.
- **After**: run `/phil:ux-review src/mobile/` → backlog includes *"[U0xx] fixed-width container
  breaks reflow (WCAG 1.4.10) — must-fix"* traced to `ux.md`.
- **Decision enabled**: which mobile defects to fix from the prioritized backlog.

#### Acceptance Criteria
- [ ] `skills/ux-review/SKILL.md` must-fix list includes the 5 mobile always-flag classes from US-01,
      each tracing to a `ux.md` principle and WCAG SC.
- [ ] Items whose defect depends on rendered output (reflow/zoom) are marked "verify at runtime".
- [ ] No new flags invented beyond what `ux.md` (post-US-01) contains — the skill mirrors the rule.

## Wave: DISCUSS / [REF] Out-of-scope

- Native mobile (iOS/Android) app UI — web rendering only.
- A dedicated `/phil:ui-review` command — `ui.md` stays passive (unchanged from parent).
- Backfilling the missing `devon-ui-developer` persona file.
- Automated/CI enforcement or contrast-ratio computation tooling.
- Performance measurement tooling — `ui.md` guardrail is advisory guidance, not a measured budget.

## Wave: DISCUSS / [REF] Definition of Done

1. Research precursor doc exists and is cited by the rule additions.
2. `ux.md` mobile tier merged, WCAG-cited, ≤ ~15 net lines, voice preserved.
3. `ui.md` mobile guardrails merged, ≤ ~8 net lines, no usability duplication.
4. `/phil:ux-review` SKILL.md must-fix list covers the mobile always-flag classes.
5. Dogfood fixture (one instance per mobile defect class) exercises the rule: 5/5 surfaced, 0 false
   always-flag on an intentionally-responsive-dense fixture.
6. No verbatim duplication across `ux.md`/`ui.md`/`react.md`; boundaries held.
7. All stories trace to the refined job; `jobs.yaml` updated.
8. Additions readable in-flow (< 2-min rule read preserved).
9. Reviewed against ACs + the research doc.

## Wave: DISCUSS / [REF] DoR validation

All 9 items pass with evidence: job traceability (refined job in `jobs.yaml`); testable ACs
(WCAG-anchored, fixture-measurable); KPIs with numeric targets (5/5, 0 false-positive); scope
right-sized (assessment PASS); no cross-context dependency; evidence base decided (research
precursor, D1); structure decided (D2); voice/length constraints explicit (D5); out-of-scope
enumerated. **Requirements completeness: ≥ 0.95.**

## Wave: DISCUSS / [REF] Machine artifacts (slice briefs)

- `docs/feature/mobile-web-standards/slices/slice-01-ux-mobile-tier.md`
- `docs/feature/mobile-web-standards/slices/slice-02-ui-mobile-guardrails.md`
- `docs/feature/mobile-web-standards/slices/slice-03-ux-review-coverage.md`

## Wave: DISCUSS / [REF] Wave decisions summary

- **Recommendation**: research precursor → extend `ux.md` + `ui.md` → update `/phil:ux-review`.
- **Evidence base**: research-first (D1); always-flag anchored to WCAG 2.2 (D3).
- **Structure**: extend existing rules, no new files (D2); job refined not duplicated (D4).
- **Constraints**: react.md voice, ≤ ~15 / ≤ ~8 net lines, "Do not flag" discipline (D5).
- **Upstream change**: appended a mobile-facet refinement to `catch-ux-violations-while-building-ui`
  in `docs/product/jobs.yaml` (SSOT write outside `discuss/`, user-approved; `refactor-tests` /
  `ux-standards-rule` precedent).

## Wave: DISCUSS / [REF] Handoff

Ready for DELIVER (this is a standards artifact — DESIGN/DISTILL are near-no-ops, per the parent's
handoff note: no architecture, no executable suite beyond reviewing the shipped additions against
the ACs, the research doc, and the dogfood fixture). **DELIVER order:** (0) research precursor →
(1) US-01 `ux.md` → (2) US-02 `ui.md` → (3) US-03 `/phil:ux-review`.
