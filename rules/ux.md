---
paths:
  - "**/*.{tsx,jsx,vue,svelte,css,scss,sass,less,html}"
  - "**/components/**"
  - "**/pages/**"
  - "**/layouts/**"
  - "**/styles/**"
---

# UX Guide

Usability and interaction principles — the complement to `ui.md` (visual aesthetics). Flag the violation, name the preferred form. Vendor-neutral, durable heuristics (Nielsen, WCAG 2.2, Laws of UX), not framework rules. Source: `docs/research/ux/general-ux-design-best-practices.md`.

Two tiers. **Always-flag** — objective defects; call them out. **Advisory** — judgment calls; offer as guidance, don't hard-block. This rule owns **usability + accessibility**; aesthetics stay in `ui.md`; React-specific a11y stays in `react.md`. Complement those rules — don't restate them.

---

## Always-flag — objective defects

### Accessibility (WCAG)

| Violation | Preferred form |
|-----------|----------------|
| Interactive element not keyboard-operable, no visible focus, or a focus trap | All actions reachable and operable by keyboard; focus always visible; logical order; no traps |
| Meaning conveyed by color alone (red = error, green = ok) | Pair color with text, icon, or shape (WCAG 1.4.1) |
| Text contrast < 4.5:1 (< 3:1 large text); UI/icon contrast < 3:1 | Meet AA: text ≥ 4.5:1 / 3:1 large; components ≥ 3:1 (1.4.3 / 1.4.11) |
| Interactive target < 24×24 CSS px with no spacing exception | Target ≥ 24×24px (2.5.8); ~44px for comfortable touch |
| Icon-only control, image, or region with no accessible name / semantics | Text alternatives, accessible names, semantic structure and headings |

### State & feedback

| Violation | Preferred form |
|-----------|----------------|
| Data-driven view with no loading / empty / error state | Design every state; never assume data loads successfully |
| One-click destructive or irreversible action, unguarded | Undo (preferred) or confirmation; reserve modal confirm for the irreversible |

### Forms & controls

| Violation | Preferred form |
|-----------|----------------|
| Input labeled only by `placeholder` | Persistent visible `<label>`; placeholder is a hint, not a label |
| Validation on every keystroke, or only in a distant summary | Validate inline after the field loses focus; message adjacent to the field |
| Checkbox set where exactly one option is valid | Radio / single-select with a sensible default |
| Checkbox/radio used to trigger an action | Use a button; toggles are for instant binary on/off only |
| Raw error code, stack trace, or "Invalid input" shown to the user | Specific, human, blame-free, actionable message that preserves input |

## Advisory — judgment calls, not hard blocks

- **Feedback & timing** — respond within ~1s; show a progress indicator past ~1s, cancelable past ~10s. Empty states guide the next action, not just "No data."
- **Choice & disclosure** — reduce or segment simultaneous choices; offer presets and a reset. Progressively disclose advanced/rare options, ≤ 2 levels deep. Ship a sensible, reversible default rather than forcing a choice.
- **Errors & input** — prevent errors with constraints/defaults before relying on messages; keep recovery easy. Accept forgiving input formats and normalize internally (Postel — **input formatting only**, never lax validation). Ask only for necessary fields; mark required vs optional consistently. Always give a clear exit/cancel; never trap the user.
- **Consistency & recognition** — follow platform/industry conventions; deviate only to genuinely improve. The same word/control/action means the same thing everywhere. Prefer recognition over recall; chunk and group to ease memory (there is **no "max 7 items" cap** — that misreads Miller).
- **Hierarchy & grouping** — convey grouping via proximity and shared containers (Gestalt). Front-load key content; use descriptive headings for scannability. Establish one clear visual hierarchy — if everything is emphasized, nothing is. Remove non-essential elements; each extra unit dilutes the rest.
- **Copy** — plain, audience-appropriate language; action-specific labels ("Save changes", not "OK"); no internal jargon.
- **Progress & motion** — show progress toward goals; place key items first or last. Use optimistic UI only for reversible, high-confidence actions; roll back visibly on failure.
- **Aesthetic-usability** — polish raises perceived trust, but never let it mask a real usability defect. Visual polish is `ui.md`'s remit.

## Do not flag

- **Intentional density** in expert/pro tools (dashboards, IDEs, trading UIs) — dense by design, not a defect.
- **Established conventions** the team has deliberately adopted.
- **Visual aesthetics** — color, typography, animation, gradients — `ui.md` owns those.
- **React-specific accessibility** already covered by `react.md`.
- **Formatting/style** the formatter owns.
- A **"max 7 items" limit** — Miller's number is short-term-memory span, not an on-screen cap; advise chunking, never a count.
