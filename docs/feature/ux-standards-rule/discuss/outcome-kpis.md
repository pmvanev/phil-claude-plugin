# Outcome KPIs — ux-standards-rule

## Feature: ux-standards-rule

### Objective
A developer editing UI code with the phil plugin catches objective usability and accessibility
defects in-flow — without carrying the whole heuristic + WCAG checklist in their head — while the
rule stays scannable and quiet on judgment calls.

### Outcome KPIs

| # | Who | Does What | By How Much | Baseline | Measured By | Type |
|---|-----|-----------|-------------|----------|-------------|------|
| 1 | Devs editing UI files with the plugin active | Catch/fix objective UX/a11y defects during editing/review | 6/6 always-flag defect classes surfaced on the seeded fixture | 0 (no rule covers usability/a11y) | Dogfood fixture with one instance per defect class | Leading (primary) |
| 2 | Devs on dense/expert UIs | Get advisory guidance without false hard-flags | 0 always-flag false positives on the dense-UI fixture | n/a (rule absent) | Dense expert-UI dogfood fixture | Guardrail |
| 3 | Maintainers | Trust provenance + non-overlap with `ui.md`/`react.md` | 0 verbatim-duplicated principles; both research conflicts correctly scoped | n/a | Side-by-side review vs neighbouring rules + research | Guardrail |
| 4 | Devs (readability) | Read the whole rule quickly | <= ~90 lines, two tiers, under 2 min to read | react.md ~56 / ui.md ~23 lines | Line count + read-through | Guardrail |
| 5 | Rule (coverage) | Represent the research's distilled principles | 34/34 present across the two tiers, none inflated into a false rule | 0 | Map each `ux.md` line to a distillation item | Leading (secondary) |

### Metric Hierarchy
- **North Star**: KPI 1 — objective UX/a11y defects are caught in-flow where the plugin is active.
- **Leading indicators**: KPI 5 (coverage without bloat) predicts KPI 1.
- **Guardrail metrics**: KPI 2 (no false-flag noise), KPI 3 (provenance/non-overlap), KPI 4
  (scannability) — must not degrade in pursuit of the north star.

### Measurement Plan
| KPI | Data Source | Collection Method | Frequency | Owner |
|-----|------------|-------------------|-----------|-------|
| 1 | Seeded defect fixture | Run the rule over the fixture, count surfaced classes | Once at DELIVER, then on rule edits | Maintainer |
| 2 | Dense expert-UI fixture | Run the rule, count always-flag false positives | Once at DELIVER | Maintainer |
| 3 | `ux.md` vs `ui.md`/`react.md`/research | Manual side-by-side review | At DELIVER + review gate | Reviewer |
| 4 | `ux.md` | `wc -l` + read-through | At DELIVER | Maintainer |
| 5 | `ux.md` vs research distillation list | Line-to-principle mapping | At DELIVER | Maintainer |

### Hypothesis
We believe that an auto-loaded, two-tier `rules/ux.md` for developers editing UI code will let them
catch objective usability/accessibility defects in-flow. We will know this is true when the six
always-flag defect classes are surfaced on the seeded fixture (from a baseline of zero) with zero
false hard-flags on an intentionally-dense UI.

> **Note on measurement honesty (per outcome-kpi framework smell tests)**: the true outcome —
> fewer UX/a11y defects reaching production in downstream repos — is not instrumentable from a
> plugin. The fixture-based KPIs above are the strongest *leading* proxies measurable today.
