# Slice 05 — Staleness and safe re-run

**Goal:** Make a second run cheap, honest and quiet — reporting exactly what the forge now says that the
file did not, and writing zero bytes when nothing moved.

**Stories:** S5 (re-run it and trust the result)

## Learning hypothesis

**Disproves safe re-runnability** if a second run churns the file — if the region cannot be regenerated
byte-identically from an unchanged board, then every run produces a diff, the diffs stop being read, and
the block decays into exactly the unnoticed-stale state of issue #31 while looking maintained.

**Confirms**, if it passes, that the command can be run habitually rather than once at adoption — which
is what turns it from a scaffolder into a check.

## IN scope

- Byte-identical regeneration from an unchanged board: the region's ordering, spacing and formatting are
  deterministic functions of the probe result.
- The timestamp question, settled explicitly: **re-stamping alone is not a change** and must not be
  presented as one. Either the stamp is excluded from the change comparison, or it is not refreshed on a
  no-change run — decided at authoring, but decided.
- The change report: a line-by-line account of what the forge now says that the file did not.
- A vanished option id — present in the file, absent from the forge — refreshed inside the markers and
  **reported only** outside them.
- Refusal when `CLAUDE.md` changed between the read and the write.
- KPI-3 measured: `git diff --stat` after a second run on an unchanged board is empty.

## OUT of scope

- Watching, scheduling, or any hook that runs this automatically. A `SessionStart` reporter is a
  plausible follow-on and is **not** this feature — the third driving-port option was considered and not
  chosen ([D3]).
- Repairing drift outside the markers. Reporting is the whole of the power out there (C5).
- Notifying anyone. The report is to whoever ran it.

## Acceptance criteria

1. KPI-3: a second run on an unchanged board writes zero bytes and reports `unchanged`.
2. A timestamp refresh is never reported as a change.
3. A vanished option id is refreshed inside and reported outside, with no edit outside.
4. A file modified between read and write is re-read and the write refused.
5. The report distinguishes *nothing changed* from *nothing could be read* — a probe failure never
   renders as `unchanged`.

## Dependencies

Slices 01–04. There has to be something to re-run, and all three provenance categories must exist before
"what changed" can be answered per category.

## Effort · reference class

≤1 day. Reference class: `phil:resume`'s staleness verdict — a current/stale judgement stated **before**
any content, on the principle that a confidently-followed stale artifact is worse than none.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — deterministic regeneration, a differ, refusals |
| Depends on a new abstraction? | Reuses 01–04 |
| Disproves a pre-commitment? | Yes — that habitual re-running is safe |
| Synthetic data? | No — the real board, run twice |
| Identical to another slice but for scale? | No |
