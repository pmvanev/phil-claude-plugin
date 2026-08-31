# Expected outcome — fixture 13 (the fold reads every slice)

**Pins:** *The feature-level state, on request* — the `in progress` row of the fold table, and the reason the order
is the content.

**Expected state:** `in progress`. With a count beside it, because a state and a count answer different
questions:

```
Feature: bulk-import — in progress · 5 of 6 slices done · current slice 06
```

**The failure this fixture exists to catch.** Slice 06 is both **current** and **not started**, so a fold
that reads the current slice alone returns `not started` → `to do`. That renders a feature five-sixths
finished as untouched, on a board, to a team. It is the `unknown`-published-as-`not started` defect one
level up, and it is worse there: at step level a wrong row is one line in a table someone is already
reading closely; at feature level it is the card's whole position, read at a glance by people who will not
open it.

**Why the current-slice shortcut is so tempting.** It is cheap, it is correct in the common case, and it is
correct *here* about the slice — slice 06 really has not started. Only the scope is wrong. Any caller that
finds itself reaching for the current slice to answer a question about the feature has substituted the part
for the whole.

**Gate failures:**

- Returning `to do`. The defect, stated.
- Returning `unknown` because slice 06 has no record. `unknown` sits *below* `done`/`current` in the fold
  precisely so that one unrecorded slice cannot outvote five recorded ones. It is a `Notes` entry, not a
  verdict on the feature.
- Returning a bare count with no state when a state was asked for. `5 of 6` does not tell a caller which
  column to use, which is the whole reason the fold exists.
- Emitting the state unasked. It is a derivation on request; the default output is unchanged.
- Folding this in the publisher instead. `phil:nwave-issue-board` renders this value and must not compute
  it — two derivations over the same files drift apart, which is why the two skills are separate at all.
