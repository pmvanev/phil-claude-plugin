# BOOTSTRAP — `/phil:resume`

Part of the `session-handoff` skill. `SKILL.md` governs this path as much as this file does: the
snapshot format, *The last exchanges*, *Writing the snapshot*, the ceiling, the decision outcomes and
the invariants all apply here.

**Compute the verdict before presenting anything.** This ordering is the whole safety property.

1. **No `.session-handoff.md`?** Take the `RECONSTRUCT` path below.
2. **Read the fingerprint** from the delimited header.
3. **Compare against the tree now** — current short HEAD, and current dirty state.
4. **Branch on the comparison**, and state the verdict *first*:

The emitted order is **verdict → board triple (5) → stack (5b) → content (6) → owner (7)**, and the
steps below appear in that order. Both checks come before any content, because a reader who has seen
the briefing has already started believing it.

**`RESUME-CURRENT`** — the commit matches **and** the dirty flag matches. Say the resume point is
current, then present the why and the next action. When both were and are dirty, add one line: the
fingerprint records only *that* the tree was dirty, not what was in it, so uncommitted work may have
moved beneath a current verdict.

**`RESUME-STALE`** — the commit differs, **or** the dirty flag differs in either direction, **or** the
recorded commit is unknown to this tree (rebased, or captured on another branch). Say so **before**
any content, and quantify it:

```
STALE — snapshot at 4a91c02, HEAD is now e17bd55 (6 commits), working tree dirty.
The recorded next action may no longer apply.
```

Measure the distance with `git rev-list --count <recorded>..HEAD`. If that command fails, the
recorded commit is not in this tree's history — report `STALE` and say the recorded commit is
unreachable, rather than reporting no distance at all.

The shape is what matters, not these values: both fingerprints, the distance between them, and the
tree state. Report the distance in whatever unit is available — commit count is best; a bare
"different" is acceptable; silence is not.

State a stale verdict as `STALE` whenever the fingerprint proves it, never as "may be out of date". A
confidently followed stale snapshot is worse than none, because the next session acts on it.

## 5. The board is the other record of what is in flight

The freshness verdict compares the snapshot against the **tree**. It can never compare it against the
**board**, where the rest of the team records the same fact — so a snapshot can be `RESUME-CURRENT` with
every check green while the board says different work is in flight.

Report exactly one of `BOARD-AGREES`, `BOARD-DIVERGES`, `BOARD-UNREADABLE` — **beside the freshness
verdict and before the recorded content** — on `RESUME-CURRENT` and `RESUME-STALE` alike. `RECONSTRUCT`
reports none: with no snapshot there is no recorded next action to compare.

- **`BOARD-AGREES`** — one line naming the card. **Report agreement out loud** — a detector silent on
  agreement is indistinguishable from one that never fires.
- **`BOARD-DIVERGES`** — name **both** sides, label each with its source, and stop.
- **`BOARD-UNREADABLE`** — name the reason and say the next action was not checked. Most repositories
  carrying this skill have no board, so this branch runs most often, and an unreadable board is not an
  agreeing board.

Four rules govern the comparison:

- **The board's in-flight claim is the `In Progress` card where one exists, the top Todo card otherwise.**
- **The match is semantic, not string equality, so bias toward reporting divergence.** Advisory output: a
  false positive costs one line, a false negative is the failure the check exists to kill.
- **Detect; never resolve.** Do not prefer one source, drop the other, or rank them.
- **Read the board; never write it.** No card moved, no Status set, no comment posted.

**`phil:issue-board` owns how a board is read**, including which call under-reports on each forge —
delegate rather than inlining, because an under-reporting read is a *missed divergence*, the one failure
this check cannot notice about itself. The repository's `CLAUDE.md` supplies the constants.

Worked output for all three branches, the #24 incident, and why each rule is drawn where it is:
**`references/board-divergence.md`**.

## 5b. Present the stack, with its marks

**Render the stack as `show` does** (`references/stack.md`) — every frame with what it is, why it was entered, its age, its
`crossed` where non-zero, and `⚠ stale` on any frame at `crossed` 2 or more. Innermost marked.

