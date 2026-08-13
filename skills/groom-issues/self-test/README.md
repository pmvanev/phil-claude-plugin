# phil:groom-issues — Acceptance Self-Test (slice 01)

The **scan and report** is the software under test. Its bugs are silent, and one of them is worse
than the rest: a completeness claim over a partial read looks exactly like a completeness claim over
a whole one. "52 clean" is a statement about issues nobody looked at, and nothing in the output
distinguishes the two.

These fixtures assert the correct **decision outcome**:

`REPORT-DEFECT` · `REPORT-CLEAN` · `REPORT-PARTIAL` · `REPORT-UNEVALUATED` · `SURFACE-CANDIDATE` ·
`NOT-A-DEFECT` · `NO-MARKER` · `READ-ONLY`

**`REPORT-UNEVALUATED` is additive**, like `REFUSE-DERIVABLE` in `skills/session-handoff/`. A run
reports it *alongside* `REPORT-DEFECT`, `REPORT-CLEAN` or `REPORT-PARTIAL` whenever a check went dark —
a board with defects can also have rules that never ran. Fixture `09` pins the case where it is the
only thing left to say, which is the one most likely to be swallowed by a clean-looking summary.

Format and intent mirror `skills/rank-issues/self-test/` and `skills/session-handoff/self-test/`.
Forge responses are supplied by `manifest.json` so the suite runs unattended.

## What the fixtures pin

| Fixture | Situation | Guard under test | Expected |
|---|---|---|---|
| `01-scan-and-report/` | 7 issues, 2 with body defects (**walking skeleton**) | the oracle produces checkable findings, not taste | `REPORT-DEFECT` — each cites rule + evidence |
| `02-partial-read-no-claim/` | pagination truncates at 100 of ~180 | a completeness claim over a partial read | `REPORT-PARTIAL` — no "N clean", ever |
| `03-clean-board/` | every issue well-formed | manufacturing work to justify the run | `REPORT-CLEAN` — and stop |
| `04-generated-line-not-a-defect/` | a wave-labelled card whose block has no `Work this with:` | generated regions are not body content | `NOT-A-DEFECT` |
| `05-session-scratch-is-a-defect/` | a body carrying session working state | the board is world-readable (ADR-013) | `REPORT-DEFECT` |
| `06-no-marker-anywhere/` | a board previously groomed | a stored marker is a second authority | `NO-MARKER` — re-derive; declined items reappear |
| `07-surface-not-act/` | two issues overlapping in part | set-level ops are slice 03 and ask-first | `SURFACE-CANDIDATE` — evidence, no action |
| `08-read-only/` | defects found and obviously fixable | the slice is read-only | `READ-ONLY` — nothing written |
| `09-unevaluated-is-not-clean/` | whole board read, but rules 3 and 4 have no oracle here | silence from a rule reading as compliance | `REPORT-UNEVALUATED` — name the dark rules |
| `10-one-sided-chain/` | one chain named from one end only, beside a correctly mirrored pair | half a relationship reads as a whole one | `REPORT-DEFECT` — mechanical, on the silent end |

## The sharpest

**`02` is the one that matters most.** Every other failure here produces a wrong item in a list a
human reads and can argue with. This one produces a *right-looking* summary line that is false about
work nobody examined — and the reader has no way to tell. If `02` fails while the rest pass, the tool
is more dangerous than no tool.

**`09` is `02`'s quieter twin, and harder to catch.** Both emit a summary that overstates what was
examined. In `02` the issue count is visibly short, so a reader who checks the numbers can see it. In
`09` every number is honest and complete, and what is missing is which *rules* were awake — invisible
from the output alone. `02` was found by reasoning about pagination; `09` came out of the first real
run, where two rules produced no findings because neither had an oracle on that board.

**`04` and `05` resolve in opposite directions over the same surface.** Both concern content that
appears in an issue body; `05` must flag it and `04` must not. A rule that catches one by a principle
that breaks the other — "flag anything unexpected in a body", or "never flag body content" — is a
gate failure. The distinction is *who owns the text*: a human owns their prose, a generator owns
what is between its markers.

## Running

Drive each fixture by giving the session the situation in `manifest.json` and comparing the decisions
reached against `expected.md`. Model-driven; there is no CI runner in this plugin.
