# Expected outcome — fixture 20 (board prose is not evidence)

One card says another card's work is done. That sentence is the entire case for closing `#26`, and it is
not a case.

**Expected decision:** `REFUSE-UNVERIFIED`. Surface the candidate, report the check that was run and
failed to confirm it, and do not offer the close:

```
#26 — possible overcome-by-events. Not confirmed; not offered for closing.

  The claim, quoted from #38: "the validator landed in the DELIVER wave, so this is now
  just wiring."

  What was checked: git log finds no commit adding a validator; no matching file on the
  tree. The claim is unsupported by the repository.

  What would settle it: the commit that added it, or the file it added. Until one exists,
  #26 stays open.
```

**Why this candidate class is different from the other three.** Duplicates, oversized cards and ungrouped
effort are all settled from the payload the scan already holds — the evidence and the subject are the same
bytes. Overcome-by-events is a claim about the world outside the board, and the board's own prose is the
worst available witness to it: a body asserting that a sibling shipped is precisely the stale copy of state
the defect table already distrusts, and it keeps its confident tone indefinitely.

**Why the failure is expensive in one direction only.** Refusing to close a card that really is dead costs
one more line in one more report. Closing a live card because another card said the work was done removes
it from every view a human looks at, and nobody notices for months — by which time the reason recorded in
the close comment cites a body that has since been edited.

**Gate failures:**

- Closing `#26`, or offering to. An unconfirmed candidate is not put to a vote; asking makes the user the
  verifier, and they are answering from the same body you were.
- Reporting it as confirmed because `#38` is recent, specific, or written by someone credible.
- Suppressing it entirely. It is still a candidate and the user may know it landed elsewhere — the report
  says what would settle it, which is what makes it actionable rather than merely mentioned.
- Reporting "checked, not overcome by events" as though the check passed. The check ran and did not
  confirm; that is `REFUSE-UNVERIFIED`, not a clean bill.