This step is mandatory: a frame's staleness becomes true at the next pick-up, and `commands/resume.md`
promises the stack. Why `show` alone is not enough: `references/why-these-rules.md` § *Why read-back
renders the stack, and `show` is not enough*.

Where the snapshot has no `## Stack`, say `Stack — none`. Where there is no snapshot at all, this step
does not run: `RECONSTRUCT` has nothing to render.

## 5c. Read-back over `captured: never`

A snapshot created by `push` (see *push* in `references/stack.md`) carries a fingerprint and no payload. Read-back over it:

- **Reports the freshness verdict normally** — `RESUME-CURRENT` or `RESUME-STALE` against `commit:`/`dirty:`.
  The fingerprint is real and was stamped from the tree.
- **Reports no board outcome.** The triple compares the *recorded next action* against the board's
  in-flight claim, and there is no recorded next action — the same reason `RECONSTRUCT` reports none. The
  exemption is stated on the criterion, not on the shape: **no next action, no comparison.** Reporting
  `BOARD-UNREADABLE` would be false where the board reads perfectly, and `BOARD-AGREES` is unproduceable.
- **Says the why and the next action were never recorded** — not that they were empty. `never` is a claim
  about the record; empty would be a claim about the session.
- **Presents the stack**, per 5b. It is the only thing the file holds, and marks nothing, because
  `crossed` is 0 on every frame.

```
RESUME-CURRENT — tree matches the snapshot's fingerprint (7e63578, dirty).
  No state of play has ever been captured against it: the why and the next action were never recorded.
  The board was NOT checked — there is no recorded next action to compare.

  Stack — 1 deep
  1. Deploy script · the blocker's fix cannot be tested until deploys work · open 3h25m   ← you are here
```

## 6. Then, and only then, the content

Show the recorded content clearly marked as historical. Offer the recorded next action as what was
intended at the time, for the reader to judge — not as the thing to do now.

**Read the exchanges into context, print one line counting them, and act on none of them** — nor offer
to, as though the request had been made to this session. A recorded
prompt carries less warrant than the next action — nobody composed it as a plan, and it was addressed to
a session that has ended. A snapshot predating the region prints no line: absent is not zero, and the
line counts what was recorded.

**This step is where the ceiling bites, and it is the only step that gives ground.** Everything above it
is mandatory. Print the next action always; print as many decisions and ruled-out approaches as the
remaining budget holds, then report `REPORT-CLIPPED` with the count withheld against the whole recorded
population and name the snapshot as their home. A reader who needs the discarded alternatives can open
the file; a reader who never learns they exist will re-propose them, which is the defect the why exists
to prevent.

## 7. Naming the owner

After the verdict and the content, name the command that owns the work — on every read-back path,
including `RECONSTRUCT`.

**`ROUTE`** — an owner is determined. State it and stop:

```
owner: /nw-execute  (wave: deliver)  → run it to continue
```

**Name it, and leave it to the human to run.** A read-back reports; it does not start work.

**`ROUTE-LIVE-WINS`** — the recorded `owner:` disagrees with what the feature's current wave label
implies. **The live label wins**, and the disagreement is reported rather than quietly settled:

```
owner: /nw-execute  (wave: deliver)
  recorded as /nw-distill — the wave advanced since this snapshot was written
```

**`ASK-OWNER`** — no `owner:` recorded and no wave label to derive one from. Say the owner is unknown
and ask, under the decision-request standard `SKILL.md` names, then stop before the work. This is the common case on a mixed board, not an edge case: most
cards are not nWave work, and the absence of a label is not permission.

**`RECONSTRUCT`** — no snapshot exists. Derive the position from whatever owns it: the
`nwave-slice-status` skill for a feature's wave, slice, and step state, and git for the branch and
recent commits.

**Derive; never launch.** `/nw-continue` starts the next wave, so reconstruct from the read-only
delegates alone. **Label the briefing reconstructed, not recorded**, including that the *why* is
unavailable, because nothing derives it. The two carry different warranties; `references/why-these-rules.md` says why blurring them invents confidence.
