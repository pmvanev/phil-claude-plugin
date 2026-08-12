# Expected outcome — fixture 15 (a count that is maintained by hand is not a rollup)

**Where it fails silently.** GitLab really will report `2 of 4` from a roster written as `- [ ] #101`
checkboxes, and on the day it is written the number is correct. But a checkbox is ticked by a person
and a slice issue is closed by the work, so the two authorities diverge the first time anyone forgets
one of them — and what the feature displays is the state of the checkboxes. The failure is invisible
in exactly the way the rest of this suite guards against: a feature reading `2 of 4` while three
slices are closed looks like a healthy board, not a broken one. The bare-reference roster has no
such gap, because each `#N` renders the issue's own live state and nothing caches a total.

The tier is Premium on purpose. Premium is what would normally unlock a real child-issue rollup, and
here it does not, because the project sits in a personal namespace and epics need a group. A fixture
set to Free would pass for the weaker reason that nothing was available anyway.

**Expected decision:** `ROSTER-NOT-CHECKBOXES`.

**Checkable assertions (all must hold):**

1. The roster in the feature description stays a list of **bare `#N` references**. No `- [ ]` or
   `- [x]` markers are introduced anywhere in it.
2. No slices-done count is written into the feature description or the generated block — on GitLab
   the honest answer is the roster's live states, not a total.
3. The closed slices are not hand-marked. `#101` and `#102` already render as closed; nothing
   restates it.
4. If a feature-level bar is asked for explicitly, the answer offered is a **milestone** holding the
   slice issues, per *A parent's "N of M done" counts different things on each forge* in
   `phil:issue-board` — not checkboxes, and not a hand-kept tally.
5. Nothing here restates the GitLab rollup field names or their tier and stability; those live in
   `phil:issue-board`.

**Gate failure (blocks the skill change):** a roster converted to checkboxes to manufacture a
progress bar; OR a slices-done count written into the description or the generated block on GitLab;
OR a closed slice hand-marked in the roster.
