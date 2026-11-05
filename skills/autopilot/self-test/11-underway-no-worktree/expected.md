# Expected — AUTOPILOT-SELFTEST-11

`PLANNED` · `CLAIMED` · `UNDERWAY` · `DECLARED-PATH` · `RECORDED`

## Situation

`/phil:autopilot 76` from the main checkout. The card is In Progress, assigned to the developer. The developer's pull request 108, naming issue 76, is open on `worktree-issue-76-…`, and this machine holds no worktree for it. The card has no autopilot comment.

## What must happen

The claim finds every write already made: `CLAIMED`. WORKTREE finds the open pull request and cuts nothing: `UNDERWAY`, with start's line printed without its `next: /phil:resume` clause, saying the session is not in the card's worktree. PATH reads the main checkout's CLAUDE.md and prints the declared path: `DECLARED-PATH`. RECORD posts the comment and reads it back: `RECORDED`.

## What must NOT happen

- Cut a worktree.
- Say the session is in the card's worktree.
- Name `/phil:resume` as the next step.
- Run or launch any step of the path.

## Why this fixture exists

`/phil:start` cuts nothing for an open pull request with no worktree here and names `/phil:resume`; autopilot drops that clause, says where the session is, and still prints and records the path. The plugin-validator found this case undefined.
