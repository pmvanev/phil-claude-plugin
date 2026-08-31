# phil:ux-review — Acceptance Self-Test

The `phil:ux-review` **UX auditor** is the software under test, and its bugs are silent in a
particular way: this skill's output is a *citation*. A finding names a WCAG success criterion and a
preferred form, which is what makes it actionable — and what makes a wrong one credible. A false
2.5.8 violation is indistinguishable from a true one to everybody downstream, because both arrive as
one line in the same table, in the same format, at the same severity.

So the risk is not a reviewer that misses things. It is a reviewer that is **confidently, citably
wrong** — and worse, one whose wrong findings get acted on, because a backlog is treated as a
compliance record.

These fixtures feed the auditor known UI situations and assert each produces the correct **decision
outcome** (`BACKLOG-WRITTEN` / `BOUNDARY-HELD` / `COUNT-CAP-NOT-FLAGGED` / `EXEMPT-NOT-FLAGGED` /
`CITATION-CORRECT` / `RUNTIME-DEFERRED` / `SCOPE-FILTERED` / `NEVER-EDITS`).

This suite is the **acceptance + regression gate** for
[`skills/ux-review/SKILL.md`](../SKILL.md) and
[`commands/ux-review.md`](../../../commands/ux-review.md). Run it whenever either changes, and
whenever [`rules/ux.md`](../../../rules/ux.md) or [`rules/ui.md`](../../../rules/ui.md) changes —
this skill's correctness is defined by those two, and fixture `02` exists because the boundary between
them moved. Format and intent mirror `skills/adversarial-review/self-test/` and
`skills/nwave-slice-status/self-test/`.

Written 2026-08-31. Until then `ux-review` was the only reviewer skill in the plugin with **no
self-test at all** — noticed while redrawing its aesthetics boundary, when it turned out that four
edits to what it must and must not flag were pinned by nothing.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected outcome |
|---|---|---|---|
| `01-backlog-from-real-defects/` | placeholder-only label; no loading/empty/error state (**walking skeleton**) | raises both as must-fix, each naming the principle and the preferred form | `BACKLOG-WRITTEN` |
| `02-motion-cost-in-scope-taste-is-not/` | one stylesheet with **both** a missing reduced-motion variant and a garish palette | flags the motion gap, says nothing about the palette | `BOUNDARY-HELD` |
| `03-no-count-cap/` | a twelve-item nav, already grouped and labelled | never rests a finding on item count; does not advise chunking where grouping exists | `COUNT-CAP-NOT-FLAGGED` |
| `04-two-d-content-exempt-from-reflow/` | a 14-column table scrolling horizontally at 320px | applies the 1.4.10 exemption instead of rediscovering the symptom | `EXEMPT-NOT-FLAGGED` |
| `05-target-size-cited-to-the-right-floor/` | a 30×30px icon button — above the WCAG floor, below platform comfort | cites the platform guidance, never 2.5.8 | `CITATION-CORRECT` |
| `06-contrast-unresolvable-defers-to-runtime/` | text and background set by theme tokens that do not resolve in scope | defers to a rendered check; neither asserts nor silently passes | `RUNTIME-DEFERRED` |
| `07-non-ui-files-skipped/` | a diff touching a component, its test file, a config and a data module | reviews the component; skips the rest without reporting them clean | `SCOPE-FILTERED` |
| `08-writes-the-backlog-never-the-code/` | an unambiguous defect with a two-token fix, and a grant that permits editing | writes the backlog; leaves the component byte-identical | `NEVER-EDITS` |

`01` is the single walking-skeleton scenario. The **safety core** is `02`, `04`, `05`, `06` — the
cases where a wrong answer is indistinguishable from a right one: a taste finding dressed as an
accessibility defect, a real criterion cited against content it exempts, a true-sounding citation for
a criterion the element passes, and a check reported as clean when it never ran.

**Fixture `04` carries the only actively harmful failure in the suite.** Every other bad outcome
misinforms someone. That one *directs*: it tells an author to make a conformant fourteen-column ledger
reflow to a single column, cites a real success criterion while doing so, and an author who complies
ends up worse off than before the review. Same shape as fixture `04` in the sibling status suite,
which is a coincidence of numbering and not of design.

**Fixtures `05` and `06` pin the honesty of a citation in both directions** — claiming a standard that
does not apply, and reporting a measurement that was never taken. Both convert an absence of evidence
into a statement about the product.

**Fixture `02` is the newest and the most likely to rot.** The boundary between this skill and
`ui.md` is not "usability versus aesthetics" — it is **checkable versus not**. An animation's
reduced-motion variant and its frame cost are reviewed here; whether the animation is attractive is
not. Anyone tempted to restore the shorter summary should make this fixture fail first.

## Layout

Each fixture is self-contained and manifest-driven — no sample application is checked out. The
`manifest.json` describes the situation: the UI code and its relevant contents, the arguments the
command is invoked with, and the `expected_outcome`. The `expected.md` states the decision the skill
must produce, the guard that produces it, and the gate-failure conditions that block the skill change.

## How to drive it

For each fixture, run `skills/ux-review/SKILL.md` against the situation in `manifest.json` as
`/phil:ux-review` would, and compare the findings against `expected.md`. Any fixture that produces the
wrong outcome is a gate failure — **block the skill change**.

Two assertions apply to every fixture and are not repeated in each file:

1. **No file under review is modified.** The backlog is the only write.
2. **No finding is raised without naming the `ux.md` principle it violates and the preferred form.**
   A finding a reader cannot trace to the standard is an opinion, and this skill does not ship
   opinions.
