# The drift report and the retire offer — the incidents behind the rules

`SKILL.md` states the rules. This file records what bought them. Read it before changing the
evidence floor, the flattening depth, or any retire-offer rule.

## Two defects the first dogfood run found, 2026-08-17

Both made the report look **better** than it was, which is this feature's own failure mode turned on
itself: a false confirm asserts the prose was checked and found sound.

**A probed scalar shorter than six characters is not evidence.** The probe returns `number: 3` for
the project and `option_count: 4` for the Status field. Substring-matching those against prose
produced **nineteen confirms** on this repo's real section — one of them resting entirely on a line
containing the digit 2. The floor is six characters, which keeps eight-digit option ids like
`39094273` as evidence while dropping bare counts. Pinned by
`test_a_short_scalar_is_not_evidence_of_anything`.

**Fact values are walked to full depth.** `column-families` nests its option ids as a list of dicts
inside the fact's value. A one-level walk stringifies that list, matches nothing, and files the line
stating all four option ids — the constant whose full-replacement hazard nearly destatused 25
cards — under `cannot evaluate`. Pinned by `test_option_ids_nested_inside_a_fact_are_evidence`.

Neither was reachable from the unit tests as first written, and neither would have been visible in
the finished file. The dogfood found both, which is the argument for running against a real board
rather than a fixture.

## Why line numbers are counted over the excised file

The report must be identical before and after placement. Numbering the file with the region removed
achieves that for free, because placement is built so excision restores the original byte-for-byte.

The alternative — numbering the file as it stands — would make the same prose report different line
numbers once a region sat above it, and would let the generated region's own values appear in
`confirms`. **The region agreeing with the probe is a tautology, not a confirmation.**

## A truncated-but-correct id lands in `cannot evaluate`

Prose carrying a shorthand id (`PVT_kwHOANPp…` for the full token) is cleared from `contradicts` by
the substring test, but does not reach `confirms`, which needs the full value present. The line is
reported as unjudged rather than as agreement. That is the honest answer — the prose does not
actually state the constant — but it is a case a reader of the `confirms` definition would not
predict.

## Why the retire offer deletes rather than corrects

Correcting a contradicting line is the obvious helpful act and it is wrong twice over. It edits
prose the human owns, and it destroys the evidence that the two sources disagreed — which is the
finding, not a problem to be tidied away before anyone reads it.

Deleting a whole line is reviewable in a diff. Rewriting one is an edit nobody asked for, and in a
file of hazards recorded after contact, the rewritten version may be the wrong one.

**Silence is not consent.** A declined offer leaves no trace at all — no comment, no marker, no note
that it was declined. A record of the declining would itself be a change outside the markers.

**A `cannot evaluate` line is never offered.** There is no evidence it is wrong, so there is nothing
to retire it in favour of. Offering anyway would convert absence of evidence into a prompt to
delete, which is how a board's habits come to audit themselves.
