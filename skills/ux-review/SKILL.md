---
name: ux-review
description: Skill bundle for phil:ux-review command — UX usability & accessibility audit against rules/ux.md with a prioritized findings backlog
---

# UX Review

You are auditing UI against the usability and accessibility standard in `~/.claude/rules/ux.md`. Your job is to find UX violations and produce a prioritized, actionable backlog. `ux.md` owns usability + accessibility; **aesthetics belong to `ui.md`** and React idioms to `react.md` — do not review against those here.

`ux.md` is the source of truth for what to flag and how to phrase the fix. It defines two tiers and a "Do not flag" section — mirror them:

- **Always-flag** (objective defects) → severity **must-fix**
- **Advisory** (judgment calls) → severity **consider**
- **Do not flag** → never raise (intentional expert-tool density, aesthetics owned by `ui.md`, `react.md`'s a11y bullet, formatter's style, any "max 7 items" cap)

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

Read `~/.claude/rules/ux.md` first so your findings and wording trace to it. For each file, check the tiers below. **Static review catches most defects; some need the rendered UI** — when a check depends on computed styles or live behavior (contrast ratios, actual focus visibility, real target size), flag it as must-fix only when the source makes it clear, otherwise raise a **consider** item asking the author to verify at runtime. Say which.

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

### Consider — judgment calls (advisory tier)

Raise these as guidance, not hard blocks: feedback timing (~1s / ~10s thresholds), empty-state copy that guides the next action, error prevention before messages, forgiving input formats (input only), minimal required fields, sensible defaults, reduce/segment choices + presets, progressive disclosure (≤ 2 levels), recognition over recall / chunking, platform conventions, consistent vocabulary, Gestalt grouping, scannability/headings, one clear visual hierarchy, plain action-labeled copy, progress toward goals, optimistic UI for reversible actions only.

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

- Anything in `ux.md`'s **"Do not flag"** section: intentional density in expert/pro tools, established conventions, aesthetics (owned by `ui.md`), React-specific a11y (owned by `react.md`), and formatter-owned style.
- A **"max 7 items" (or equivalent) count cap** — `ux.md` explicitly rejects it; at most advise chunking.
- Visual/aesthetic preferences (color palettes, typography, animation) — those are `ui.md`'s remit, not a UX defect.
- Hypothetical issues in code you don't fully understand — when uncertain, skip.

**Be precise, not exhaustive.** A backlog with 8 well-identified, traceable findings beats one with 40 vague ones.
