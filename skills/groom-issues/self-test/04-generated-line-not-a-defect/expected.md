# Expected outcome — fixture 04 (generated regions are not body content)

The card carries `wave: deliver` and an `nwave:status` block with no `Work this with:` line.

**Expected decision:** `NOT-A-DEFECT`. Say nothing about it in the defect table.

**Gate failure:** reporting it as a missing body element. It is generated into the delimited block by
`phil:nwave-issue-board`, so its absence is a publishing question — the block has not been refreshed
since that rule shipped. Worse, a grooming tool that "fixes" it hand-writes into a generated region,
and the next refresh silently destroys the edit.

Read this with `05`, which resolves the opposite way over the same surface. Both concern text in an
issue body; the distinction is **who owns it**. A human owns their prose, so scratch in it is a
defect. A generator owns what lies between its markers, so its contents are not this skill's business
at all.
