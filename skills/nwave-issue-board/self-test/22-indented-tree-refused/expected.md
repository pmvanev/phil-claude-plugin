# Expected outcome — fixture 22 (an indented tree is the same wall, flat)

**Pins:** the refusal *"no slices indented as sub-rows of the feature roster."*

**Expected: refused**, with the reason — the rendering enumerates the slices of features that are not
current, and the bound is about **what is enumerated**, not about how many tables it is spread across.

**Why this is the fixture that matters most in this slice.** The correct answer and the failure are one
word apart. *"Features, with slices demoted a level"* is question 1's own phrasing, and *indenting* is
the reading a careful person reaches first. It even looks like compliance: one table instead of four,
visibly hierarchical, and every fact present. **It renders the same 28 rows** — four feature rows plus twenty-four slice sub-rows.

A bound stated only as *"the roster and the current slice's steps are the only tables"* would have
**passed** this rendering — one table, therefore within the count. That is exactly why the bound was
restated as a purpose, and this fixture is the proof the restatement was necessary rather than cosmetic.

**What was actually wanted.** Slices move to a **second table** scoped to the current feature. "Demoted
a level" describes where a slice sits in the *hierarchy of the story*, not where its row sits in a table.

**Gate failures:**

- Accepting the rendering because it is one table. The defect, stated.
- Accepting it because every fact is present. Completeness is the failure mode here, not the goal.
- Accepting a collapsed or `<details>`-wrapped variant. Rows a reader must expand are still rows, and a
  forge that does not render the disclosure shows all 24.
- Refusing it on the grounds that indentation is ugly. That is taste; it would be argued away at the
  next reading. **There are two real grounds and both must be available**: it breaches the bound at
  scale, *and* it puts both glyph vocabularies in one table — `▶ in progress` on a feature row above
  `▶ current` on a slice sub-row. Refusing on scale alone leaves the rendering defensible at two
  features of one slice, where the scale argument evaporates and the collision does not.
- Refusing without naming the second-table remedy. A refusal that does not say what to do instead gets
  worked around.
