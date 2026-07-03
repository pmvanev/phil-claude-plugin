# Job Stories — ux-standards-rule

Lean JTBD framing for a tooling feature. The "user" is a **developer using this plugin**
while editing UI code. Grounded in `docs/research/ux/general-ux-design-best-practices.md`.

## Persona (inline — no separate persona file for an ~80-line rule)

**Devon — UI-building developer.** Ships product UI (React/Vue/HTML/CSS) inside a repo that
has the phil plugin installed. Competent at behavior and state, but does **not** hold
Nielsen's 10 heuristics and WCAG in working memory while heads-down on a component. Trusts
`react.md` to flag React idioms and `ui.md` to push visual polish, and wants the same
always-on help for **usability and accessibility** — the parts easiest to forget mid-flow.

## Primary job (registered in `docs/product/jobs.yaml`)

`job_id: catch-ux-violations-while-building-ui`

> When I'm building or editing a UI and I'm heads-down on behavior, I want the plugin to
> flag concrete UX/usability and accessibility violations and name the preferred form, so I
> can catch defects (missing states, placeholder-as-label, color-only status, unlabeled
> controls, sub-24px targets) before they ship — without having to hold all of Nielsen's
> heuristics and WCAG in my head.

### Four forces

- **Push**: No automated UX coverage exists. `ui.md` pushes aesthetics ("wow", premium,
  gradients) but nothing owns usability/accessibility; heuristics and WCAG are easy to forget
  mid-flow.
- **Pull**: The same auto-loaded, "flag the violation, name the preferred form" help that
  `react.md` gives React idioms — but for UX usability and accessibility.
- **Anxiety**: (A) A rule that nags on every judgment call creates noise on dense expert
  tools. (B) It might duplicate or contradict `ui.md`'s aesthetics guidance.
- **Habit**: Manual review, relying on memory, or catching UX defects only in QA/production.

## Secondary job stories (touchpoint-specific — inform rule vs skill)

**JS-2 (review touchpoint).**
> When I run `/phil:review-code` over a UI change, I want UX/a11y defects surfaced alongside
> the code-quality findings, so a single review pass covers usability too.

**JS-3 (deliberate audit touchpoint).**
> When I want to deliberately audit a whole screen against UX best practice (not just the file
> I'm editing), I want a focused, deeper pass I can invoke on demand, so I can check a finished
> flow end-to-end.

> JS-3 is the only job an *invoked skill* would serve better than an auto-loaded rule. It is
> lower-frequency and partly covered by `/phil:review-code` today — see `journey.md` for why it
> is deferred (YAGNI).
