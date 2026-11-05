# Slice 04 — Exactly the slips asked for

**Goal (one sentence):** with `--slips N`, the run adds exactly N slips of the kinds the profile holds,
grammar kinds unless `--misspellings` is given, none in a protected span, each reported by line.

Story 4 · Decisions D6, D7, D8, D11, D13, D16, D17.

## IN scope
- Add exactly N slips, drawn from the profile's slip kinds in their proportions (D7), grammar kinds by
  default (D8). `--slips 0`, or no `--slips`, adds none (D6).
- Draw each misspelling's mechanism and each grammar slip's cause from the profile's proportions.
  Place a residue slip only in a sentence the voice pass reworded, when one ran (D16).
- Report how many of the profile's slips sat on a name or technical term in the samples, and so
  could not be mirrored (D17).
- No slip lands in code, a command, an identifier, a link, a number, a quotation, a name, a technical
  term, a heading, frontmatter or a table of data (D11).
- Run last, after the voice pass and its re-check (D10).
- Report each slip's line and kind, and warn that a later `phil:eos` or `phil:red-team-prose` run will
  fix them (D13).
- Fixtures: `--slips 2` adds exactly two, each reported; `--slips 0` adds none; a draft whose only
  open positions sit beside code; a profile with no grammar kinds and no `--misspellings`; a draft with
  fewer open positions than the count, where the run reports the shortfall; a residue slip after a
  voice pass, which must land in a reworded sentence; a `--misspellings` run whose mechanisms all
  appear in the profile; a profile built from the paper, whose report names the slips it could not
  mirror.

## OUT of scope
- A built-in slip catalogue (D7).
- Correcting slips the draft already held.

## Learning hypothesis
- **Disproves** "a profile's own slip kinds read as plausible" if the developer, reading the output,
  marks a slip as one they would never make.
- **Confirms** it if every slip in two real runs reads as one they might have made.

## Acceptance criteria
AC4.1–AC4.7 in `feature-delta.md`.

## Dependencies
Slice 02; slice 03 for the full order.

## Effort estimate
≤1 day. Reference class: slice 01's protected-span handling, applied to insertion instead of
rewriting.

## Production data
The thesis's 24 grammar slips, the essay's 29 misspellings and the co-written paper's 14 and 7, as
kinds, mechanisms, causes and counts only.

## Dogfood moment
The same day, run `--slips 2` on a real draft with the `formal` profile, and read where each landed.
