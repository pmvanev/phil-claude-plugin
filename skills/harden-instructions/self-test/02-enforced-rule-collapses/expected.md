# Expected outcome — fixture 02 (an enforced rule collapses to one bullet)

**Situation.** Run this fixture from a committed copy. A five-sentence bullet explains a rule that
`scripts/check-mutates.py` enforces, and buries a second, unenforced rule in its last sentence. The
script exists in the fixture, and `tests/test_check_mutates.py` proves it refuses every input the rule
names: `Write`, `Edit` and bare `Bash` under `mutates: false`, and a missing declaration.

**Pass.**
- The enforced rule survives as one bullet: the reflex (every command declares `mutates:`), the limit an
  author writes to (a `mutates: false` command grants no `Write`, `Edit` or bare `Bash`), and the path
  `scripts/check-mutates.py`.
- The second rule survives as its own bullet: watch a new check fail on the input that motivated it
  before trusting a green run. Its wound — the first version was written and never called — may stay as
  one line.
- The August audit story is gone.
- The file's last line is `Rationale and history cut <date>: git show <hash>:CLAUDE.md`, naming the
  copy's commit.
- The report lists the collapse, names the proven script, and names the history cut with its `git show`
  command.

**Fail.**
- Either rule is deleted outright — both still bind authors.
- The `Write`, `Edit`, bare `Bash` limit is cut — an author learns it only from a refusal.
- The audit story survives in `CLAUDE.md`.
- History is cut and no pointer line names where it went.
- The run writes, edits or proposes a new script — the check already exists.
