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

## Outcome — authored 2026-08-17

| AC | Verdict | Evidence |
|---|---|---|
| 1 | **PASS — KPI-3 met on the real board** | A second run, re-probed and re-rendered with a fresh stamp, wrote **zero bytes**; `md5sum` identical either side, `status: unchanged`, `stamp_only: true`. |
| 2 | **PASS, and DECIDED** | See below — the brief required a decision, not a mechanism. |
| 3 | **PASS** | `refresh_region` replaces only the probed region; the declared region and all prose are outside what it touches, tested. Fixture 12 pins the report-outside/refresh-inside split. |
| 4 | **PASS** | `--expect-sha` re-checked immediately before the write; a mismatch refuses with the file untouched. |
| 5 | **PASS** | `refresh_region` refuses outright when handed no rendered region, rather than reporting `unchanged`. A probe that could not be read is not a board that did not move. |

### The timestamp question — DECIDED, not left open

**The stamp is not refreshed on a no-change run.**

The brief offered two options and required one be chosen. They are not equivalent: excluding the stamp
from the *comparison* while still *writing* it would satisfy AC2 and **fail KPI-3**, because writing a
stamp writes bytes. So the two requirements are really one, and only this answer satisfies both.

### The renderer had to move into the repo, and that was a gap slices 01–02 left

**Determinism is unreachable while a model does the rendering.** Ordering, spacing and wording drift
run to run, so every run produces a diff, the diffs stop being read, and the block decays into #31's
unnoticed-stale state *while looking maintained*.

Slices 01 and 02 shipped no renderer — the region was assembled by a model reading the probe JSON, and
AC1 held only by after-the-fact value matching. `scripts/render-block.py` now makes the region a pure
function of `(probe, stamp)`, which is what KPI-3 stands on. **A gap that only the fifth slice's
requirement made visible**, and an argument for ordering slices by learning rather than by convenience.

### Learning hypothesis — CONFIRMED

Habitual re-running is safe, so the command is a **check** rather than a scaffolder. That is the
difference between something run once at adoption and something run whenever the board is touched — and
issue #31 exists precisely because nothing currently notices a stale generated block.

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
