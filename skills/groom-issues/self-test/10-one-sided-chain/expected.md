# Expected outcome — fixture 10 (half a chain)

`#41` says it relates to `#55`. `#55` says nothing about `#41`. The `#41`/`#39` pair is mirrored and
must not be reported.

**Expected decision:** `REPORT-DEFECT`, classified **mechanical**:

```
#55 — one-sided chain. #41's ## Chain reads "Relates to #55 — if every mechanical defect
needs a question, this slice collapses into that one". #55 has no ## Chain section.
Rule 5: the edge and the reason, on both ends.
```

**Why mechanical, when so much else about chains is not.** The missing text is already written, on the
other issue. Mirroring it invents nothing — which is the test the mechanical column applies, and the
reason this row belongs there while "no purpose stated" never can.

**Gate failures:**

- Reporting the mirrored `#41`/`#39` pair. A check that flags every chain is not a check.
- Classifying it semantic and asking. The reason exists in `#41`'s own words; asking the user to supply
  what is already written teaches them the tool has not read the board.
- Reporting it against `#41` rather than `#55`. `#41` is complete; the gap is on the issue a reader
  lands on and learns nothing from.
- Deciding which end is right when the two ends give *different* reasons. That is a genuine
  disagreement between two authored statements and it is semantic — this fixture is the case where one
  end is simply absent.

**Provenance.** This defect was produced by the skill's own author on a real run: three of four chains
written that day were one-sided, hours after the rule requiring both ends was read. Writing one end
while the relationship is fresh and never returning for the other is the ordinary way this is made, so
a suite that only pins exotic cases will not pin the common one.
