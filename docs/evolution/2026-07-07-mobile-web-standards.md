# Evolution — mobile-web-standards (`rules/ux.md` + `rules/ui.md` + `/phil:ux-review`)

**Finalized:** 2026-07-07 · **Branch:** `main` (trunk-based) · **Type:** standards feature (path-scoped rules + prose skill), extends `ux-standards-rule`
**Waves run:** DISCUSS → RESEARCH (precursor) → DELIVER (3 slices) → verified by review-against-ACs. DESIGN/DISTILL folded (standards artifact, no code to TDD); SPIKE/DEVOPS skipped (no new mechanism, no infrastructure).

## Feature summary

Adds **mobile web coverage** to the plugin's design standards, which previously covered mobile only via the touch-target line in `ux.md`. Delivered by **extending** the two existing rules rather than adding new files:

1. **`rules/ux.md`** — a *Mobile & responsive* always-flag table (5 WCAG 2.2 SC), a *Mobile & touch* advisory bullet, and mobile *Do-not-flag* exemptions.
2. **`rules/ui.md`** — a *Mobile guardrails* section scoping its aesthetic advice for small touch screens and constrained devices, with an explicit boundary back to `ux.md`.
3. **`skills/ux-review/SKILL.md`** — the `/phil:ux-review` audit path gains the same 5 mobile always-flag items so the on-demand touchpoint (T3) catches them, not just in-flow editing.

Backed by a new research precursor, `docs/research/ux/mobile-web-best-practices.md`.

## Business context (JTBD)

`job_id: catch-ux-violations-while-building-ui` — persona **Devon**, refined this feature with a **mobile facet** (recorded in `docs/product/jobs.yaml`) rather than a duplicate job. Devon's job is unchanged — flag UI defects in-flow and name the preferred form — but its surface now explicitly includes mobile web rendering: reflow, zoom, orientation, pointer gestures, motion, and touch. The gap: only touch-target size was covered; reflow/orientation/gesture/motion had no owner, and `ui.md`'s aesthetic push implicitly assumed desktop.

## Key decisions

| ID | Decision | Where it lives |
|----|----------|----------------|
| D1 | **Research wave first** — author a citable evidence base before rule wording | `docs/research/ux/mobile-web-best-practices.md` |
| D2 | **Extend `ux.md` + `ui.md`; no new rule files** — mobile cuts across both existing axes | `rules/ux.md`, `rules/ui.md` |
| D3 | **Always-flag ⊆ citable WCAG 2.2 SC**; advisory + completeness from research | `rules/ux.md` Mobile & responsive table |
| D4 | **Refine the existing job**, don't duplicate (redesign-tests precedent) | `docs/product/jobs.yaml` |
| D5 | Length/voice discipline: react.md voice, ≤ ~15 (`ux.md`) / ≤ ~8 (`ui.md`) net lines | `rules/ux.md` (+13), `rules/ui.md` (+10) |
| D6 | **Update `/phil:ux-review`** to cover the new always-flag items (parent deferred the skill; it now exists) | `skills/ux-review/SKILL.md` |

## Work completed

- **DISCUSS** (`/nw-discuss`, Luna, `6857ec3`): mobile facet of the parent job, 6 locked decisions, 3 LeanUX stories with WCAG-anchored ACs + elevator pitches, KPIs, DoR, scope-assessment PASS; 3 slice briefs; refined `jobs.yaml`. Consolidated in `feature-delta.md`.
- **RESEARCH precursor** (`nw-researcher`, `a38eb8d`): `docs/research/ux/mobile-web-best-practices.md` — 17 sources (avg reputation ~0.97), High confidence; 6 ALWAYS-FLAG principles (WCAG 1.4.10 / 1.4.4 / 1.3.4 / 2.5.1 / 2.5.4, plus 2.5.8 cross-referenced), 12 ADVISORY heuristics, 5 conflicts, 7 knowledge gaps logged. Mirrors the sibling general-ux doc.
- **DELIVER slice 1** (`1f186b3`): `rules/ux.md` Mobile & responsive tier (+13 lines).
- **DELIVER slice 2** (`9737d29`): `rules/ui.md` Mobile guardrails (+10 lines).
- **DELIVER slice 3** (`83a3193`): `/phil:ux-review` must-fix + advisory + do-not-flag mobile coverage (+8 net).

## Lessons learned

1. **Research conflicts are the highest-value output — again.** As with `ux-standards-rule`, the doc's 5 flagged misreadings became the rule's guardrails: 2-D content exempt from reflow, essential-orientation exempt from 1.3.4, "mobile-first" is a workflow not a defect, breakpoints are content-driven not device-cargo-culted, and 44/48px is HIG *comfort* — not a WCAG requirement (the floor is 24px). Encoding "what NOT to flag" prevented shipping plausible-but-wrong mobile guidance.
2. **Extending beat forking.** Mobile concerns cross the ux/ui axis, but splitting into `mobile-ux.md`/`mobile-ui.md` would have created a 4-file matrix and a new "is this defect mobile?" boundary. Placing each concern where its concern already lives (usability→`ux.md`, aesthetics→`ui.md`) kept the axis clean and let `/phil:ux-review` inherit the `ux.md` additions for free.
3. **Anchor objective claims to a standard you can cite.** Every always-flag mobile item maps to a WCAG SC number, so the rule stays defensible without re-litigating; the softer, single-sourced heuristics were deliberately kept in the advisory tier (and their gaps logged in the research doc), not promoted above their evidence.
4. **Standards verification = review against ACs + source, not tests.** Confirmed structurally: all 5 SC present in both rule and skill, skill mirrors rule 1:1 with no invented flags, ux/ui boundary holds with no verbatim duplication, each slice within its line budget.

## Deferred / follow-ups

- **Seeded dogfood fixture** — the KPI ("5/5 mobile defect classes surfaced; 0 false always-flag on a responsive-dense fixture") was specified but not built; this repo is Markdown-only with no `.tsx/.css` surface to exercise it. Same deferral as the parent.
- **7 research knowledge gaps** — single-sourced advisory claims (safe-area insets, hover-on-touch, `prefers-reduced-motion` vestibular rationale, iOS 16px input-zoom, `inputmode`/`autocomplete`, content-driven breakpoints, thumb-zone geography). Each names what a follow-up fetch should target.
- **Missing persona file** — `docs/product/personas/devon-ui-developer.yaml` is referenced by `jobs.yaml` but doesn't exist (pre-existing gap, inherited from `ux-standards-rule`; explicitly out of scope here).

## Permanent artifacts

- Extended rules: `rules/ux.md`, `rules/ui.md`
- Extended skill (prose): `skills/ux-review/SKILL.md`
- Research (already permanent): `docs/research/ux/mobile-web-best-practices.md`
- Product SSOT: `docs/product/jobs.yaml` (mobile facet on `catch-ux-violations-while-building-ui`)
- Full wave record (preserved workspace): `docs/feature/mobile-web-standards/feature-delta.md`, `docs/feature/mobile-web-standards/slices/slice-0{1,2,3}-*.md`
