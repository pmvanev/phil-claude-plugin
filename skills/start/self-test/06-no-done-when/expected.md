# Expected — START-SELFTEST-06

`NOT-LAUNCHED` · `CLAIMED` · `NO-DONE-WHEN`

## Situation

`/phil:start 91`. The card asks to move the decision-request hook's word counter into a shared module. Its body has no checklist, no *Done when* and no *Acceptance criteria* heading, and no *Open questions*. Nothing a user sees changes. The repo is a consumer's whose CLAUDE.md holds a board block and records no build path; the card is open, in Todo, assigned to the developer, with no `wave:` label. The developer answers **not now**.

## What must happen

CLAIM writes Status In Progress and skips the assign, because the developer is already assigned; it reads both back: `CLAIMED`. DONE WHEN reads `the card does not say` and names `/phil:groom-ask`. ROUTE reads `phil:work` — nobody would see the change.

## What must NOT happen

- Write a done-when criterion of its own.
- Infer one from the title.
- Route inline.
- Edit the card's body.
- Assign the developer a second time.

## Why this fixture exists

AC2.3. A start report that supplies the missing criterion hides the gap the card's author must fill.
