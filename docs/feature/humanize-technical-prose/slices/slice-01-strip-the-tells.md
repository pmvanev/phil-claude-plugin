# Slice 01 — Strip the tells

**Goal (one sentence):** `/phil:humanize-technical-prose <file>` rewrites every tell `phil:ai-eos`
finds in a committed draft, re-checks, and reports, with no profile needed.

Story 1 · Decisions D1, D10, D11, D12, D13, D15.

## IN scope
- `commands/humanize-technical-prose.md` (`mutates: true`, D15) and
  `skills/humanize-technical-prose/SKILL.md`, after reading `plugin-dev:command-development` and
  `plugin-dev:skill-development`.
- Refuse a file git does not have committed (D12).
- Load `phil:ai-eos`'s catalogue, take its findings, rewrite each in the plain form it names, then
  re-run the detector over the changed sentences (D1, D10).
- Protected spans stay byte-for-byte (D11).
- The report: tells found, rewritten, and left after the re-run, by line. It follows
  `rules/writing.md`, and the citation's test is watched failing first.
- Fixtures: a draft with tells; a draft with uncommitted changes; a tell inside a code block that must
  stay; a rewrite that would otherwise add a new tell.

## OUT of scope
- The profile, the voice pass and the slips (slices 02–04).

## Learning hypothesis
- **Disproves** "the catalogue's own plain forms clear a tell without creating another" if the re-run
  finds a new tell in two of three real drafts.
- **Confirms** it if the re-run finds none across three real drafts.

## Acceptance criteria
AC1.1–AC1.4 in `feature-delta.md`.

## Dependencies
None.

## Effort estimate
≤1 day. Reference class: `phil:red-team-prose`'s fix step, run without its other two passes.

## Production data
Three documents in this repo that Claude drafted, such as a slice brief, a README section and a rule.

## Dogfood moment
The same day, run it over this feature's own `feature-delta.md` and read the diff.
