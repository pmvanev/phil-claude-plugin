# CLAIM — In Progress, assigned, read back

Part of the `start` skill; `../SKILL.md` governs this step as much as this file does. Read this file
whole before the first claim write, and before filing a card.

**Running `/phil:start` is the developer's yes to the claim.** Claim the card in the order
`phil:issue-board` requires: add the item, write the Status, assign, read back. Skip a write that would
change nothing: a card already In Progress on the board needs no Status write, and a developer already
assigned needs no assign.

## Filing a card

A search matched nothing and the developer said yes to filing (`../SKILL.md`, RESOLVE). Words typed under
Other are a proposed title, not a yes: ask once more whether to file it under those words, and file only
on that yes.

```bash
gh issue create -R <owner/repo> --title '<the words>' --body ''
```

Write each `'` in the words as `'\''`. Use `gh issue create` only with `-R`, `--title` and `--body ''`: a
template, an assignee, a project or a body file would put words on the card that are not the developer's.
Take the number from the URL it prints and report `FILED`. A create that fails filed nothing:
`CANNOT-RUN`, quoting the error.

Then go straight to CHECK and to the steps below. The new card is on no board item, so step 1 adds it in
the same breath: a card created and never added is invisible on a board grouped by Status. **Once a card
is filed, no failure is `CANNOT-RUN`**: a failed read or write after the filing is `CLAIM-FAILED`, and the
report names the filed card's number.

## The writes

1. **Add the card to the board** where none of its project items is on the board's project:

   ```bash
   gh project item-add <project-number> --owner <project-owner> --url <issue-url>
   ```

   The exit code is not evidence that the item landed (`phil:issue-board`), and neither is its output:
   take the item id and its Status from a re-read of the number query's `projectItems`, the node whose
   `project.id` is the board's. Where that node is missing, re-read once more; still none is
   `CLAIM-FAILED`: `item-add exited 0 and the card is on no board item`. An add-to-project workflow may
   have set a Status already, which is why the Status comes from the re-read.
2. **Write Status = In Progress**:

   ```bash
   gh project item-edit --id <item> --project-id <project-id> --field-id <status-field-id> \
     --single-select-option-id <in-progress-id>
   ```
3. **Assign the developer**: `gh issue edit <n> -R <owner/repo> --add-assignee <viewer.login>`.

**Stop the claim at the first board write that fails** — the item add or the Status. The assign is not a
board write. After a failed board write, read the card back once and report what it shows, because a
write that timed out may have landed; quote the error, repair nothing, and report `CLAIM-FAILED`. Where
the error names a missing `project` scope, name `gh auth refresh -s project`. Then go on to DESCRIBE:
whether to work a card the claim left unclaimed is the developer's call at the route.

**An assign that fails, for any reason, is `NOT-ASSIGNED`, never `CLAIM-FAILED`.** Quote the error and
assign no one else. An assign that exits 0 but reads back without `viewer.login` is `NOT-ASSIGNED` too:
the forge may drop an assignee it will not accept without an error.

With no board block, or a block missing any constant `../SKILL.md` lists, name `/phil:board-setup` and
write no Status: skip steps 1 and 2, report `NO-BOARD-BLOCK`, and still assign. Never choose a Status
option by its name: the block's option id is the only one the claim writes.

## The read-back

**Read the claim back** with the number query, and check each write that ran or was skipped as already
made:

- **Status** reads `In Progress` on the board's project — only where a board block exists and the
  Status write did not fail.
- **`viewer.login`** is among the assignees — only where the assign did not fail.
- **Every login RESOLVE read among the assignees** is still there. A missing one is
  `READ-BACK-MISMATCH`, naming the login.

Projects v2 reads lag writes, and this grant has no way to wait, so the re-read runs at once: re-read once
before concluding, and say a surviving mismatch may be lag. A difference that survives the re-read is
`READ-BACK-MISMATCH`: report it as found, and repair nothing. Where the board's add-to-project workflow is
enabled, name it as a likely cause of a Status that reads back Todo.

**A read that fails after the claim's first write leaves the claim unverified**: report
`READ-BACK-MISMATCH`, quoting the error, and never `CLAIMED`.

A card that reads back In Progress on the board and assigned to the developer, with every earlier
assignee in place, is `CLAIMED`, whether this run wrote it or found it so.

## The claim line

The report prints one claim line, after the CARD line:

```
CLAIMED: Status In Progress, assigned to pmvanev — read back
CLAIMED: already In Progress and assigned to pmvanev — nothing written
CLAIMED: added to the board, Status In Progress, assigned to pmvanev beside colleague — read back
NO BOARD BLOCK: Status not written — run /phil:board-setup; assigned to pmvanev — read back
NOT ASSIGNED: Status In Progress — read back; assigning pmvanev failed: <error>
NOT ASSIGNED: Status In Progress — read back; the assign exited 0 and pmvanev is not among the assignees
CLAIM FAILED: added to the board; the Status write failed: <error> — read back: Todo, unassigned
READ-BACK MISMATCH: wrote In Progress, read Todo after a re-read — may be lag
READ-BACK MISMATCH: colleague is no longer among the assignees
```

Where two outcomes fire, as `NO-BOARD-BLOCK` and `NOT-ASSIGNED` do together, print both clauses on one
line.
