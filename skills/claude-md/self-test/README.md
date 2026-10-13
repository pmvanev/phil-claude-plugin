# claude-md — Self-Test

`/phil:claude-md` fails silently. A cut rule, a reworded generated region or a deleted history all
look like a tidy file. Each fixture here pins one such failure.

| Fixture | Pins | Pass |
|---|---|---|
| `01-generated-region-untouched/` | Safety: generated regions | Bytes between the markers unchanged |
| `02-enforced-rule-collapses/` | Revision rule 3 | One line naming `scripts/check-mutates.py` |
| `03-prohibition-becomes-reflex/` | Revision rule 5 | Three constraints survive in positive form |
| `04-history-kept-when-unrecoverable/` | Recoverability | History kept and flagged when no commit holds it |
| `05-unproven-check-keeps-prose/` | Revision rule 3 | Prose kept; the check reported found and unproven |

## Driving a fixture

Copy the fixture directory outside this repository. For fixtures 01–03 and 05, `git init` the copy and commit
it, so the skill finds a root and searches the copy's own `scripts/`. Leave fixture 04's copy
uncommitted. Run `/phil:claude-md <copy>/CLAUDE.md` and judge the result against `expected.md`.

Directory mode skips `self-test/`, so `/phil:claude-md` with no argument never touches these inputs.

## What runs automatically

`tests/test_claude_md_wiring.py` checks that the skill names both rules, that every fixture holds a
`CLAUDE.md` and an `expected.md`, and that fixture 01's markers pair up. It verifies the skill *says*
the right things, not that a run *does* them. A human drives the fixtures; nothing runs the skill
unattended.
