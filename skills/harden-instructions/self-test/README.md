# harden-instructions — Self-Test

`/phil:harden-instructions` fails silently. A cut rule, a reworded generated region or a deleted history all
look like a tidy file. Each fixture here pins one such failure.

| Fixture | Pins | Pass |
|---|---|---|
| `01-generated-region-untouched/` | Safety: generated regions | Bytes between the markers unchanged |
| `02-enforced-rule-collapses/` | Revision rule 3 | One bullet keeping the `Write`/`Edit`/`Bash` limit and naming `scripts/check-mutates.py`; the buried rule kept; pointer added |
| `03-prohibition-becomes-reflex/` | Revision rule 5 | Three constraints survive in positive form |
| `04-history-kept-when-unrecoverable/` | Recoverability | History kept and flagged when no commit holds it |
| `05-unproven-check-keeps-prose/` | Revision rule 3 | Prose kept; the check reported found and unproven |
| `06-skill-keeps-frontmatter-and-shape/` | Profiles; Safety: frontmatter | Frontmatter unchanged; no project-memory layout imposed |
| `07-pointer-kept-when-nothing-cut/` | Recoverability | Earlier pointer byte-for-byte unchanged |

## Driving a fixture

Copy the fixture directory outside this repository. For fixtures 01–03 and 05–07, `git init` the copy and commit
it, so the skill finds a root and searches the copy's own `scripts/`. Leave fixture 04's copy
uncommitted. Rename fixture 06's `SKILL.md.input` to `SKILL.md` in the copy — it ships renamed so
skill discovery never loads it. Run `/phil:harden-instructions <copy>/<input>` and judge the result against `expected.md`.

Directory mode skips `self-test/`, so `/phil:harden-instructions` with no argument never touches these inputs.

## What runs automatically

`tests/test_harden_instructions_wiring.py` checks that the skill names its rules, that every fixture holds an
input (`CLAUDE.md` or `SKILL.md.input`) and an `expected.md`, and that fixture 01's markers pair up. It verifies the skill *says*
the right things, not that a run *does* them. A human drives the fixtures; nothing runs the skill
unattended.
