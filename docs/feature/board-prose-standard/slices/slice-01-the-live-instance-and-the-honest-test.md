# Slice 01 — The live instance, and the honest test

**Goal:** Make the block's composed sentences name the clarity standard, then re-render issue #36's seven
roster descriptions under it and report the word delta either way.

**Stories:** S1 (read a roster description where both lines carry information)
**Answers:** issue #40's open questions 1 and 3, at one surface

## Learning hypothesis

**Disproves [D2] — naming as the mechanism — if seven descriptions composed under a named standard come
out indistinguishable from the seven composed without one.** If KPI-3 shows no delta, the answer to
question 1 is not "name it", and slices 02 and 03 must be re-scoped to apply-before-write before five
more surfaces inherit a mechanism that does nothing.

**Confirms**, if the delta is real, that a citation changes composed text, and that the remaining
surfaces can be cited at a paragraph each.

**This slice exists to be able to fail.** The card's chosen mechanism is the one `CLAUDE.md` records as a
defect twice; measuring it first is cheaper than discovering it at surface six.

## IN scope

- `skills/nwave-issue-board/SKILL.md`, at the point it requires the two-line description (`:134`) and at
  *Summarise what you link*: name `phil:eos` / `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` as the standard
  applied to those sentences.
- **[D4]'s boundary, stated as a refusal** because a scope given only positively gets read as a minimum:
  the standard applies to the two-line descriptions and the summarising clauses, and **not** to glyphs,
  header lines, timestamps, or any derived cell.
- **The one-writer compatibility sentence.** The block regenerates whole from one writer; a standard the
  writer applies to sentences it composes adds no second writer. Stated in the skill, because an author
  meeting the new citation will otherwise ask exactly this.
- Re-render issue #36's seven roster descriptions. Record before and after word counts. **Report the
  delta whichever way it goes.**
- Two fixtures in the existing `self-test/`: one roster description composed under the standard, and a
  padded variant that fails.
- Version bump.

## OUT scope

- Every other surface — slices 02 and 03.
- `issue-board`'s missing suite — slice 02, even though it is the load-bearing half. Coupling it here
  would mean a failed hypothesis wasted the suite-creation cost too.
- Changing the row-count bound (C4/C8). It is correct and measures something else.
- Any editing pass at run time. That is the escalation this slice's failure would authorise, not
  something to build before the measurement.

## Acceptance criteria

1. The skill names the standard at both composition points, and states [D4]'s in/out boundary as a
   refusal list.
2. **KPI-3 reported, not assumed.** Seven descriptions, `wc -w` before and after. A "no change" result
   is written into the slice outcome as [D2] disproven — reporting it as success is the failure this AC
   exists to prevent.
3. **KPI-4 at this surface: 0.** No description gets longer.
4. Two fixtures pass; the padded variant fails for the stated reason rather than incidentally.
5. **Every existing `nwave-issue-board` fixture passes unchanged.** A citation that alters shipped output
   is a wrong citation, whatever it says about prose.

## Dependencies

Issue #36 closed and its block stable, so the before-measurement cannot move underneath the slice.

## Dogfood moment

Same day: re-read the re-rendered block on issue #36 against Morgan's thirty-second budget, and say
whether the descriptions read better — a judgement recorded beside KPI-3's number, not instead of it.

## Effort

Half a day. One skill file, two fixtures, one measurement.

## Reference class

`story-spans-features` slice 01 — a hand-built block on a real card, measured against a read budget.
That slice is the source of the seven descriptions this one re-renders.

## Taste tests

| Test | Verdict |
|---|---|
| Ships 4+ new components? | No — one skill file, two fixtures |
| Depends on a new abstraction? | No — `phil:eos` and the self-test harness both ship |
| Disproves a pre-commitment? | **Yes — [D2], the card's own chosen mechanism** |
| Synthetic data only? | No — issue #36's seven live descriptions |
| Identical to another slice but for scale? | No — 02 creates a suite, 03 cites four surfaces |
