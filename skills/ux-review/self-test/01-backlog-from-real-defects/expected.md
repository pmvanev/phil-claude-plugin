# Expected outcome — fixture 01 (the walking skeleton)

**Pins:** the whole path end to end — gather, analyse against the standard, write the backlog, report.

**Expected outcome:** `BACKLOG-WRITTEN`. Two must-fix findings, each naming the specific `ux.md`
principle and the preferred form:

- placeholder-as-label → *"Persistent visible `<label>`; placeholder is a hint, not a label"*
- no loading / empty / error state → *"Design every state; never assume data loads successfully"*

**Why this fixture is the skeleton rather than the interesting case.** Both defects are objective, both
are in the always-flag tier verbatim, and neither needs the rendered UI. If this one does not pass,
nothing else in the suite means anything — the remaining fixtures all test where the reviewer must
*stop*, and a reviewer that cannot start is not being tested by them.

**Gate failures:**

- Either defect missed. They are table rows in the standard, not inferences.
- A finding that does not name the principle it violates, or does not state the preferred form. Step 2
  requires both; a finding a reader cannot trace is an opinion.
- Raising either as **consider**. Neither depends on runtime.
- Writing the backlog anywhere but `.ux-review-backlog.md` in the project root.
- Padding the backlog toward exhaustiveness. Precision over volume is stated in the skill.
