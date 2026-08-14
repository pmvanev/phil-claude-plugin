# Expected — 35 (shorter than the clean card, and oversized)

**Pins:** the other half of the pair. `34` and `35` must resolve **opposite ways**, and a rule that gets one
right by getting the other wrong is a gate failure.

**Expected decision:** `REPORT-DEFECT` with `SURFACE-CANDIDATE`. Oversized, **with the seam named**:

```
#31 — oversized. Four jobs, no single demonstration.
  seam: signing-key rotation | session-store migration | login rate limiting |
        password-reset email rewrite
  Each can be demonstrated alone; the card as a whole cannot.
  Resolving this is /phil:groom-set, and it asks first.
```

**Why the pair is the point.** #31 is **shorter** than #26, which is clean. Any heuristic keyed on length,
body size, section count or roster presence gets this pair backwards — and the failure is silent both ways:
the clean card gets flagged, and this one passes. The discriminator is the rule as written, and only the
rule as written: *can this be demonstrated on its own?*

**Gate failures:**

- Passing #31 because it is short, or because it lacks a generated block.
- Reporting it without naming the seam. "Consider splitting this" hands the work back with none of the
  analysis that made it a finding.
- Acting on it. The scan reports; `/phil:groom-set` resolves, and asks.
- Proposing the split as a *feature* re-slicing. This is a story with four jobs in it, not a feature with
  slices — `/phil:groom-set`'s split creates cards here, which is the operation that still exists.
