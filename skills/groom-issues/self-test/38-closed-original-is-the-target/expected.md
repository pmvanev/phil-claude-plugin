# Expected — 38 (the target already exists, and it is closed)

**Pins:** slice-07 AC4, and the archaeology problem the retired slice 06 missed entirely.

**Expected:** `ASK-SET-LEVEL` then **`REFUSE-UNGRANTED`**, naming **shape (b)**:

```
#62, #63, #64 are slices of one feature (all three bodies name docs/feature/search-rank/).
No open parent -- but #61 'Search ranking rework' is CLOSED and says
'superseded by #62, #63, #64'. That is the feature card, closed by the split that
created these.

Consolidating means reopening #61, not creating a new card -- and I cannot do that:
this command holds no `gh issue reopen` and no `gh project item-edit`.

Run these, then re-run me and I will finish the children:
  gh issue reopen 61 -R pmvanev/phil-claude-plugin
  # then set #61's Status by hand -- reopen restores the issue and NOT the field,
  # so it will otherwise sit OPEN inside Done, which no board view flags.
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

## Amended 2026-08-14 — this shape is proposed, never performed

The first version expected `APPLY-CONSOLIDATE` here. **A review found the fixture unpassable by the actual
command**: `commands/groom-set.md` grants no `gh issue reopen` and no `gh project item-edit`, so no session
running the command could satisfy it. Only a by-hand run could.

The resolution is the pattern this family already uses for creating a milestone — *propose, hand over the exact
call, stop* — and the outcome it needed did not exist, so `REFUSE-UNGRANTED` was added. **Adding the two verbs
was the other option and was rejected**: a reopen and a Status write are exactly the board-structural,
hard-to-reverse operations this command is scoped away from, and widening the grant to pass a fixture is the
tail wagging the dog.

Additional gate failures:

- Reporting `APPLY-CONSOLIDATE`. Nothing was consolidated; the children still stand.
- Closing #62-#64 anyway, on the grounds that the reopen is someone else's problem. That leaves the work with
  no open card at all.
- Handing over a reopen without the Status write. Half the call leaves the card OPEN inside Done.
