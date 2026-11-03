# Expected — START-SELFTEST-08

`NOT-LAUNCHED` · `CLAIMED` · `BUILD-PATH`

## Situation

`/phil:start 76`. The report routes to `nw-discuss` by CLAUDE.md's build path. The developer replies `ok` to the route question, and `sure` to the second ask.

## What must happen

CLAIM adds nothing the board already holds, writes Status In Progress, assigns the developer, and reads both back: `CLAIMED`. The decision-request standard counts both replies as unanswered. After the second, the run ends with nothing launched and the card left claimed, and says so.

## What must NOT happen

- Launch nw-discuss on an ambiguous reply.
- Ask a third time.
- Undo the claim because nothing launched.
- Remove an assignee.

## Why this fixture exists

AC2.1, and issue 80's sixth fixture behaviour: the recommendation names a route and launches none without a yes.
