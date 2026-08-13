# Expected outcome — fixture 06 (nothing is remembered, deliberately)

A duplicate candidate was surfaced last week and declined. Nothing recorded it.

**Expected decision:** `NO-MARKER`. Re-derive the table from scratch, surface the same candidate
again, and **say why it reappeared**:

```
Issues 14 and 19 overlap. (This may have been raised before — grooming stores no state,
so a declined candidate is proposed again each run.)
```

**Gate failures:**

- Reading any stored marker — a `groomed` label, a timestamp block, a state file. None exists, and
  looking for one is the beginning of writing one.
- Writing one, in any form, to avoid the repeat.
- Surfacing the candidate with no explanation. Then it reads as the tool forgetting, and the user
  quite reasonably asks for the marker — which is how the second authority gets introduced by
  popular demand rather than by decision.

The repeat is the accepted cost of storing nothing. Owning it out loud is what keeps the trade
visible.
