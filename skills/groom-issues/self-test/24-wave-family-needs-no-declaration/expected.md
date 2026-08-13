# Expected outcome — fixture 24 (the family nobody chose)

An nWave repo that declares nothing. Two feature cards have accumulated wave labels; two other cards
pair `documentation` with `enhancement`. Rule 4 must fire on the first pair and go dark on the second,
**in the same run**.

**Expected decision:** `REPORT-DEFECT` **and** `REPORT-UNEVALUATED` together:

```
#31 — two values in the `wave` family: `wave: discuss` and `wave: deliver`.
      Rule 4. The wave family is single-valued — phil:nwave-issue-board: "the wave label
      is single-valued and must be swapped, not added". Mechanical: the newer wave is the
      one the artifacts support, and the older is removed in the same call.
#44 — same defect in the scoped spelling: `wave::design` and `wave::deliver`.

rule 4 partly unevaluated — `documentation` + `enhancement` on #12 and #19. This repo's
CLAUDE.md declares no project-local family, so nothing on the forge says whether that
pairing is a defect or two orthogonal facts.
```

**Why the wave family does not wait for a declaration.** It is the one family with a *documented*
failure mode, stated normatively upstream: a feature walked DISCUSS→DELIVER accumulates four labels
and the record of where it stands becomes unreadable while every command reported success. That
invariant is identical in every nWave repo, so making each repo hand-copy it guarantees that the repos
which forget are exactly the ones running blind on it. And they run blind *silently* — `unevaluated`
produces no findings, and no findings reads as compliance to anyone not checking which rules were
awake.

**Why the other half still goes dark.** `documentation` + `enhancement` is a defect or two orthogonal
facts depending on a convention no forge records, and no upstream skill has a position on it. Firing
there too would mean inferring the family from the labels in use, which makes the board's own habits
the rule that audits the board.

**Gate failures:**

- Reporting rule 4 wholly `unevaluated` because `CLAUDE.md` declares nothing. That is the bug this
  fixture exists for: the accumulation is real, mechanical, and visible in the payload already
  fetched.
- Firing on `documentation` + `enhancement` as well, on the grounds that the run is already reporting
  a rule-4 defect. The two halves of rule 4 have different authorities and resolve independently.
- Missing `#44` because the spelling differs. A family is matched on the prefix before `::` or `: `;
  a board may carry both spellings, and `phil:nwave-issue-board` prescribes each for a different forge
  tier.
- Reporting only `REPORT-DEFECT` and dropping the unevaluated note. A run that finds defects can still
  have rules that did not fully run, and a summary carrying findings looks complete in a way a clean
  one does not — which makes the omission *harder* to notice here than in fixture `09`.
- Treating this as licence to infer other families. Only `wave: *` moves; it moved because something
  upstream declared it, not because inference became acceptable.

**Contrast with `09`.** Fixture `09` is the same undeclared-family situation on a board with **no**
wave labels, and there rule 4 correctly reports nothing but `REPORT-UNEVALUATED`. Run the two
together: the difference between them is the whole of this change, and a session that treats them
alike has either broken `09` or failed `24`.
