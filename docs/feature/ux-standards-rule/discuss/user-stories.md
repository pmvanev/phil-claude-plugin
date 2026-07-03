<!-- markdownlint-disable MD024 -->
# User Stories — ux-standards-rule

The deliverable is a single auto-loaded rule, `rules/ux.md` (~80 lines). Per Elephant Carpaccio
this is **one file sliced into three thin, independently verifiable outcomes**, not three files.
All three trace to `job_id: catch-ux-violations-while-building-ui`.

## System Constraints (cross-cutting)

- **Voice**: match `react.md` — "flag the violation, name the preferred form", Prefer/Over/Why
  tables, a closing **"Do not flag"** section.
- **Scope globs**: mirror `ui.md` — `**/*.{tsx,jsx,vue,svelte,css,scss,sass,less,html}`,
  `**/components/**`, `**/pages/**`, `**/layouts/**`, `**/styles/**`.
- **Length/detail**: terse and scannable; target ~80 lines (react.md ≈ 56, ui.md ≈ 23), hard
  ceiling ~90; readable in under 2 minutes.
- **Provenance**: cite `docs/research/ux/general-ux-design-best-practices.md` as the source.
- **Boundary**: owns **usability + accessibility**; defers **aesthetics** to `ui.md`; does not
  restate `react.md`'s React-specific a11y bullet.
- **Guardrails (must-not)**: never encode a "max 7 items" cap (research Conflict 2); reference
  Postel's Law only scoped to **input formatting**, never as lax validation (research Conflict 1).
- **Solution-neutral within remit**: describes observable UI outcomes, not framework specifics.

---

## US-01: Auto-loaded rule flags objective usability/accessibility defects *(walking skeleton)*

### Problem
Devon edits a data-driven React component with no automated check for usability or accessibility.
An input labeled only by its placeholder, a status shown by color alone, or a one-click unguarded
delete reaches manual review or production, because **no rule owns usability/accessibility** today.

### Who
- Devon, UI-building developer | editing files matching the UI globs | wants obvious UX/a11y
  defects caught in-flow without recalling the whole heuristic + WCAG checklist.

### Solution
A path-scoped rule `rules/ux.md` that auto-loads on UI files and, in an **"always-flag"** tier,
names each objective violation and its preferred form.

### Elevator Pitch
- **Before**: Devon edits UI files with no automated UX/a11y feedback — usability defects surface
  only in manual review or production.
- **After**: Devon edits `LoginForm.tsx` → the plugin flags *"email input is labeled only by
  `placeholder` — add a persistent `<label for>`"* and *"Delete button has no confirm or undo"*,
  each citing the principle and the preferred form.
- **Decision enabled**: whether to fix each flagged defect before committing.

### Domain Examples
1. **Happy path** — `<input placeholder="Email">` with no `<label>` → flagged: "placeholder is
   not a label; add a persistent visible label" (distillation #9).
