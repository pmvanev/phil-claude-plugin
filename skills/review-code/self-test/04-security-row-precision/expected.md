# Expected outcome — fixture 04 (row precision)

`probe.py` holds a board probe and two PreToolUse hooks. Each function sits on the edge of an
always-flag row, where the first dogfood run hesitated over whether the row fires. `test_probe.py` is green.

**Pins:** four precision rules in `rules/security.md` and `review-code`:

- An earlier call that happens to fail on hostile input is not a guard; the sink after it still fires.
- CWE-636 covers a security control that fails open, not a gate enforcing some other standard.
- CWE-1333 covers a quantified class beside a literal the class also matches, run on unbounded text.
- One defect matching two of a row's ids is one item, under the more specific id.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** the Priority 1 items in `expected-backlog.md`, matched on the Smell and on a Refactoring that is
the row's Preferred form verbatim, alone or followed by ` — here: ` and this code's one change:

1. **CWE-88** — `repo_labels` passes the model-composed slug to `gh repo view` as a positional argument.
2. **CWE-943** — `repo_labels` `%`-formats owner and name into a GraphQL literal. The `gh repo view`
   call before it fails on most hostile slugs, by accident, and guards nothing.
3. **CWE-1333** — `FILE_PATH` puts `[\w./-]*` beside `\.`, which the class also matches, and `paths_in`
   runs it on a question of any length.
4. **CWE-636** — `protect_tests` lets the write through on any payload it cannot parse.

**Hard assertions (any failure blocks the skill change):**

- **No security item names `wording_gate`.** It fails open too, but it enforces a word count, not a security
  property, and says so.
- **No CWE-770 item beside the CWE-1333 one.** The missing length limit and the backtracking pattern
  are one defect; the more specific id names it.

**Not a failure:** a CWE-180 item on `protect_tests`' raw-path check, once the rule carries that row;
items about structure or naming; line numbers within ±2.
