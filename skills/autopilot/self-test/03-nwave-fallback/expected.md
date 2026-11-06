# Expected — AUTOPILOT-SELFTEST-03

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED`

## Situation

`/phil:autopilot 41 --plan` in a GitHub repo holding `docs/feature/`, whose CLAUDE.md records no build path. The card carries `wave: design`.

## What must happen

PATH falls back to the nWave waves, read from `phil:nwave-issue-board`'s *Work this with* table, starting at DESIGN, and names the rule: no declared path, an nWave repo, the card's `wave: design` label: `FALLBACK-PATH`. RECORD posts the comment and reads it back: `RECORDED`.

## What must NOT happen

- Start the path at DISCUSS when the card carries `wave: design`.
- Restate the *Work this with* table instead of reading it.
- Run or launch any step of the path.

## Why this fixture exists

D2's nWave fallback: with no declared path, an nWave repo takes the waves from the card's wave label onward.