2. **Edge case** — a `<span class="status status--red">` conveying "failed" with color only →
   flagged: "status by color alone; pair with text/icon" (#27).
3. **Error/boundary** — a group of `<input type="checkbox">` where only one may be selected →
   flagged: "single-choice set should be radios with a default" (#13); and a `<button>Delete</button>`
   with no confirm/undo → flagged (#4).

### UAT Scenarios (BDD)
#### Scenario: Placeholder-only label is flagged with the preferred form
Given Devon edits a component with an input whose only label is a `placeholder`
When the UX rule is applied
Then the placeholder-as-label defect is flagged and a persistent visible `<label>` is named as the preferred form

#### Scenario: Color-only status is flagged
Given Devon edits a view that signals success/failure using color alone
When the UX rule is applied
Then the color-alone defect is flagged and pairing color with text or an icon is named as the fix

#### Scenario: Single-select checkbox group is flagged as a radio set
Given Devon edits a set of checkboxes where exactly one option may be chosen
When the UX rule is applied
Then the misuse is flagged and radio buttons with a sensible default are named as the preferred form

#### Scenario: Missing data-view states are flagged
Given Devon edits a data-driven component that renders results but has no loading, empty, or error state
When the UX rule is applied
Then the missing states are flagged (never assume data loads successfully)

#### Scenario: Unguarded destructive action is flagged
Given Devon edits a one-click Delete with no undo and no confirmation
When the UX rule is applied
Then the unguarded destructive action is flagged and undo (preferred) or confirmation is named

#### Scenario: Sub-minimum touch target is flagged
Given Devon edits an interactive control smaller than 24x24 CSS px with no spacing exception
When the UX rule is applied
Then the target-size defect is flagged against WCAG 2.5.8

### Acceptance Criteria
- [ ] `rules/ux.md` exists with `paths` frontmatter matching the UI globs (mirrors `ui.md`).
- [ ] An "always-flag" tier names each objective defect **and** its preferred form.
- [ ] The always-flag tier covers, at minimum: missing UI states; placeholder-as-label; unguarded
      destructive action; validate-on-keystroke / distant-only error summary; keyboard
      operability + visible focus + no focus traps; contrast minimums; color-alone meaning;
      target size >= 24px; text alternatives / accessible names / semantic structure;
      radio/checkbox misuse; controls used as action triggers.
- [ ] Each flag reads as "flag the violation, name the preferred form" (react.md voice).

### Outcome KPIs
- **Who**: developers editing UI files in a repo with the plugin active.
- **Does what**: catch and fix objective usability/accessibility defects during editing/review.
- **By how much**: the six always-flag defect classes above are surfaced on a seeded fixture
  (6/6), where the baseline coverage is 0.
- **Measured by**: a dogfood fixture file containing one instance of each defect class.
- **Baseline**: no rule covers usability/accessibility today (0 coverage).

### Technical Notes
- Additive, isolated, brownfield (no walking-skeleton wiring). Auto-discovered by the plugin's
  existing rule loader; no manifest change (per `ui.md`/`react.md` precedent).

---

## US-02: Advisory tier + "Do not flag" section keep guidance signal high

### Problem
Judgment-call principles (visual hierarchy, progressive disclosure, minimalism, chunking) are
real UX guidance but wrong to hard-block on — and expert-tool UIs are legitimately dense. Without
a separation, the rule either nags on every call or stays silent; both erode trust.

### Who
- Devon building an intentionally information-dense expert tool | wants advisory nudges, not
  false "too many options" flags on a UI that is dense by design.

### Solution
A second **"advisory"** tier for judgment-call principles, plus a closing **"Do not flag"**
section that scopes the rule away from known false positives.

### Elevator Pitch
- **Before**: a usability rule risks flagging every judgment call, so Devon learns to ignore it —
  or it is so terse it offers no guidance on hierarchy/disclosure.
- **After**: Devon edits a dense trading dashboard → the rule offers advisory guidance on visual
  hierarchy but **does not** flag "too many options", and never cites a "max 7 items" cap.
- **Decision enabled**: which advisory nudges are worth acting on, without noise on intentional density.

### Domain Examples
1. **Happy path** — a screen where every element is bold/primary → advisory: "establish one clear
   visual hierarchy; if everything is emphasized, nothing is" (#24) — guidance, not a hard flag.
2. **Edge case** — a Bloomberg-style dense data grid → **not** flagged for density; the "Do not
   flag" section covers intentional expert-tool density (Aesthetic-Usability / minimalism #31-32).
3. **Boundary** — a nav with 12 items → **not** flagged; the rule never cites "max 7 items"
   (research Conflict 2); at most advises chunking/grouping.

### UAT Scenarios (BDD)
#### Scenario: Judgment-call principle is offered as advice, not a hard flag
Given Devon edits a screen with weak visual hierarchy
When the UX rule is applied
Then visual hierarchy appears as advisory guidance, distinct from the always-flag tier

#### Scenario: Intentionally dense expert UI is not false-flagged
Given Devon edits an information-dense expert tool that is dense by design
When the UX rule is applied
Then it is not flagged for "too many options", per the "Do not flag" section

#### Scenario: The debunked item-count cap is never cited
Given Devon edits a navigation with more than seven items
When the UX rule is applied
Then no "max 7 items" cap is cited; at most chunking/grouping is advised

### Acceptance Criteria
- [ ] `rules/ux.md` groups principles into two tiers: **always-flag** (objective) and
      **advisory** (judgment calls), clearly separated.
- [ ] A closing **"Do not flag"** section lists at least: intentional expert-tool density;
      aesthetics owned by `ui.md`; style owned by the formatter.
- [ ] The rule contains no "max 7 items" (or equivalent) count cap anywhere.

### Outcome KPIs
- **Who**: developers using the rule on dense/expert UIs.
- **Does what**: receive advisory guidance without false always-flag noise.
- **By how much**: 0 always-flag false positives on a seeded intentionally-dense fixture.
- **Measured by**: a dogfood fixture of a dense expert UI.
- **Baseline**: n/a (rule does not exist yet).

### Technical Notes
- Advisory vs always-flag split is the primary mechanism for keeping signal high; ties to the
  research Recommendations ("group by always-flag vs advisory").

---

## US-03: Provenance, boundary, and misuse guardrails

### Problem
The rule can drift from its cited research, silently overlap `ui.md`/`react.md`, or re-import the
two misreadings the research explicitly warns against (Miller "7+/-2" as a cap; Postel as lax
validation). Any of these erodes trust or contradicts a neighbouring rule.

### Who
- Devon, and future maintainers of the plugin | need to trust the rule traces to cited evidence
  and does not fight `ui.md` or `react.md`.

### Solution
A provenance pointer to the research doc; an explicit boundary statement (usability/accessibility
here; aesthetics in `ui.md`; React-specific a11y bullet stays in `react.md`); and the two scoped
guardrails baked into the wording.

### Elevator Pitch
- **Before**: the rule risks duplicating `ui.md`, contradicting `react.md`, or reviving the
  debunked "7 items" cap and lax-Postel readings.
- **After**: a maintainer opens `rules/ux.md` → sees a one-line pointer to the research doc, a
  boundary note ("aesthetics: see `ui.md`"), Postel scoped to input only, and no item-count cap.
- **Decision enabled**: whether the rule is trustworthy and non-overlapping enough to ship.

### Domain Examples
1. **Happy path** — the rule's header cites `docs/research/ux/general-ux-design-best-practices.md`.
2. **Edge case** — `ui.md` says "use rich aesthetics / dynamic animations"; `ux.md` does not
   restate aesthetics and instead notes "aesthetics: see `ui.md`; never let polish mask a usability
   defect" (#32), so the two rules complement rather than conflict.
3. **Boundary** — Postel appears only as "accept forgiving input formats and normalize internally",
   explicitly **not** as a license for lax validation (research Conflict 1).

### UAT Scenarios (BDD)
#### Scenario: The rule cites its research provenance
Given a maintainer opens `rules/ux.md`
When they read the header
Then it points to `docs/research/ux/general-ux-design-best-practices.md` as the source

#### Scenario: Usability rule does not duplicate the aesthetics rule
Given `ui.md` already owns visual aesthetics
When `rules/ux.md` is reviewed against it
Then `ux.md` covers usability/accessibility and defers aesthetics to `ui.md` without restating it

#### Scenario: Postel's Law is scoped to input only
Given the rule references forgiving input handling
When that guidance is read
Then it is scoped to input formatting and normalization, never presented as lax validation

### Acceptance Criteria
- [ ] `rules/ux.md` cites the research doc path in its header/provenance line.
- [ ] The rule states its boundary with `ui.md` (aesthetics) and does not duplicate `react.md`'s
      React-specific a11y bullet.
- [ ] Postel's Law, if referenced, is scoped to input formatting/normalization only.
- [ ] No principle is copied verbatim from `ui.md` or `react.md` (complement, not repeat).

### Outcome KPIs
- **Who**: plugin maintainers and Devon.
- **Does what**: trust the rule's provenance and non-overlap with neighbouring rules.
- **By how much**: 0 verbatim-duplicated principles across `ui.md`/`react.md`; 100% of the two
  research conflicts (7+/-2 cap, lax Postel) correctly scoped.
- **Measured by**: side-by-side review of `ux.md` against `ui.md`, `react.md`, and the research.
- **Baseline**: n/a (rule does not exist yet).

### Technical Notes
- Coverage target: represent the research's 34 distilled principles across the two tiers without
  inflating any into a false rule and without dropping any silently.
