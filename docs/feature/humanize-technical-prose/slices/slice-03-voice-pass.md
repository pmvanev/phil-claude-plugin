# Slice 03 — The voice pass

**Goal (one sentence):** with `--profile <name>`, the run rewords the draft toward that profile, adds
nothing, brings back no tell, and reports how each measured feature moved.

Story 3 · Decisions D5, D10, D11, D13.

## IN scope
- Reword word choice, sentence rhythm, openers and contractions toward the profile. Add no claim,
  figure of speech, hook, analogy or joke (D5).
- Re-run `phil:ai-eos` over every changed sentence, and keep the plain form where a rewording tripped
  it (D10).
- Report each measured feature before and after against the profile, such as
  `median sentence 24 → 18 (profile 17)`, with the rewordings by line.
- Skip the pass when no profile is named or the named one is missing, and list the profiles that exist.
- Fixtures: a draft reworded toward `formal`; a draft reworded toward `essay`; a rewording that brings
  back a trailing participle and must be undone; a technical term, a code span and a quotation that
  must stay; a run with no profile. Passages quoted from the samples are approved by the developer
  one by one (D9).

## OUT of scope
- Slips (slice 04).
- Any figure of speech the draft lacks, even where the profile's samples show one (D5).

## Learning hypothesis
- **Disproves** "rewording toward counted features makes a draft read as the developer's" if the
  developer, shown the tells-only and the voiced output of one real draft unlabelled, cannot pick the
  voiced one as closer to theirs.
- **Confirms** it if they pick the voiced one.

## Acceptance criteria
AC3.1–AC3.5 in `feature-delta.md`.

## Dependencies
Slices 01 and 02.

## Effort estimate
≤1 day. Reference class: `phil:eos`'s rewrite discipline, steered by a profile in place of
Strunk and White.

## Production data
A real draft the developer is about to send, and the two profiles from slice 02.

## Dogfood moment
The same day, the unlabelled comparison in the learning hypothesis, on a real draft.
