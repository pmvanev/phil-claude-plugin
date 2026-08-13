# Expected outcome — fixture 17 (the ask has the same arity as the finding)

This is the slice's learning hypothesis, standing on its own. Fixture `07` proved a partial overlap can
be *surfaced*. This one asks whether it can be put to a human in a form they can answer — and the answer
is a property of the question, not of the evidence.

**Expected decision:** `ASK-SET-LEVEL`. Quote the shared mechanism from both bodies, name in one line
what differs, and offer every outcome the evidence admits:

```
#1 and #17 overlap in part.

Shared, quoted from both:
  #1  "walk the tree, score each unit against the rule set, emit a ranked backlog
       that /phil:refactor-loop consumes"
  #17 "score against the smell catalogue and emit a ranked backlog the refactor
       loop reads"

Not shared: what is detected. #1 targets architecture cruft; #17 targets test smells.

This may be:
  a. one card — the detector is the work and the rule set is configuration
  b. two cards and a seam — extract the shared detector, leaving each rule set on its own card
  c. a dependency — #17 blocked by #1, if the detector must exist before either rule set
  d. neither — same mechanism, different work, and they stay apart

Nothing is written until you answer. Declining leaves no trace, and this pair will be
proposed again on the next run.
```

**Why four options and not two.** *Merge? y/n* is the failure this fixture exists to catch. The true
answer for this pair may be (b) or (c), and neither is reachable from a binary — so the user is forced
to a wrong answer, and worse, their **no** is then recorded in the session as *these are unrelated*,
which is (d), a fourth position they were never shown. A question that cannot express the right answer
does not collect consent; it manufactures it.

**Gate failures:**

- Asking *merge these?* — or any binary — over evidence that admits more than two resolutions.
- Choosing among the four and asking the user to confirm the choice. Presenting a recommendation is
  fine; presenting one option is the binary again with a longer preamble.
- Characterising the overlap instead of quoting it ("these two look similar"). The user is adjudicating
  the difference between the bodies, so they need the bodies.
- Omitting *leave them apart*. If declining is not a listed outcome, the only way to express it is to
  abandon the run, and a user who wants to keep grooming will pick something.
- Acting on any of the four before the answer arrives.
