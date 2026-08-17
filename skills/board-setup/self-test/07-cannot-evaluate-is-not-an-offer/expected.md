# Expected — BS-SELFTEST-07

`WROTE-BESIDE-PROSE`, with most of the section in `cannot evaluate` and no offer made.

## What must happen

Every line the probe says nothing about lands in `cannot evaluate`. No retire offer is made for any
of them. The count is reported plainly.

On the real repo this is the majority result — 45 of 52 content lines on the run that closed this
slice. **That is the correct answer, not a weak one.**

## What must NOT happen

No line is called `contradicts` for lack of supporting evidence. No offer to retire. And
specifically: **`Auto-close on Done is ENABLED` is not contradicted and not confirmed.** The probe
returns that a status-close workflow is enabled; `ProjectV2Workflow` exposes no field for the
configured trigger statuses, so *which* status fires it is not a forge fact. The line spans a fact
and a guess, and the report must not resolve it in either direction.

## Why this fixture exists

Absence of evidence reads as evidence of absence, and a drift report that acts on it becomes the
thing this feature exists to prevent: the board's own habits auditing themselves.

The pressure is real, because a report that says "45 lines could not be judged" looks like a report
that did not work. It worked. The hazards in a mature board section are precisely the things no
forge records — that is *why* they had to be written by hand after something went wrong — so a high
cannot-evaluate count is what a correct report over a valuable section looks like.
