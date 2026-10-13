# Expected outcome — fixture 02 (an enforced rule collapses to one line)

**Situation.** A five-sentence bullet explains a rule that `scripts/check-mutates.py` enforces. The
script exists in the fixture, and `tests/test_check_mutates.py` proves it refuses the motivating input.

**Pass.** The rule survives as one line: the reflex (every command declares `mutates:`) and the path
`scripts/check-mutates.py`. The explanation of what the check refuses is gone, because the script's
header owns it. The report lists the collapse and names the proven script.

**Fail.**
- The rule is deleted outright — the declaration still binds authors.
- The explanation of the check's behaviour survives in `CLAUDE.md`.
- The run writes, edits or proposes a new script — the check already exists.
