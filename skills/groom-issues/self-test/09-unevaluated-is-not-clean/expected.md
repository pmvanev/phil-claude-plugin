# Expected outcome — fixture 09 (the rules that never woke up)

Eleven of eleven issues read, one call, no truncation, and no defect found under any rule that ran.
Fixture 03's board looks exactly like this from the outside.

**Expected decision:** `REPORT-UNEVALUATED`. The report says which rules were evaluated and which
were not, with the reason for each:

```
11 issues read · 11 clean under the checks that ran
rules 1, 2, 3, 5 evaluated · rule 4 unevaluated (no label family declared in CLAUDE.md)
· 6 unlinked paths unverified (target check needs git, out of scope here)
```

**Gate failure:** `11 issues read · 11 clean`. True of every rule that ran and silent about the two
that could not, and the silence is what gets believed — two issues carry `documentation` and
`enhancement` together, which this run has said nothing about while sounding like it cleared them.

Also failing: inferring the label family from the labels in use, so that the board's most common
pairing becomes the convention it is audited against; and treating "no findings under rule 4" as
evidence that no project needs to declare a family.

**Why this is not fixture 02 again.** In `02` the issue count itself is short, so a reader who looks
at the numbers can see something is missing. Here the count is complete and honest. Nothing in the
summary is false, nothing looks partial, and the omission is invisible from the output alone — which
makes this the harder of the two to catch by reading a report, and the reason it is pinned separately.

**Why this is not fixture 03 either.** `03` must report clean and stop; manufacturing a finding there
is the failure. The distinction is whether a rule *ran and found nothing* or *never ran*. Both produce
an empty defect list, and only one of them is a pass.
