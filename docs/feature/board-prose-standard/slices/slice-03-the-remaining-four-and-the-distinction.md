# Slice 03 — The remaining surfaces, and the distinction

**Goal:** Bring the last four prose-generating surfaces to KPI-1, and write [D6] — judging is taste,
generating is not — where the next author of a board surface will meet it.

**Stories:** S2 (elicited purpose), S3 (set-level comments and ranking basis), S4 (`@infrastructure`)
**Answers:** issue #40's done-conditions 1, 2 and 4

## Learning hypothesis

**Disproves "one distinction covers every surface" if any of the four needs a different rule.** [D6] is
one sentence asserted to hold across elicitation, set-level comments, the ranking basis, the projected
handoff prose and the `assumed`-line rationales. Elicitation is the likely counterexample: it writes
words a human supplied, so "your own output" is not obviously what it produces.

**Confirms**, if one sentence holds, that this is a convention rather than five local rules — and a
convention is what `CLAUDE.md` route 2 can carry.

**The elicitation case is the reason this slice is last.** If [D6] needs a clause for words a human
supplied, that clause is discovered here and nowhere earlier.

## IN scope

- `skills/groom-issues/SKILL.md` + `commands/groom-ask.md`: name the standard for the purpose and
  done-condition elicitation composes. **Scoped to composed text**, so a verbatim answer is untouched.
- `commands/groom-set.md`: the merge, split and closing comments.
- `commands/rank-issues.md` + `skills/rank-issues/SKILL.md`: the recorded ranking basis. **Cite
  `issue-board`'s `## Chain` convention, never restate it** — the restate-versus-reference fault this
  repo has caught three times.
- `skills/session-handoff/SKILL.md`: the projected `Why` / `Next` / `Stack` prose, per [D4].
- `skills/board-setup/SKILL.md` + `commands/board-setup.md`: the `assumed`-line rationales. **The probed
  lines are out** — they are derived, and a rationale is composed.
- **[D6], written at `groom-issues`' *well-formed issue* standard**, where the checkability argument it
  extends already opens. Not in a new section: an author reading the standard meets it there.
- **`CLAUDE.md`, route 2**: record that a board surface naming a prose standard ships a fixture with it.
  A convention with no mechanism is what already failed here.
- Version bumps.

## OUT scope

- **Any change to the five structural items.** KPI-5 guards it. If this slice adds a style item to the
  scan, it has misread the card. *(Corrected from "four" during the slice: there were always five — item 5
  is the `## Chain` section, and it already demands the reason, not only the edge.)*
- A fifth provenance label in elicitation. *I rephrased your answer* already covers a tightened write.
- `phil:ai-eos`, `phil:red-team-prose`, and any new rule in `rules/`.
- Retro-editing prose already written onto cards. The standard governs what is composed next.

## Acceptance criteria

1. **KPI-1: 6 of 6.** The grep from the delta's *measurement, re-taken* returns non-zero for all twelve
   files.
2. **KPI-5: the scan's five structural items are byte-unchanged.** `git diff` against the prior commit.
3. **KPI-4: 0 surfaces longer.** Word count per surface, before and after.
4. [D6] is stated at the `groom-issues` standard, and it is **one sentence covering all five surfaces**
   — or the counterexample is recorded with the clause it needed.
5. `CLAUDE.md` carries the fixture-with-citation requirement.
6. `rank-issues` cites the chain convention; a restatement fails this AC.

## Dependencies

Slices 01 and 02. This slice spends the per-surface cost that 01 justified and 02 priced.

## Dogfood moment

Same day: run `/phil:groom-ask` against a real title-only card on this board — issue #34 or #39, both of
which want shorter output — and read the written purpose. **KPI-4 is checked against the neighbours this
feature could most easily harm.**

## Effort

One day. Nine files, mostly a paragraph each; the [D6] sentence is the part that can take longer than it
looks.

## Reference class

`story-spans-features` slice 05, which adapted grooming and ranking to a new paradigm across the same
command set — and which is where the seven unedited descriptions came from.

## Taste tests

| Test | Verdict |
|---|---|
| Ships 4+ new components? | No components — nine citations and one sentence |
| Depends on a new abstraction? | No — [D6] is a distinction, and the card supplies it |
| Disproves a pre-commitment? | Yes — that [D6] is one rule rather than five |
| Synthetic data only? | No — the dogfood runs against live cards #34 and #39 |
| Identical to another slice but for scale? | No — the only slice carrying the cross-surface convention |
| Only `@infrastructure` stories? | No — S2 and S3 carry user-visible value; S4 ships alongside |
