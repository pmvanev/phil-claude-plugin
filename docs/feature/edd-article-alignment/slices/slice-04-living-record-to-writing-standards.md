# Slice 04 — A living record for every run that built, written to this plugin's writing standards

**Goal (one sentence):** every run that built leaves a record whose composed prose has passed
`phil:red-team-prose`, with the evidence and the developer's own words untouched.

Story 5 · Decisions D2 (red-team-prose row), D9, D11.

## IN scope
- The trail for every run that built landed in slice 01; this slice adds challenges and waivers to
  what it records.
- Provenance per field (`you wrote` vs composed), as `phil:groom-ask` labels them.
- `phil:red-team-prose` over every composed document before it is written; auto-applicable fixes to
  composed words only; a `[fitness]` finding blocks done until fixed or waived.
- `evidence/` byte-identical to capture.
- New fixtures: evidence hash unchanged after prose review; a `you wrote` field untouched by an
  applied fix.
- `tests/test_edd_skill.py` fails without the `rules/writing.md` and
  `rules/technical-communication.md` citations, watched red first.

## OUT of scope
- Editing evidence or the developer's words, ever.

## Learning hypothesis
- **Disproves** "composed records need a prose pass" if `phil:red-team-prose` finds no
  `[fitness]` finding and nothing auto-applicable across two real records.
- **Confirms** it if a real record changes, or a teammate can answer "what does this do, and how do
  we know?" from it unaided.

## Acceptance criteria
AC5.1–AC5.5 in `feature-delta.md`.

## Dependencies
Slices 01–03 (the record carries what they produce).

## Effort estimate
≤1 day. Reference class: edd-loop slice 02's DOCUMENT step.

## Production data
The records from slices 01–03's dogfood runs.

## Dogfood moment
Hand one record to a reader who did not run it, the same day.

## Close-out (after this slice, before the work closes)
Run the editing passes Definition of Done item 8 lists in `feature-delta.md`: `/phil:harden-instructions`
over every instruction file the feature touched, and `phil:eos` over every rule and document it touched.
Then re-run `python3 -m pytest -q` and a by-hand fixture drive, cut the release, and tick issue 38's
checklist item with the merging PR named.
