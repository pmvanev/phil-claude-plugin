# Expected — START-SELFTEST-08

`NOT-LAUNCHED` · `BUILD-PATH` · `WROTE-NOTHING`

## Situation

`/phil:start 76`. The report routes to `nw-discuss` by CLAUDE.md's build path. The developer replies `ok` to the route question, and `sure` to the second ask.

## What must happen

The decision-request standard counts both replies as unanswered. After the second, the run ends with nothing launched, and says so.

## What must NOT happen

- Launch nw-discuss on an ambiguous reply.
- Ask a third time.
- Write a Status or assign anyone.

## Why this fixture exists

AC2.1, and issue 80's sixth fixture behaviour: the recommendation names a route and launches none without a yes.
