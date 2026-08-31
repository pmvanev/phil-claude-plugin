# Expected outcome — fixture 04 (the exemption is the rule here)

**Pins:** *"Inherently 2-D content or essential orientation — tables, maps, diagrams, and indented code
are exempt from reflow (1.4.10)."*

**Expected outcome:** `EXEMPT-NOT-FLAGGED`. No reflow finding.

**This is the one actively harmful failure in the suite.** Every other fixture guards against a
reviewer that misinforms. This one guards against a reviewer that **directs**: a must-fix citing
1.4.10 tells an author to make a fourteen-column ledger reflow into a single column, and an author who
complies destroys a table that was already conformant. The finding cites a real success criterion, in
the right format, at the right severity — and following it makes the product worse.

**Why the shape is so convincing.** The observable fact is true: the content does scroll in two
dimensions at 320px. The reviewer sees a real symptom, matches a real criterion, and produces a real
citation. Only the exemption separates a correct pass from a damaging finding, and the exemption is one
clause long.

**Gate failures:**

- Any reflow / 1.4.10 finding against the table, at any severity.
- Recommending a card layout, stacked rows, or "responsive table" pattern as a fix for a defect that
  does not exist.
- Raising it as **consider** with a note to verify at runtime. The exemption is categorical; it is not
  a question the rendered page settles.
