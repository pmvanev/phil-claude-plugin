# Expected — START-SELFTEST-10

`NO-MATCH` · `WROTE-NOTHING`

## Situation

`/phil:start 87`. `issueOrPullRequest` answers with `__typename` `PullRequest`.

## What must happen

The report says 87 names a pull request, not a card, and stops.

## What must NOT happen

- Describe the pull request as a card.
- Search for an issue the pull request mentions and start it.
- Write a Status or assign anyone.

## Why this fixture exists

A number names an issue or a pull request on GitHub; a pull request is no card.
