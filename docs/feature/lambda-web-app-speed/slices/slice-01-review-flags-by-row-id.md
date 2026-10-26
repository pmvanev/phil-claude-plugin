# Slice 01 — `review-code` flags load-time defects by row id

**Goal.** `/phil:review-code` names a Lambda web app's file-visible load-time defects by `LWS-n` id and
fix, and leaves the look-alikes alone.

**Story:** US-01 · **Job:** make-a-lambda-web-app-load-fast

## IN scope
- `rules/lambda-web-app-speed.md`: the Always-flag table (research LWS-1 to LWS-20, revised by D6, D10
  and D11) and the Do-not-flag list, with a stub Principles heading that slices 02 and 04 fill.
- `skills/review-code/SKILL.md`: read the rule when the review meets the files D4 names, and apply its
  two lists.
- A self-test fixture: at least eight seeded defects beside five look-alikes, and a test that pins every
  row id and each expected item.
- One cross-reference line in `coding.md` §8 pointing at LWS-1, the Lambda form of building once at the composition root.

## OUT scope
- The Principles prose and the Advisory list (slices 02 and 04).
- The new command (slice 02).

## Learning hypothesis
Disproves "most of what the projects found by measuring is visible in their files" **if** the backtest
catches fewer than 80% of the file-visible fixes beatrix 254 and modive 22 made by hand. Confirms the
review half earns its place in every review if it does.

## Acceptance criteria
See US-01 in `feature-delta.md`.

## Dependencies
- Research precursor (done). V1 closed on the day the GovCloud rows are written.

## Effort / reference class
≤ 1 day. Reference class: `ci-pipeline-standard` slice 01.

## Production data
Two backtests, recorded in the delta: beatrix at the commit before issue 254's first fix, and modive at
`43e6b85`, each read in a scratch clone.
