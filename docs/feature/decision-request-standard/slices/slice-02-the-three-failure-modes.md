# Slice 02 — The three failure modes become fixtures

**Goal:** Pin the three measured ways a decision request goes wrong, so each is caught by a test rather
than rediscovered by a reader.

**Stories:** S3 (see a malformed ask actually fail)
**WS strategy:** n/a — slice 01 holds the skeleton

## Learning hypothesis

**Disproves [D4] — the hard ceiling** — if the count cannot be applied to a real request without either
evicting what turns on it or forcing the decision to be split. [D4] is the largest untested commitment in
the feature: a hard ceiling that starts squeezing framing is being applied backwards, and the honest
outcome would be to reopen it as a target with the mechanism cost stated.

**Disproves [D9] — placement is part of the standard** — if *buried* cannot be pinned at all. Modes 1 and
2 are wording and are obviously testable. Mode 3 is placement, and it is entirely possible that no fixture
can express "correct wording, wrong position" in a way a check can read. If so, [D9] is a sentence rather
than a clause, and the standard covers two thirds of the reported problem — which must be stated, not
quietly dropped.

**Confirms**, if it passes, that all three reported failures are regression-testable, which is what
separates this from the prose that already failed.

## IN scope

- Fixture *bare-option-list* — options present, framing absent. Fails.
- Fixture *jargon-wall* — internal vocabulary inside the ask. Fails.
- Fixture *buried-ask* — wording that would pass, placed inside surrounding output. Fails **on placement**.
- Fixture *conforming* — passes all three checks.
- The word-count assertion from slice 01, generalised to run over any fixture.
- A decision, recorded, on whether fixtures live beside the fragment in `skills/shared/` or in a
  `self-test/` directory — `skills/shared/` holds no fixtures today, so this slice sets the precedent
  either way and should set it knowingly (feature delta, *Open* item 1).

## OUT of scope

- Propagation to other askers and the check script — slice 03.
- The conversational half — slice 04.
- Any attempt to detect these modes automatically in live output. The fixtures pin the **standard**, not a
  linter over conversation; conflating the two would promise enforcement [D11] says does not exist.

## Acceptance criteria

- **AC1** Fixture *bare-option-list* fails, and its failure names the missing framing rather than a count.
- **AC2** Fixture *jargon-wall* fails, and names at least one forbidden token by category.
- **AC3** Fixture *buried-ask* fails **on placement**, with wording that passes AC1 and AC2 — this is the
  fixture that decides [D9].
- **AC4** Fixture *conforming* passes all three checks and the count.
- **AC5** The count runs on slice 01's real recorded request, not a synthetic one.
- **AC6** Each fixture is proven to fail **before** the check is trusted — `CLAUDE.md`'s standing rule,
  written after `check-readonly-commands.py`'s first version silently passed.
- **AC7** If AC3 cannot be met, that is recorded in the Result section and [D9] is amended in the feature
  delta rather than left standing.

## Dependencies

**Slice 01** — needs the fragment to test against and its real recorded request for AC5.

## Effort · reference class

**≤1 day.** Reference class: `groom-issues` self-test fixture additions, and `board-setup-block` slice 04
(a taxonomy pinned by fixtures, one day). Three fixtures plus one generalised assertion.

## Pre-slice SPIKE

**Consider one, timeboxed to an hour, for AC3 only.** Whether "correct wording, wrong placement" is
expressible as a fixture is a genuine unknown, and it is the one thing here that could fail for a
structural reason rather than a work reason. A cheap probe before committing the slice is worth it; if it
comes back negative the slice still ships modes 1 and 2 and amends [D9].
