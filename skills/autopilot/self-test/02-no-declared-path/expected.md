# Expected — AUTOPILOT-SELFTEST-02

`PLANNED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED`

## Situation

`/phil:autopilot 12 --plan` in a GitHub repo with no nWave directories and a CLAUDE.md that names a test command and a paradigm but no command or skill for any kind of work. The card asks for a new flag on the CLI's report.

## What must happen

The claim and the worktree run as `/phil:start` writes them. PATH finds no declared steps and falls back: `PATH (fallback — no build path in CLAUDE.md or AGENTS.md; a user would see the change): 1. phil:edd`, naming route rule 3: `FALLBACK-PATH`. The AUTHORIZED line says the fallback names no write beyond its route's own. RECORD posts the comment and reads it back: `RECORDED`.

## What must NOT happen

- Treat the test command or the paradigm as a declared step.
- Fall back without naming the rule that chose phil:edd.
- List a push, pull request or merge on the AUTHORIZED line.
- Run or launch any step of the path.

## Why this fixture exists

AC1.2: a repo with no declared path falls back, and says so with the rule that chose the fallback.
