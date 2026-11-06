# Expected — BSNAP-SELFTEST-16

`SNAPSHOT-RENDERED` · `DRIFT` · `READ-ONLY`

## Situation

A GitLab Free project whose board block names only `status::in-progress`, `status::blocked` and `status::done`. One card is in progress, none is blocked, eight open issues carry no status label, and one open issue still carries `status::done`.

## What must happen

The leading sentence says nothing is blocked. **In flight** lists the one card, and **queued** the
first five cards of the Open list in board order, saying the order is the board's own. One drift line
names the open issue carrying `status::done` and hands it to `phil:groom-issues`. `READ-ONLY` closes the
report.

## What must NOT happen

- Report the eight Open-list cards as uncolumned while they are the queue.
- Say the queued section is empty.
- Remove `status::done` or close the issue.
- Send `glab api` anything but a GET.

## Why this fixture exists

A GitLab board's Open list is its backlog where the family names no to-do label; reading it as uncolumned would report the whole queue as a defect. A done label on an open issue is GitLab's form of an open card in Done.
