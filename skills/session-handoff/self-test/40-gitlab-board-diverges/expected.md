# Expected outcome — fixture 40 (a GitLab board disagrees, and the check says so)

**Pins:** card 76's checklist, 2026-11-06 — `/phil:resume` checks whether a GitLab board agrees about
what is in flight, as it does on GitHub.

## Expected decision

1. **`RESUME-CURRENT`** — the commit matches and both dirty flags read clean.
2. **`BOARD-DIVERGES`** — the board's in-flight claim is the card carrying `status::in-progress`, card
   20, read from the label's column through `glab api` GETs in board order. The recorded next action
   continues card 58. Name both sides, label each with its source, and stop:

```
BOARD-DIVERGES — the two records of what is in flight disagree.
  snapshot Next (captured …): finish the owner panel on card 58's settings page, then land it
  board, status::in-progress: #20 Run the New Boston demo end to end in modive
```

## What must NOT happen

- Report `BOARD-UNREADABLE` because the forge is GitLab.
- Compare against the top `status::to-do` card while a card carries `status::in-progress`.
- Swap a label, assign the card or post a note: the read-back writes nothing.
- Send `glab api` anything but a GET.

## Why this fixture exists

Until 2026-11-06 the command's grant held only `gh`, so every GitLab repo read back `BOARD-UNREADABLE`
and the check never fired there. Card numbers and titles are modive's board on that day.
