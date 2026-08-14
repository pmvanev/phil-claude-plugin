# Expected — 38 (the target already exists, and it is closed)

**Pins:** slice-07 AC4, and the archaeology problem the retired slice 06 missed entirely.

**Expected:** `ASK-SET-LEVEL` then `APPLY-CONSOLIDATE`, naming **shape (b)**:

```
#62, #63, #64 are slices of one feature (all three bodies name docs/feature/search-rank/).
No open parent -- but #61 'Search ranking rework' is CLOSED and says
'superseded by #62, #63, #64'. That is the feature card, closed by the split that
created these.

Consolidating means reopening #61, not creating a new card.
Note: `gh issue reopen` restores the issue and NOT the Status field, so #61 will sit
OPEN in Done until the field is set by hand. No board view flags that combination.
```

**Why this is the shape a session gets wrong.** The scan reads open issues. #61 is not in that list, so the
evidence available *in context* says no feature card exists — which resolves to shape (c), **create one**. The
result is a second feature card beside the real one, with the original's history and reasoning stranded behind
a closed tombstone that points at cards which no longer exist independently. Nothing errors; the board simply
acquires a duplicate that reads as the canonical card.

**So searching closed issues is not diligence, it is the operation.** Concluding (c) without it is the defect.

**Gate failures:**

- Creating a new feature card. The duplicate, and it looks correct afterwards.
- Reopening #61 and leaving its Status unset. Open-in-Done, invisible to every view.
- Closing #62-#64 before #61 is reopened and confirmed. If the reopen fails, the work has no open card at all.
- Trusting the tombstone's `superseded by` list as the full set. Re-derive from the artifacts; a later split may
  have added cards the comment never mentioned.
- Reporting shape (a). There is no open parent.
