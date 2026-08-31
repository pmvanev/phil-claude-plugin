# Expected outcome — fixture 15 (either source alone is a roster)

**Pins:** the *conjunction* in the empty-roster row of the fold. Fixture 14 proves the guard fires when it
should; this one proves it does not fire when only one of its two clauses holds.

**Expected state:** `done`, with the count beside it:

```
Feature: export-csv — done · 4 of 4 slices done
```

**The failure this fixture exists to catch.** A guard written as *"no slice files"* rather than *"no slice
files **and** no roadmap phases"* fires here — a feature whose every step is recorded COMMIT/PASS would be
published as `unknown`, and a card sitting in Done would be pulled out of it. The guard would have converted
a fold that over-reported completion into one that under-reports it, and the fixture that motivated the
guard (14) would still pass.

**Why this fixture had to exist.** This repo's own record says a check must be shown to fail on the input
that motivated it before a green run is trusted — the first version of `check-readonly-commands.py` passed
silently because the function was written and never called. Fixture 14 alone cannot distinguish a correct
conjunctive guard from a broken disjunctive one: both return `unknown` over an empty roster. Only a layout
where exactly one clause holds separates them.

**Roadmap-without-slices is a real layout, not a contrivance.** *Degrade honestly* already treats the two
sources as independent — it names *"no `roadmap.json` and no `progress.md`, but `slices/` exists"* and
*"roadmap present, no progress record of any kind"* as separate cases. A feature small enough to roadmap
without slice briefs produces this one, and the roadmap's phases are the roster.

**The mirror arm is real but not state-discriminable, and this fixture does not claim it.** A guard weakened
the other way — *"no roadmap phases"* alone — would fire on a roster of slice files with no roadmap
(fixture 10's layout). It cannot be caught by comparing states: with no roadmap there is no step record, so
every slice is `unknown`, the `unknown` row returns `unknown`, and a wrongly-fired guard returns `unknown`
too. Same answer, different path. Catching that one needs a fixture that asserts the *reason* rather than the
state, which this suite has no vocabulary for. Recorded rather than papered over: half this conjunction is
pinned by output, and half is pinned only by reading the row.

**Gate failures:**

- Returning `unknown`. The disjunctive guard, stated — and the reason this fixture exists.
- Returning `in progress`. Every phase is complete; this is the fold's third test read too early.
- Treating the absent `slices/` directory as a reason to degrade rather than to read the roadmap. *Degrade
  honestly* discards neither source when the other is present.
- Returning `done` with no count, or a count of slice *files* rather than roster entries. The roster here is
  the roadmap's phases; `0 of 0` would be the empty-roster rendering applied to a non-empty roster.
