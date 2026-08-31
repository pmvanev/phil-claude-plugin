---
name: ux-review
description: Skill bundle for phil:ux-review command — UX usability & accessibility audit against rules/ux.md with a prioritized findings backlog
---

# UX Review

You are auditing UI against the usability and accessibility standard in `${CLAUDE_PLUGIN_ROOT}/rules/ux.md`. Your job is to find UX violations and produce a prioritized, actionable backlog. `ux.md` owns usability + accessibility, and since 2026-08-31 the motion, effect-cost and small-scale legibility guardrails that used to sit in `ui.md`. **The taste questions belong to `ui.md`** — which colour, which typeface, whether an animation is attractive — and React idioms to `react.md`; do not review against those here. The split is by checkability, not by subject: an animation's reduced-motion variant and its frame cost are yours, its appeal is not.

`ux.md` is the source of truth for what to flag and how to phrase the fix. It defines two tiers and a "Do not flag" section — mirror them:

- **Always-flag** (objective defects) → severity **must-fix**
- **Advisory** (judgment calls) → severity **consider**
- **Do not flag** → never raise (intentional expert-tool density, aesthetic *taste* owned by `ui.md` — not an effect's motion variant or frame cost, which are yours — `react.md`'s a11y bullet, formatter's style, any "max 7 items" cap)

## Parse the Argument

Determine what `$ARGUMENTS` refers to:

| Pattern | Type | Example |
|---------|------|---------|
| `--changes` | Latest git changes | `--changes` |
| Has a file extension | File path | `src/LoginForm.tsx` |
| Ends with `/` or a directory with no extension | Directory path | `src/`, `src/components` |
| No argument | Default to `--changes` | |

---

## Step 1: Gather UI Code

Restrict to UI files — the surface `ux.md` governs: `**/*.{tsx,jsx,vue,svelte,css,scss,sass,less,html}` and anything under `components/`, `pages/`, `layouts/`, `styles/`. Skip pure logic, config, and test files.

### `--changes` (default)
Run `git diff HEAD~1 --name-only`, filter to UI files, read each in full, and run `git diff HEAD~1 -- <file>` to see what changed.

### File Path
Read the entire file.

### Directory Path
Glob recursively for UI files. Read each. For large directories (>20 files), use an Explore agent to parallelize reading.

---

## Step 2: Analyze Against `rules/ux.md`

Read `${CLAUDE_PLUGIN_ROOT}/rules/ux.md` first so your findings and wording trace to it. For each file, check the tiers below. **Static review catches most defects; some need the rendered UI** — when a check depends on computed styles or live behavior (contrast ratios, actual focus visibility, real target size), flag it as must-fix only when the source makes it clear, otherwise raise a **consider** item asking the author to verify at runtime. Say which.

### Must-fix — objective defects (always-flag tier)

**Accessibility**
- Interactive behavior on a non-semantic element (`onClick` on a `<div>`/`<span>`), no keyboard handler, or a likely focus trap → real button/link, keyboard-operable, visible focus, no trap.
- Meaning by color alone (class names / inline styles like `status--red` with no text or icon) → pair color with text/icon/shape.
- Text contrast < 4.5:1 (< 3:1 large) or UI/icon contrast < 3:1 where colors are visible in source → meet WCAG AA.
- Interactive target < 24×24 CSS px with no spacing exception → ≥ 24×24px (WCAG 2.5.8).
- Icon-only control, image, or region with no accessible name / alt / semantics → provide text alternatives, accessible names, semantic structure.

**State & feedback**
- Data-driven view rendering results with no loading / empty / error state → design every state.
- One-click destructive or irreversible action with no undo or confirmation → undo (preferred) or confirmation.

**Forms & controls**
- Input labeled only by `placeholder` → persistent visible `<label>`.
- Validation on every keystroke, or only in a distant summary → validate inline after the field loses focus, message adjacent.
- Checkbox set where exactly one option is valid → radio / single-select with a sensible default.
- Checkbox/radio wired to trigger an action → use a button; toggles are for instant binary on/off only.
- Raw error code, stack trace, or "Invalid input" shown to the user → specific, human, actionable message that preserves input.

**Mobile & responsive**
- Layout that forces two-dimensional scrolling of ordinary content at ~320 CSS px width / 400% zoom (fixed pixel-width container wider than the viewport, page-level `overflow-x`) → reflow to one column with fluid units (WCAG 1.4.10); 2-D content (tables, maps, diagrams) is exempt. **Verify at runtime** — depends on rendered layout.
- Zoom disabled via `user-scalable=no` / `maximum-scale=1`, or text that can't resize to 200% → allow pinch/browser zoom (WCAG 1.4.4). The `viewport` meta is statically checkable; resize behavior is **verify at runtime**.
- View locked to one orientation with no essential-use reason → support portrait and landscape (WCAG 1.3.4).
- Path or multipoint gesture (swipe-path, pinch, drag) as the only way to act → also provide a single-pointer tap/click/long-press alternative (WCAG 2.5.1).
- Action triggered only by device motion (shake, tilt) → provide an equivalent on-screen control and a way to disable it (WCAG 2.5.4).

### Consider — judgment calls (advisory tier)

Raise these as guidance, not hard blocks: feedback timing (~1s / ~10s thresholds), empty-state copy that guides the next action, error prevention before messages, forgiving input formats (input only), minimal required fields, sensible defaults, reduce/segment choices + presets, progressive disclosure (≤ 2 levels), recognition over recall / chunking, platform conventions, consistent vocabulary, Gestalt grouping, scannability/headings, one clear visual hierarchy, plain action-labeled copy, progress toward goals, optimistic UI for reversible actions only, mobile & touch advisories (viewport meta, fluid / content-driven breakpoints, safe-area insets, thumb reach, hover-on-touch alternatives, correct input types / on-screen-keyboard handling, ≥ 16px form inputs).

For each finding, name the **specific `ux.md` principle** it violates and the **preferred form** as the fix.

---

## Step 3: Write the Backlog

Write findings to `.ux-review-backlog.md` in the project root. Use this exact format:

```markdown
# UX Review Backlog

Generated: {date}
Scope: {argument — e.g., "--changes", "src/components/", "src/LoginForm.tsx"}
Standard: rules/ux.md

## Summary

- **Total items**: {count}
- **Must-fix (objective defects)**: {count}
- **Consider (advisory)**: {count}

## Backlog

### [{id}] {short title} — {one-line description}

- **File**: `{file-path}`
- **Lines**: {start}-{end}
- **Severity**: must-fix | consider
- **Principle**: {the ux.md rule violated, e.g. "placeholder-as-label", "color-alone meaning (WCAG 1.4.1)"}
- **Preferred form**: {the fix, in ux.md's words}
- **Verify at runtime**: {yes/no — yes when the defect depends on rendered styles or live behavior}
- **Status**: pending
```

Rules for the backlog:
- IDs are sequential: `U001`, `U002`, etc.
- Sort must-fix first, then consider; within each, by file path.
- Each item is a **single, atomic fix** — not a bundle.
- Principle and preferred form must trace to `ux.md`; do not invent flags it doesn't contain.

---

## Step 4: Report

After writing the backlog, report to the user:

1. Total findings by severity (must-fix / consider).
2. Top 5 must-fix items with brief descriptions.
3. The path to the backlog file.
4. Note any items marked "verify at runtime" that need a rendered check.

---

## What NOT to Flag

- Anything in `ux.md`'s **"Do not flag"** section: intentional density in expert/pro tools, established conventions, aesthetic taste (owned by `ui.md`), React-specific a11y (owned by `react.md`), and formatter-owned style.
- A **"max 7 items" (or equivalent) count cap** — `ux.md` explicitly rejects it; at most advise chunking.
- **Inherently 2-D content** (tables, maps, diagrams, indented code) for reflow, and **orientation-locked views where the orientation is essential** — `ux.md` exempts both. "Mobile-first" is a workflow, not a defect; and don't cite WCAG for sub-44/48px targets (24px is the floor; 44/48px are HIG comfort guidance).
- Visual/aesthetic *preferences* — which palette, which typeface, whether an animation is attractive — are `ui.md`'s remit, not a UX defect. **A missing reduced-motion variant, an effect that burns frames on a low-end phone, and type that stops reading at mobile scale are not preferences** and are in scope; see `ux.md`'s reduced-motion row and its motion/legibility advisories.
- Hypothetical issues in code you don't fully understand — when uncertain, skip.

**Be precise, not exhaustive.** A backlog with 8 well-identified, traceable findings beats one with 40 vague ones.

---

## Self-test (regression gate)

`skills/ux-review/self-test/` holds golden fixtures that pin these behaviors: the backlog written from
two unambiguous always-flag defects (01, walking skeleton), the motion/taste boundary held inside a
single stylesheet (02), an item count never used as a finding (03), the reflow exemption applied to a
wide table rather than rediscovered as a symptom (04), a 30px target cited to the platform guidance and
never to WCAG (05), an unresolvable contrast deferred to a rendered check rather than asserted or
silently passed (06), non-UI files skipped without being reported clean (07), and an obvious two-token
fix left unapplied because this command reports and does not repair (08).

Whenever this skill, `commands/ux-review.md`, `rules/ux.md` or `rules/ui.md` changes, drive the
fixtures per `self-test/README.md` and confirm each produces its `expected.md` outcome. The last two
are in that list because this skill's correctness is defined by them: fixture `02` exists because the
boundary between `ux.md` and `ui.md` moved on 2026-08-31, and the shorter summary it replaced —
*"aesthetics are out of scope"* — is now wrong in a way no reader can detect from this file alone.

Every failure mode here is silent, and one is worse than silent. A finding is a **citation**; a wrong
one arrives in the same table, in the same format, at the same severity as a right one, and a backlog
is read as a compliance record. Fixture `04` is the case that does not merely misinform — it directs an
author to break a conformant table, citing a real success criterion while doing so.
