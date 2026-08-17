# Decision outcomes — the per-outcome detail

`SKILL.md` lists the six terminal outcomes and the two report lines. This file says what each one
means and who produced it. **The discriminator is who stopped the run**, because the script has one
failure state and the model has another.

## Terminal outcomes

- **`WROTE`** — names the file and the field count. The target had no `## Issue board` section, or
  no file at all, so nothing human was at risk.
- **`WROTE-BESIDE-PROSE`** — the region was inserted into a section a human had already written.
  Names the file, the field count, and the three drift bucket counts. Distinct from `WROTE` because
  the risk is different: `WROTE` touched a file with nothing to lose.
- **`AMBIGUOUS-TARGET`** — resolved by the model at CONFIRM, *before* the script runs: two remotes,
  or a fork. A question, never a guess.
- **`REFUSED`** — the script returned `status: refused`. Report `refusal.reason` verbatim and
  `refusal.fix` when non-null. Covers every case the script cannot resolve: a missing `project`
  scope, more than one candidate project, no board at all, a project with no `Status` field, a forge
  error. The file is byte-unchanged.
- **`REGION-PRESENT`** — a region is already there. Slice 05 owns re-run and staleness; until it
  ships this stops, changing nothing. **Not a failure**, and reported so it does not read as one.
- **`MALFORMED-MARKERS`** — `begin` without `end`, `end` without `begin`, nested, or out of order.
  Four shapes, and the enumeration is a checklist: `classify()` returns all four. Refused with the
  file byte-unchanged. The extent is never guessed, because a wrong guess deletes prose.

## The two report lines

- **`DRIFT`** — the three bucket counts, on any run reaching step 5.
- **`REPORTED-NOT-WRITTEN`** — the half-probed values: reported to the human, kept out of the file
  until slice 04 ships the labelling that would make them honest.

Neither stands alone. A run emitting one as its verdict has not reported an outcome.

**This separation is a correction.** The list previously said *exactly one* while
`REPORTED-NOT-WRITTEN` was defined as something that *accompanies a write*, and fixture 01 expected
both — while fixtures 03, 06 and 07, running against the same board and therefore the same two
half-probed entries, expected neither. A rule contradicted by the fixture that tests it is worse
than no rule, because each looks like authority for the other.

## `SECTION-EXISTS` is retired

It was slice 01's boundary marker, and slice 02 is the thing it pointed at. A run that still reports
it is running the old skill. The retirement is recorded in three places — here, in fixture 03's
`supersedes` field, and in that fixture's `must_not` — so a stale run is detectable rather than
merely wrong.
