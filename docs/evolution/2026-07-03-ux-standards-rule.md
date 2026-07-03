# Evolution — ux-standards-rule (`rules/ux.md` + `/phil:ux-review`)

**Finalized:** 2026-07-03 · **Branch:** `main` (trunk-based) · **Type:** user-facing plugin feature (path-scoped rule + prose skill)
**Waves run:** RESEARCH → DISCUSS → (DESIGN/DISTILL/DELIVER folded — standards artifact, no code to TDD) → verified via `nw-review`. SPIKE/DEVOPS skipped (no new mechanism, no infrastructure).

## Feature summary

A general-purpose UX standard for the plugin, delivered in two parts:

1. **`rules/ux.md`** — a path-scoped, auto-loaded rule capturing vendor-neutral UX usability and accessibility best practices (Nielsen's heuristics, WCAG 2.2, Laws of UX) as the **usability complement to `ui.md`** (aesthetics). Two tiers — *always-flag* (objective defects) vs *advisory* (judgment calls) — plus a "Do not flag" section.
2. **`/phil:ux-review`** — an on-demand command + skill that audits UI (`--changes` / file / dir) against `rules/ux.md` and writes a prioritized `.ux-review-backlog.md`. Modeled on `/phil:review-code`.

## Business context (JTBD)

`job_id: catch-ux-violations-while-building-ui` — persona **Devon**, a UI-building developer. When heads-down on behavior, Devon wants the plugin to flag concrete UX/usability and accessibility violations and name the preferred form, so objective defects (missing states, placeholder-as-label, color-only status, unlabeled controls, sub-24px targets) are caught before they ship — without holding all of Nielsen + WCAG in his head. The gap: the plugin covered visual *aesthetics* (`ui.md`) but nothing owned *usability/accessibility*.

## Key decisions

| ID | Decision | Where it lives |
|----|----------|----------------|
| D1 | Ship a **rule** now; **defer** a `/phil:ux-review` skill (later revisited and shipped, see below) | `journey.md` T1–T3 analysis |
| D2 | Length ~80 lines (hard ceiling ~90), terse, scannable, < 2 min read | `rules/ux.md` (66 lines) |
| D3 | Two tiers: *always-flag* (objective) vs *advisory* (judgment); close with "Do not flag" | `rules/ux.md` |
| D4 | Scope globs mirror `ui.md` | `rules/ux.md` frontmatter |
| D5 | Voice mirrors `react.md` — "flag the violation, name the preferred form" | `rules/ux.md` |
| D6 | Boundary: owns usability + accessibility; aesthetics stay in `ui.md`; `react.md`'s a11y bullet not restated | `rules/ux.md` |
| D7 | Guardrails baked in: no "max 7 items" cap (Miller misread); Postel scoped to input formatting only | `rules/ux.md` |
| D8 | Provenance line to the research doc; coverage = all 34 distilled principles, none inflated | `rules/ux.md` header |
| D9 | Job registered in `docs/product/jobs.yaml` (refactor-tests SSOT precedent) | `docs/product/jobs.yaml` |
| POST | Skill built after the rule shipped — modeled on `phil:review-code`, findings to `.ux-review-backlog.md`; `nw-forge` rejected (it forges nWave agents, not phil skills) | `skills/ux-review/SKILL.md` |

## Work completed

- **RESEARCH** (`nw-researcher`): cited, general-purpose UX doc → `docs/research/ux/general-ux-design-best-practices.md`; 17 sources, ends in a **34-principle distillation**; surfaced two conflicts to scope (Postel = input only; no "max 7 items" cap).
- **DISCUSS** (`/nw-discuss`, Luna): JTBD job story, lightweight touchpoint journey (T1–T3), 3 LeanUX user stories with Given-When-Then ACs, outcome KPIs, and `wave-decisions.md` (D1–D9). Registered the job in `jobs.yaml`.
- **DELIVER (rule)** (`f2aef72`, plugin 0.6.0): authored `rules/ux.md` by hand (no code to TDD). `nw-review` returned a clean PASS — all 34 principles represented, tiers correct, guardrails and WCAG numbers verified, no overlap with `ui.md`/`react.md`.
- **DELIVER (skill)** (`64095f7`, plugin 0.7.0): authored `commands/ux-review.md` + `skills/ux-review/SKILL.md` by mirroring `phil:review-code`; two severity bands map to the rule's two tiers; README updated.

## Lessons learned

1. **`nw-forge` and the DELIVER machinery mismatch standards/prose artifacts — twice.** `nw-forge` forges nWave *agents*; a path-scoped rule and a phil skill/command are neither. `/nw-discuss` fit (requirements), but DESIGN/DISTILL/DELIVER are near-no-ops with no architecture and no executable acceptance suite. Both artifacts were authored directly and verified by review. Recognizing the mismatch early — rather than running a code pipeline over Markdown — was the right call each time. (Mirrors the same lesson from `refactor-tests`.)
2. **Research conflicts are the highest-value output.** The two documented misreadings (Miller's "7±2" as an item cap; Postel as lax validation) became explicit *guardrails* baked into the rule wording. Encoding "what NOT to say" prevented shipping plausible-but-wrong guidance.
3. **The rule teaches the heuristic it follows.** "Recognition over recall" is both a flagged principle and the reason a path-scoped auto-loaded rule (zero recall to invoke) beat an invoked skill for the high-frequency editing touchpoint (T1).
4. **Verification for a standards artifact = review against ACs + source, not tests.** `nw-review` checking coverage/tiers/guardrails/WCAG-accuracy against the user stories and the research doc was the meaningful quality gate.

## Deferred / follow-ups

- **Live dogfood of `/phil:ux-review`** — this repo is Markdown-only; the skill needs a repo with real `.tsx/.css/...` to exercise the KPI-1 (6/6 defect classes) and KPI-2 (0 false hard-flags) fixtures.
- **Seeded dogfood fixtures** — the outcome KPIs reference a seeded defect fixture and a dense-expert-UI fixture that were specified but not built (no UI surface in-repo).
- **`plainlanguage.gov` verbatim checklist** — research noted a 301 redirect; the microcopy sub-rules were cross-referenced, not quoted verbatim.

## Permanent artifacts

- Shipped rule: `rules/ux.md`
- Shipped skill (prose): `commands/ux-review.md`, `skills/ux-review/SKILL.md`
- Research (already permanent): `docs/research/ux/general-ux-design-best-practices.md`
- Product SSOT: `docs/product/jobs.yaml` (job `catch-ux-violations-while-building-ui`)
- Full wave record (preserved workspace): `docs/feature/ux-standards-rule/discuss/{job-stories,journey,user-stories,outcome-kpis,wave-decisions}.md`
