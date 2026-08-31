# Expected outcome — fixture 14 (an empty roster folds to `unknown`, never `done`)

**Pins:** *The feature-level state, on request* — the empty-roster row of the fold table, and the reason it
sits above every test quantified over slices.

**Expected state:** `unknown`, with the reason beside it and **no count**, because there is nothing to
count:

```
Feature: notification-service — unknown · no slice roster and no roadmap phases · suggest /nw-roadmap
```

**The failure this fixture exists to catch.** With no slices, *"every slice that is not `deferred` is
`done`"* is true of nothing. A fold read literally therefore answers `done` for a feature nobody has
roadmapped — and the `deferred` and `to do` rows are vacuous the same way; the `done` test merely fires
first. The `blocked` row has no current slice to read, and the two
existential rows — `in progress` and `unknown` — are *false* over an empty set rather than vacuously true.
So it is specifically the three universals that needed guarding, and naming the wrong rows here would send
the next reader to the safe ones. The bug is not a
wrong comparison, it is an unguarded quantifier, which is why no amount of care inside the rows finds it.

**Why this is the costliest cell in the table.** `phil:nwave-issue-board` maps `done` to the Done column,
and this plugin's own board has auto-close enabled on Done. So the failure does not stop at a misrendered
card: it closes an issue for a feature that has not been decomposed, and the closing write reports success.
Every other fold error misinforms a reader; this one mutates the tracker.

**Same layout as fixture 07, one flag apart.** Fixture 07 pins the *table* path over exactly these
artifacts and passes — *Degrade honestly* covers a slice-less feature, and 07's assertions predate the fold
entirely. Holding the layout fixed and changing only `--feature-state` is what isolates the defect to the
fold, and it is why 07 reporting clean was never evidence about this.

**Why `unknown` rather than `to do`.** An empty roster is a fact about the record, not about the work.
`to do` claims nobody has started; `unknown` claims nobody has assessed. That is the cardinal rule of this
skill, and the fold is where it is easiest to lose, because the fold's caller wants a column and `unknown`
does not give them one.

**Gate failures:**

- Returning `done`. The defect, stated.
- Returning `to do`. The cardinal lie — a claim about the work from a fact about the evidence.
- Returning `deferred`. *Every slice is `deferred`* is vacuous here too; nothing was set aside.
- Returning `in progress` on the strength of completed DISCUSS/DESIGN artifacts. Upstream waves are not
  slices, and the fold is defined over the roster.
- Returning a count beside the state. `0 of 0 done` reads as completion and is the same lie arithmetically.
- Emitting the state unasked. It is a derivation on request; fixture 07's default output is unchanged.
- Folding this in the publisher instead. `phil:nwave-issue-board` renders this value and must not compute it.
- Writing a board column for the returned `unknown`. The publisher's mapping says **no column — do not
  write one**; a fold fixed here and coerced there gains nothing.
