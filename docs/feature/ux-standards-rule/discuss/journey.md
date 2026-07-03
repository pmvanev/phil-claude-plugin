# Lightweight Journey — ux-standards-rule

Not an emotional-arc journey (tooling feature). This maps the developer's workflow touchpoints
where a UX standard could fire, and uses that to make an evidence-based **rule vs skill vs both**
recommendation.

## Developer touchpoints

| # | Touchpoint | Frequency | What Devon is doing | Rule (auto-load) helps? | Skill (invoked) helps? |
|---|-----------|-----------|---------------------|------------------------|------------------------|
| T1 | Editing/creating a UI component, heads-down | Very high | Writing `.tsx`/`.vue`/`.css` — Claude generates/edits UI code inline | **Yes — primary.** Fires exactly on the matching file with zero recall to invoke | No — nothing to invoke; interrupts flow |
| T2 | Review pass over a UI change | Medium | Running `/phil:review-code`; rule auto-loads for matching files under review | **Yes.** Rule content is already in context during review | Partial — `/phil:review-code` already exists and would carry the rule |
| T3 | Deliberate, whole-screen UX audit | Low | Stepping back to check a finished flow end-to-end (JS-3) | Partial — rule is present but not a focused driver | **Yes** — a `/phil:ux-review` skill could drive a deeper, screen-level pass |

## Analysis

- **The value concentrates at T1**, the highest-frequency touchpoint. A path-scoped **rule**
  auto-loads precisely when Devon touches UI files, needs **zero recall to invoke** (recognition
  over recall — the same heuristic #6 the rule teaches applies to Devon), and matches the
  established plugin pattern (`ui.md`, `react.md`). The 34 distilled principles are almost all
  "flag the violation, name the preferred form" checks — exactly what a path-scoped rule does.
- **T2 is covered for free**: an auto-loaded rule is in context during `/phil:review-code`, so a
  rule serves both the write and review touchpoints without extra machinery.
- **T3 is the only touchpoint a skill serves better** — and it is low-frequency, partly covered
  by `/phil:review-code` today, and building it now is speculative. This repo's CLAUDE.md is
  explicit: *"Empirical design over speculation."* Ship the rule; add the skill only if evidence
  shows the rule alone leaves the audit job unmet (YAGNI).

## Recommendation: **RULE now, skill deferred**

Ship `rules/ux.md` as an auto-loaded, path-scoped rule (T1 + T2). Defer `/phil:ux-review` (T3)
as a documented future addition, revisited only if the deliberate-audit job proves underserved.

This **validates** the pre-set brainstorming recommendation and adds the touchpoint evidence
behind it. One challenge raised and resolved: the rule must **complement, not duplicate**
`ui.md` (aesthetics) and `react.md` (its single React-specific a11y bullet) — see the boundary
decision in `wave-decisions.md`.
