# Wave Decisions — ux-standards-rule (DISCUSS)

Feature type: **infrastructure / tooling** (a development-standards artifact) · JTBD: yes ·
walking skeleton: **no** (isolated, brownfield additive file) · UX research depth: lightweight
(deep external research already done — it is the input) · density: lean · 2026-07-02

Deliverable under design: a general-purpose **UX usability/accessibility standard** for this
plugin. Open question this wave answers: **rule, skill, or both**, and its length/detail/scope.

---

## Inputs

- **Primary**: `docs/research/ux/general-ux-design-best-practices.md` — 34 distilled, flaggable
  principles; two scoped conflicts (Postel = input only; no "max 7 items" cap).
- **Format exemplars**: `rules/ui.md` (aesthetics, path frontmatter), `rules/react.md` (voice:
  "flag the violation, name the preferred form", Prefer/Over/Why tables, closing "Do not flag").
- **SSOT**: `docs/product/jobs.yaml` (job registered this wave).

## DIVERGE status

No `docs/feature/ux-standards-rule/diverge/` directory exists. The cited research doc plus the
user's brainstorming served as the de-facto divergence input. **Risk (LOW)**: no formal
ODI/option scoring was run; mitigated because the solution space here is narrow (a standards
artifact) and the research already enumerates the raw material and its conflicts.

## Scope Assessment: PASS

Right-sized. **3 thin stories over 1 file** (`rules/ux.md`, ~80 lines), **1 context** (the rules
system), 0 cross-context integration, well under 2 weeks. Walking skeleton pre-decided "no"
(isolated additive file); US-01 is the thinnest end-to-end slice (rule exists + always-flag tier).
No split required.

## Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | Ship a **rule** `rules/ux.md` now; **defer** a `/phil:ux-review` skill. | Value concentrates at the editing touchpoint (T1) and is covered for free during review (T2); the audit touchpoint (T3) is low-frequency, partly served by `/phil:review-code`, and building it now is speculative. CLAUDE.md: "Empirical design over speculation." See `journey.md`. |
| D2 | **Length** ~80 lines (hard ceiling ~90); terse, scannable, < 2 min read. | Matches the plugin's rule norm (react.md ~56, ui.md ~23); a rule that isn't scannable won't be internalised. |
| D3 | **Two tiers**: "always-flag" (objective defects) vs "advisory" (judgment calls); close with a **"Do not flag"** section. | Directly from the research Recommendations; keeps signal high and prevents false-flag noise on intentionally-dense expert tools. |
| D4 | **Scope globs mirror `ui.md`**: `**/*.{tsx,jsx,vue,svelte,css,scss,sass,less,html}` + `components/pages/layouts/styles`. | Same surface the aesthetics rule already governs; consistent auto-load behaviour. |
| D5 | **Voice mirrors `react.md`**: "flag the violation, name the preferred form", Prefer/Over/Why tables, closing "Do not flag". | Consistency across the plugin's rule set; proven format. |
| D6 | **Boundary**: `ux.md` owns **usability + accessibility**; **aesthetics stay in `ui.md`**; `react.md`'s React-specific a11y bullet is **not** restated. | Complement, not duplicate. Avoids contradicting `ui.md`'s "rich aesthetics" push and repeating `react.md`. |
| D7 | **Guardrails baked into wording**: never a "max 7 items" cap (Conflict 2); Postel scoped to **input formatting only** (Conflict 1). | The research explicitly flags both as common misreadings; encoding them would ship known-wrong guidance. |
| D8 | **Provenance line** citing the research doc; **coverage target** = represent all 34 distilled principles across the two tiers without inflating any into a false rule. | Traceability + completeness without bloat. |
| D9 | **Job registered in `docs/product/jobs.yaml`** (`catch-ux-violations-while-building-ui`); all stories trace to it. | DoR job-traceability is a hard gate; precedent set by the `refactor-tests` DISCUSS wave (which bootstrapped the same SSOT). |

## Always-flag vs advisory (mapping of the 34 principles)

- **Always-flag (objective defects)**: #2 missing states · #4 unguarded destructive action ·
  #8 raw error codes/traces as copy · #9 placeholder-as-label · #10 validate-on-keystroke /
  distant-only summary · #13 radio/checkbox by exclusivity (+ default) · #14 controls as action
  triggers · #25 keyboard operability + visible focus + no traps · #26 contrast minimums ·
  #27 color-alone meaning · #28 target size >= 24px · #29 text alternatives / accessible names /
  semantic structure.
- **Advisory (judgment calls)**: #1 feedback timing · #3 empty-state copy · #5 exits/undo ·
  #6 error prevention · #7 error-message quality · #11 forgiving input (input-only) ·
  #12 minimal required fields · #15 sensible defaults · #16 reduce choice / presets ·
  #17 progressive disclosure (<=2 levels) · #18 recognition over recall / chunking ·
  #19 platform conventions · #20 consistent vocabulary · #21-22 Gestalt grouping/similarity ·
  #23 scannability/headings · #24 visual hierarchy · #30 plain language / action labels ·
  #31 minimalism · #32 aesthetic-usability (defer to `ui.md`) · #33 progress / serial position ·
  #34 optimistic UI.

## Wave decisions summary

- **Recommendation**: **rule now, skill deferred** (D1). Ship `rules/ux.md`.
- **Length/detail**: ~80 lines, terse, two-tier, react.md voice (D2, D3, D5).
- **Scope**: usability + accessibility; globs mirror `ui.md`; boundary with `ui.md`/`react.md` (D4, D6).
- **Guardrails**: no "7 items" cap; Postel input-only; provenance + 34-principle coverage (D7, D8).
- **Upstream changes**: appended one validated job to `docs/product/jobs.yaml` (D9) — flagged in
  the handoff as a write outside `discuss/`, consistent with the `refactor-tests` precedent.

## Decision points surfaced to the user

1. **Rule now, skill deferred** — recommended (D1). Confirm, or ask for the `/phil:ux-review` skill
   in this iteration (evidence says defer).
2. **~80-line ceiling** (D2) — confirm the length/detail target, or request a longer, more
   didactic reference rule.
3. **Writing to `jobs.yaml`** (D9) — a product-SSOT write outside `discuss/`. Done under the
   `refactor-tests` precedent and the hard job-traceability gate; flag if the SSOT should instead
   stay feature-local.

## Handoff

Requirements are ready for the DELIVER step that authors `rules/ux.md` (this is a standards
artifact, not an application feature — DESIGN/DISTILL are near-no-ops; there is no architecture or
executable acceptance suite beyond reviewing the shipped rule against the ACs and the research).
Artifacts: `job-stories.md`, `journey.md`, `user-stories.md`, `outcome-kpis.md`, this file.
