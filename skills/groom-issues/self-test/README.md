# phil:groom-issues — Acceptance Self-Test (slice 01)

The **scan and report** is the software under test. Its bugs are silent, and one of them is worse
than the rest: a completeness claim over a partial read looks exactly like a completeness claim over
a whole one. "52 clean" is a statement about issues nobody looked at, and nothing in the output
distinguishes the two.

These fixtures assert the correct **decision outcome**:

`REPORT-DEFECT` · `REPORT-CLEAN` · `REPORT-PARTIAL` · `SURFACE-CANDIDATE` · `NOT-A-DEFECT` ·
`NO-MARKER` · `READ-ONLY`

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

## The two sharpest

**`02` is the one that matters most.** Every other failure here produces a wrong item in a list a
human reads and can argue with. This one produces a *right-looking* summary line that is false about
work nobody examined — and the reader has no way to tell. If `02` fails while the rest pass, the tool
is more dangerous than no tool.

**`04` and `05` resolve in opposite directions over the same surface.** Both concern content that
appears in an issue body; `05` must flag it and `04` must not. A rule that catches one by a principle
that breaks the other — "flag anything unexpected in a body", or "never flag body content" — is a
gate failure. The distinction is *who owns the text*: a human owns their prose, a generator owns
what is between its markers.

## Running

Drive each fixture by giving the session the situation in `manifest.json` and comparing the decisions
reached against `expected.md`. Model-driven; there is no CI runner in this plugin.
