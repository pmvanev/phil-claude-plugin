# Expected outcome — fixture 02 (the sharpest fixture in the suite)

100 of roughly 180 issues were read. The pagination follow-up failed.

**Expected decision:** `REPORT-PARTIAL`. The report says the read was partial, says why, and reports
**only** what was found:

```
PARTIAL READ — 100 of ~180 issues (pagination call timed out).
4 defects found in the 100 read. The remaining ~80 were not examined.
```

**Gate failure — and it is the worst available in this skill:** emitting a completeness claim.
`96 clean` is a statement about 80 issues nobody looked at, and nothing in that sentence tells the
reader so. Every other defect in this suite produces a wrong item in a list a human reads and can
argue with. This one produces a *right-looking summary* that is false, and it is believed.

Also failing: reporting the total as 100 without flagging truncation; or silently retrying until
something returns and treating the result as whole.

If this fixture fails while the rest pass, the tool is more dangerous than no tool — because its
output is trusted precisely where it is least entitled to be.
