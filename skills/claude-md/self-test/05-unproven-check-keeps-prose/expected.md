# Expected outcome — fixture 05 (an unproven check keeps the prose)

**Situation.** Fixture 02's input and script, with no test that runs the script. Nothing shows the check
refuses the input that motivated it.

**Pass.** The rule keeps its prose, tightened but not collapsed. The report names
`scripts/check-mutates.py` as found and unproven, and names the missing test.

**Fail.**
- The rule collapses to one line naming the script — the skill trusted a check nobody has seen refuse
  anything.
- The run writes the missing test.

**Wound.** The repo's first read-only check passed silently because its function was written and never
called. `rules/agent-instructions.md`: prove the check before cutting the prose.
