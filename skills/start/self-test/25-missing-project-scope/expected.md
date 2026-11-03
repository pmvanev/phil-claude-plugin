# Expected — START-SELFTEST-25

`NOT-LAUNCHED` · `CLAIM-FAILED`

## Situation

`/phil:start 98`. The card is on the board in Todo. `gh project item-edit` fails: `your authentication token is missing required scopes [project]`. The developer answers **not now**.

## What must happen

The run reads the card back once — Todo, unassigned — and reports `CLAIM FAILED: the Status write failed: … — read back: Todo, unassigned`. It names `gh auth refresh -s project` and goes on to describe and route the card.

## What must NOT happen

- Assign the developer after the failed Status write.
- Retry the Status write.
- Report CLAIMED.

## Why this fixture exists

D8: the claim stops at the first write that fails, and `phil:issue-board` names the scope `gh auth login` omits.
