# Slice 02 — The slice summary, which must say what the brief does not

**Goal:** Ship `--slice`, folding a brief together with the commits and files that landed, in 200 words.

**Stories:** S2
**Answers:** the card's own doubt about whether this half is worth building

## Learning hypothesis

**Disproves [D2] — and vindicates the card — if a slice summary never says anything its brief does not.**
The card doubted this half on the grounds that briefs are already short. That reasoning is refuted: the
median brief is 777 words, not the ~400 it measured on the two shortest in the repo. **But the conclusion
could still be right for a different reason** — if what a slice landed always matches what its brief
promised, the fold adds nothing and the brief alone is the answer.

**Confirms**, if the fold finds real gaps, that intent and outcome diverge often enough to be worth
reading — which is a fact about how this repo works, not just about this command.

**KPI-4 is the test and it is two-sided.** Three sampled slices; report the number either way. A zero
means drop this half rather than ship it.

## IN scope

- `--slice`, over `docs/feature/<id>/slices/`.
- **[D10]** — fold the brief with `git log`, `git show` and `git diff --stat` over the slice's commits.
  What **landed**, not what was intended.
- **Name the disagreement where one exists.** A brief promising something the commits do not show is the
  most valuable thing this command can surface, and smoothing it is the failure.
- **Where the brief and the outcome agree, say they agree** — and keep the summary short rather than
  padding to prove effort.
- **Where the fold finds nothing the brief does not say, say that** rather than restating the brief
  shorter. This is the card's doubt kept as behaviour instead of argued away.
- Same ceiling and same vocabulary list as slice 01, from the same module.
- Fixtures: the longest brief in the repo (3,670 words), a brief whose slice never shipped, and one where
  brief and commits agree.
- Version bump.

## OUT scope

- Deriving whether a slice is done. **[D8]** — `phil:nwave-slice-status` owns it, and this command must
  not become a second answer.
- Summarising commits outside the slice. Attribution is by the slice's own range, and where that cannot
  be established the command says so rather than guessing.
- Any write, including to the brief it read.
- Judging the quality of what landed. This reports; `phil:adversarial-review` judges.

## Acceptance criteria

S2's five. The fifth is the one that can end this half: the output must demonstrably say something the
brief does not, or say that it cannot.

## Dependencies

Slice 01, for the command, the skill and the ceiling.

## Effort

One day. The git fold is the new part.

## Reference class

`board-snapshot` slice 02 — a second mode on an existing command, bounded differently from the first.

## Dogfood moment

Same day: run it over this feature's own slice 01, and over `board-snapshot`'s three slices, whose
outcomes were written up in detail this week. **Those write-ups are the reference answer** — a summary
that misses what they record is a finding.

## Taste tests

- **Ships 4+ new components?** No — one flag.
- **Depends on a new abstraction?** No.
- **Disproves a pre-commitment?** Yes, and it is this feature's own scope decision.
- **Synthetic data only?** No — 57 real briefs and their real commits.
- **Identical to another slice but for scale?** No. Slice 01 reads one file; this one reconciles a file
  against history, which is a different question with a different failure mode.

## A routing collision this slice inherits

`phil:nwave-slice-status`'s trigger list already claims **"what was the point of slice 02"** — a
*what did the thinking intend* question, which is this mode's subject and not that skill's. Leaving it
there is correct while only the stage summary ships. **When `--slice` lands, that phrase has to move or
be disambiguated in both descriptions**, or the two skills compete for the same sentence and the reader
gets whichever is matched first.

## Pre-slice SPIKE

None, but note the one uncertainty: **establishing which commits belong to a slice.** This repo's commit
subjects name the slice, which is a convention rather than a guarantee. Where it cannot be established,
the command says so — that is in scope above rather than deferred.
