# Expected outcome — fixture 12 (the scope is a line, not a hint)

Scope: relative links. Two are in it. A third mechanical defect — #40's accumulated label — is not.

**Expected decision:** `APPLY-MECHANICAL` on #31 and #33 only, each change reported with the reason it
needed no judgement:

```
#31 — rewrote ./docs/adr/ADR-013.md as
      https://github.com/pmvanev/phil-claude-plugin/blob/main/docs/adr/ADR-013.md
      No judgement: GitHub emits relative paths verbatim, so the original 404s for every reader.
      The target is unambiguous and confirmed present on origin/main. Nothing was invented.
#33 — rewrote rules/testing.md as <absolute URL>. Same reason.

Not touched: #40's accumulated wave label — mechanical, but outside the scope you chose.
Not touched: #33 states no acceptance criteria — semantic, needs your decision.
```

**Why the justification is required rather than decorative.** The per-change line is what makes the
mechanical claim falsifiable. "No judgement: the target is confirmed on `origin/main` and nothing was
invented" can be checked and contradicted by a reader; "fixed 2 links" cannot. A slice whose whole
premise is that some fixes need no consultation has to show its work, or the premise is unfalsifiable
and the boundary is asserted rather than drawn.

**Gate failures:**

- Fixing #40 as well, because it is mechanical and the session is already writing. The scope is the
  user's line. Crossing it while technically staying inside the mechanical column is exactly the
  overreach the scoping step exists to prevent.
- Reporting the count without the reasons ("applied 2 mechanical fixes"). The reason is the deliverable.
- Silently omitting #40 and the semantic defect from the report. Out of scope means untouched, not
  unmentioned — a defect that vanishes from the output reads as fixed.
- Rewriting a relative link whose target cannot be confirmed on `origin/main`. That is the unverified
  candidate of slice 01's cross-reference row, and promoting it produces a link that renders, passes a
  read-back, and 404s for everyone else.
