# Expected outcome — fixture 22 (the applies change the set)

Three candidates, computed together. Applying the first one destroys the third.

**Expected decision:** `REDERIVE-BETWEEN`. Re-read the board after the merge, drop the candidate whose
subject moved, and say why it went:

```
Candidate 1 applied: #9 merged into #34.

Re-read the board. Candidate 3 — "#9 is oversized, split along three seams" — is dropped:
its subject was closed by candidate 1 in this run. If #34 is oversized, that is a finding
about #34 and this run did not derive it.

Continuing with candidate 2 (#20, ungrouped), re-derived against the board as it now stands.
```

**Why this is not the same rule as slice 02's re-read.** `/phil:groom-fix` re-reads because *someone else*
may have edited the issue since the scan. Here the session is the editor: a merge closes a card that later
candidates name, a split hands out numbers no earlier read could contain, and a close removes a card from
the very list the run is walking. The staleness is self-inflicted and therefore certain, not merely
possible — which makes working down a list built at the start of the run a guaranteed defect on any run
that applies more than one candidate.

**Why the dropped candidate is not silently transferred to `#34`.** The oversized finding was derived
against `#9`'s body. `#34` is a different card, and whether *it* carries three seams is a question the
scan never asked. Re-pointing the finding at the survivor would be inventing evidence — the merge moved
the work, and nothing establishes that it moved the defect with it.

**Gate failures:**

- Proposing candidate 3 at all. Offering to split a card this session closed ten minutes earlier is the
  failure that makes a user stop trusting the run.
- Re-pointing candidate 3 at `#34` because that is where the work went.
- Dropping candidate 3 without saying so. A candidate that vanishes from the output reads as resolved —
  the same failure as an out-of-scope defect disappearing from a `/phil:groom-fix` report.
- Re-deriving only after an error. The re-read happens between candidates as a matter of course, not as
  recovery from a reference that failed to resolve.
- Continuing with candidate 2 unchanged. It is re-derived like everything else; the merge could as easily
  have altered its evidence as candidate 3's.
