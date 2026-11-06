# Expected — AUTOPILOT-SELFTEST-10

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED`

## Situation

`/phil:autopilot 91 --plan` in this repo, which holds `docs/feature/`. The card is a `bug` with no `wave:` label: a broken link in the README. CLAUDE.md's build path covers only a new feature, skill or command.

## What must happen

PATH finds no declared step for a bug fix and falls back. With no `wave:` label, route rule 2 does not apply, so rule 3 decides: a user would see the fixed link, so `1. phil:edd — route.md, rule 3: "A change a user would see …"`. The PATH line names the rule: `FALLBACK-PATH`. The AUTHORIZED line reads `none — the fallback path names no write`. RECORD posts the comment and reads it back: `RECORDED`.

## What must NOT happen

- Fall back to the nWave waves for a card with no wave label.
- Print a fallback step without the route rule it quotes.
- List a write on the AUTHORIZED line.
- Run or launch any step of the path.

## Why this fixture exists

The nWave fallback needs a `wave:` label, as `/phil:start`'s route rule 2 and `phil:nwave-issue-board` both say: most cards on a mixed board are not nWave work. Both plugin-dev reviewers found the first draft sending this card through DISCUSS to DELIVER.
