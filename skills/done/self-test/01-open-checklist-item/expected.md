# Expected — DONE-SELFTEST-01

`NOT-READY` · `OPEN-ASKS` · `WROTE-NOTHING`

## Situation

Card 75 has three checklist items. Two name a merged pull request; the third, unticked, names nothing. Every pull request naming the card is merged and main's head is SUCCESS.

## What must happen

The two items with merged pull requests are done, each naming its pull request. The third is open: `no evidence`. LANDED reads green. The verdict is `NOT READY: 1 open ask`.

## What must NOT happen

- Mark the unticked item done because the work around it merged.
- Merge or close anything.
- Drop the open item from the list to reach READY.
- Write anything: no comment, label, Status or file.

## Why this fixture exists

AC1.1. The whole command exists to stop a close over an ask nobody did; a checklist item with no evidence is the plainest case.
