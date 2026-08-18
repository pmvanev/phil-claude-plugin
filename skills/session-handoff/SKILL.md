---
name: session-handoff
description: Skill bundle for the phil:handoff, phil:resume and phil:stack commands — carries work across the session boundary and tracks where attention is inside one. Use when asked "where was I", "what was I doing before this", to push or record a diversion as it happens, to show the work stack mid-session, or to put a session down and pick it up. Records only what a fresh session cannot derive (the reasoning, the next action, the diversion stack), stamps a tree fingerprint, and projects a write-only copy onto the feature's card. On read-back it states a current/stale verdict, reports whether the board agrees about what is in flight — naming a divergence and never resolving it — then names the owning command without running it. Refuses to record derivable state, and never reads its own projection back.
---

# Session handoff — capture and resume

Two commands over one spine. `/phil:handoff` puts a session down; `/phil:resume` picks the work up.

The value is narrow and specific: **record only what a fresh session cannot work out for itself.**
Everything else is derived at read-back from whatever already owns it. A snapshot that also records
the derivable becomes a second authority over the same fact, and the two drift.

**The claimed-card link was slice 03, tested and deliberately not built.** Do not improvise it, and do
not read its absence as an oversight to correct — the reasoning is in `references/why-these-rules.md`.

## Reference files

Justification lives beside the procedure, not inside it. Read these when **changing** this skill:

- **`references/why-these-rules.md`** — why the guard is content and not identity, why whole-file
  regeneration is safe, why the snapshot is per-worktree, why the projection is write-only, and what
  slice 03 settled.
- **`references/board-divergence.md`** — the #24 check's reasoning, its worked output for all three
  branches, and why each of its four rules is drawn where it is.

## What is worth recording

| Category | Recordable? | Why |
|---|---|---|
| **The why** — decisions made, approaches ruled out, why work stopped | **Yes** | It was never an artifact. No reconstruction can recover it. |
| **The next action** — what the session was about to do | **Yes** | Partly inferable, and a wrong inference is costlier than none. |
| The where — file, step, branch, commit, wave | **No** | Already owned by the artifacts. Derive it at read-back via the read-only `nwave-slice-status` skill and git. |
| **The entry point** — which command owns the work | **Yes** | The card describes work, not method. Nothing else records it. |
| **The work stack** — the diversion chain, innermost first | **Yes** | Where attention actually is. No artifact holds it, and unlike the why it has a *shape* that matters: what to return to, and in what order. |
| The claimed card and its basis | **No — tested, not built** | The board's top Todo answers *what is next*; the basis is what **the why** already records. |

## The snapshot

One file, `.session-handoff.md`, at the repository root — resolve it as
`$(git rev-parse --show-toplevel)/.session-handoff.md`, never relative to the current directory, so
both paths agree when a command runs from a subdirectory. Git-ignored — it is runtime state, not
history. Never commit it; never write it anywhere under `docs/`.

```markdown
<!-- session-handoff:v1 -->
captured: 2026-08-12T17:30Z
commit: 083c953
dirty: no
owner: /nw-execute
<!-- /session-handoff:v1 -->

## Why

- Rejected the hook for v1 — it cannot see the why, and the why is the payload.
- The card-side half can ship before the session-side half.

## Next

Verify the wave-to-command table against a real run.

## Stack

1. Wave-to-command table · the task in hand · open since 2026-08-12T14:05Z · crossed 2
2. └ Fixture 07 · it contradicted the table, so it had to be settled first · open since 2026-08-12T16:40Z · crossed 0
3.   └ The fixture runner · it needed a flag it did not have · open since 2026-08-12T17:05Z · crossed 0
```

**The stack is innermost-last, numbered, and each frame carries what it is, why it was pushed, when, and
how many wind-downs it has survived**, in that order, separated by ` · `. Read bottom-up to find where attention is; read top-down to find what
it was diverted from. A frame is popped by deleting its line, so the file is the stack rather than a log
of stack operations.

**Every frame stamps the full `YYYY-MM-DDTHH:MMZ`, including the deeper ones.** The abbreviated form this
format shipped with — a bare `16:40Z` on frames 2 and 3 — was a readability nicety while the stack was
only ever rendered. `show` computes an age from it, so it is machine input now, and a frame open across a
handoff has very likely crossed midnight.

**`crossed` counts the wind-downs a frame has survived.** A frame is written `crossed 0` by `push`, and
`CAPTURE` increments it for every frame already in the file. It is the only piece of frame state anything
but `push` writes, and it exists because the staleness rule below has no other discriminator.

**Omit the section entirely when nothing was diverted.** An empty `## Stack` heading reads as a claim that
the work was straightforward, which is a different thing from no claim at all.

**A frame with `crossed` of 2 or more is marked `⚠ stale`.** A push that was never popped is stale, and a
stale frame is worse than no frame because the reader trusts it — the same shape as a stale snapshot, one
level down.

**Two, not one**, and `crossed` is stored rather than derived, for reasons that are not obvious —
`references/why-these-rules.md` § *Why the stale threshold is two*.

**Nothing is marked while every frame reads `crossed 0`**, which is the whole of a session that has not
wound down yet, including the push-created snapshot.

No age threshold is defined, and inventing one would be guessing — `crossed` counts wind-downs, never
elapsed time. Every frame renders its age, so a frame that is merely old stays visible for a human to
judge without the tool claiming anything about it.

**The mark is computed at render time and never written to the file.** `⚠ stale` appears in `show` and in
`pop`'s report; the snapshot stores `crossed` and nothing else. A stored mark would be a second piece of
derived state that `push`'s byte-for-byte reproduction would then carry forward after it went wrong.

**This rule's source is here**, beside the recorder. `skills/nwave-issue-board/SKILL.md` states it again
for the projected copy and cites this file; if the two disagree, this one wins.

The delimited header is machine-readable with `grep`/`sed`; the body is prose for a human. Read the
fingerprint from the header, never by parsing the prose.

## Writing the snapshot

Every write to `.session-handoff.md` — from CAPTURE, from `push`, from `pop` — obeys one rule:

**Regenerate the whole file. Never edit part of it, and never merge into a snapshot that changed
beneath this session.**

```
read    h1 = git hash-object <root>/.session-handoff.md    # absent file → no h1, see below
modify  add or drop what this path is changing, in memory, over the whole parsed file
verify  h2 = git hash-object <root>/.session-handoff.md    # re-read, immediately before writing
        h2 ≠ h1  →  REFUSE. Report both hashes. Write nothing.
write   the whole file
```

`git hash-object`, not `sha256sum` or `shasum`: git is already required to resolve the path, and the
coreutils spelling differs between Linux and macOS. Never pass `-w` — that writes the object into the
database, which is why the verb is not on `check-readonly-commands.py`'s read-only allowlist.

Where no file exists at `read`, there is no `h1`; `verify` instead asserts the file is **still** absent.
A file that appeared in between is another writer's, and the same refusal applies.

**The delimited header belongs to CAPTURE alone.** `push` and `pop` reproduce `captured:`, `commit:`,
`dirty:` and `owner:` **byte-for-byte** and never re-derive them. This is the single most destructive
mistake available on this path, and it is the natural one: a whole-file regeneration, run by something
holding a live tree and a `git rev-parse` grant, will re-stamp a fingerprint unless told not to. Re-stamp
it and `commit:` always matches `HEAD`, so `RESUME-STALE` never fires again — the worst outcome this skill
can produce, arrived at by a routine mid-session note.

`captured:` means *when the payload was captured*, not *when the file was last touched*. A push is not a
capture.

**A failed compare-and-swap refuses and reports. It never retries and never loops.** Retrying resolves a
competing write by overwriting it, which is arbitration; competing claims are **detected, not resolved**
here. Report `WRITE-REFUSED` with both hashes and stop.

The file is **per-worktree**, not per-repo — `git rev-parse --show-toplevel` returns a linked worktree's
own root.

Why regeneration is safe, why the guard is content rather than identity, and where `core.autocrlf` lands:
`references/why-these-rules.md`.

## CAPTURE — `/phil:handoff`

1. **Decide whether anything happened.** The payload is the why and the next action. If neither can
   be stated — no decision reached, no next action formed — take the `NO-OP` path below, **however
   many files changed**. File churn alone is derivable from git and is not a reason to write a
   snapshot.

   `$ARGUMENTS`, when present, is the session's own account of what it was doing. Treat it as raw
   material for the why and the next action, never as the record itself — it is subject to every rule
   below, including the refusal of derivable state it may contain.
2. **Collect the why.** State the decisions reached and, critically, the approaches **ruled out and
   why**. A decision without its discarded alternatives invites the next session to re-propose them.
3. **Collect the next action** — one sentence, concrete enough to start from.
4. **Record the owning command**, when the work has one. Derive it from the feature issue's wave
   label using the table in `skills/nwave-issue-board/SKILL.md` — that skill owns the wave label and
   owns the mapping. Do not restate the table here; a second copy is a second authority. Omit
   `owner:` entirely when no wave label applies. Most work has no owner, and that is not a defect.
5. **Carry the work stack forward, and increment it.** The frames already in `.session-handoff.md` are
   **authoritative**. Reproduce each one's what, why and `open since` **byte-for-byte**, and add 1 to its
   `crossed`. Do not re-derive `open since` from the session's account or from the clock: re-stamping it
   makes every frame postdate its own capture, and `⚠ stale` becomes unreachable for ever after — the
   header rule's failure, one level down.

   Append a frame only for a diversion the session took and did **not** close, that is not already in the
   file; new frames are written `crossed 0`. A diversion closed before the session ended leaves no frame —
   the stack records where attention *is*, not where it has been. **Collected here, with the other payload,
   because step 8 writes the file**: a stack gathered after the write is a stack the snapshot does not
   contain.
6. **Refuse the derivable.** If wave, slice, step, branch, or file position comes up, leave it out.
   Say plainly that it is left out because it is derived at read-back. This is not an optimisation;
   recording it is the defect.
7. **Stamp the header.** `captured:` is the current time in UTC at minute precision
   (`2026-08-12T17:30Z`); `commit` is `git rev-parse --short HEAD`; `git status --porcelain`
   non-empty means `dirty: yes`.
8. **Write `.session-handoff.md`** whole, under the compare-and-swap in *Writing the snapshot* above.
   Never merge into a snapshot that changed beneath this session.
9. **Refresh the projection on the feature's card, if the work has one.** Local file first, always: the
   snapshot is the authority and a failed forge call must never cost it. Publishing is
   `phil:nwave-issue-board`'s — hand it the why, the next action and the stack with their capture
   timestamp, and let it own the block. **Never read the card back.** A forge failure leaves the snapshot
   intact and is reported as an un-refreshed projection, not as a failed capture.
10. **Report** `CAPTURE`, and echo what was recorded so a mistake is visible immediately. Say whether the
   projection was refreshed, and where it was not.

**Where no snapshot was ever projected, the card's stack section must render `unknown` — never empty.**
An empty stack asserts *no diversions*, which is a claim; `unknown` asserts *nobody wrote it down*.

Why the projection exists at all, and why it is write-only: `references/why-these-rules.md`.

### NO-OP

A session that advanced nothing writes **no** file. Report `NO-OP` and say that nothing was
recorded and why.

Do not write an empty or placeholder snapshot. A resume point that says "no decisions, next action
unknown" is worse than none: the next session finds one, reads nothing in it, and learns to distrust
resume points generally.

Saying nothing was recorded is part of the outcome, not politeness — silence is indistinguishable
from the command having failed.

## STACK — `/phil:stack`

The stack is the only payload with **operations**. The why and the next action are stated once at
wind-down; a diversion happens mid-session, and the reason for it is only in the human's head while it
is happening. These three verbs exist so that reason can be caught then rather than reconstructed later.

All three read the whole snapshot. `push` and `pop` write it back under *Writing the snapshot*, header
reproduced byte-for-byte; `show` writes nothing.

### push — `/phil:stack push "<what>" "<why>"`

1. **Require the why.** A frame naming only what was entered records the half that is derivable from the
   files being touched and drops the half that is not. Where `<why>` is missing, ask for it; do not infer
   it from the diff and do not write the frame without it.
2. **Read the whole snapshot** and take `h1`.
3. **Append the frame** innermost-last, numbered, indented one step deeper than its parent, and stamped
   with the **full** current UTC minute plus a zero counter:

   ```
   <N>. <indent><└ if N>1><what> · <why> · open since <YYYY-MM-DDTHH:MM>Z · crossed 0
   ```

   Frame 1 carries no `└` and no indent. **Every frame carries the full date**, deeper ones included —
   `show` subtracts from it and the staleness rule reads it, so a bare `HH:MMZ` is undecidable.
4. **Write the whole file** under the compare-and-swap.
5. **Report** `PUSHED`, echoing the frame and the new depth, so a mistyped reason is visible at once.

**Where no snapshot exists, create one carrying the stack alone.** A diversion is payload, so this is
not the `NO-OP` case — but the why and the next action are **absent**, never invented.

Such a file still needs a header, and `push` is not a capture, so it cannot stamp one as CAPTURE does.
Write `captured: never` and stamp `commit:` and `dirty:` from the tree at creation — the one sanctioned
exception to the header rule, because there is no prior header to reproduce. `captured: never` is the
load-bearing token: a fingerprint exists, and no payload was ever captured against it.

**What BOOTSTRAP does with it** is stated in full at *Read-back over `captured: never`* below, because it
is not obvious: the freshness verdict works, the board triple cannot, and the why is *never recorded*
rather than empty. A read-back over
such a snapshot presents the stack and says the why was never captured.

**Never refresh the projection from `push`.** The card is refreshed at boundaries, by `/phil:handoff`.
A forge write per push would put the board on the critical path of a mid-session note and publish
in-flight scratch a frame at a time.

### show — `/phil:stack`, bare

1. **Read the snapshot.** Take no hash; nothing is written.
2. **Render the trace**: every frame with what it is, why it was pushed, and how long it has been open.
   Mark the innermost — that is where attention is — and mark `⚠ stale` any frame whose `crossed` is 2
   or more, per *The snapshot* above. Render `crossed` where it is non-zero, so the mark shows its
   working rather than asserting a judgement.
3. **Report** `SHOWN`, or one of the two empties below.

**`unknown` and `none` are different answers and must not be collapsed.** No snapshot at all → `unknown`:
nobody wrote anything down. A snapshot with no `## Stack` → `none`: a session recorded its state and had
no diversions to record. `unknown` is a claim about the record; `none` is a claim about the work.

Read bottom-up for where attention is; read top-down for what it was diverted from.

### pop — `/phil:stack pop`

1. **Read the whole snapshot** and take `h1`.
2. **Delete the innermost frame only** — the last line of `## Stack`. A frame is popped by deleting its
   line, which is what keeps the file a stack rather than a log of stack operations, and what keeps it
   from growing without bound. Popping anything else is editing the stack rather than navigating it: do
   that by hand, which the prose format allows on purpose.
3. **Remove the `## Stack` section entirely** when the last frame goes. An empty heading asserts the work
   was straightforward, which is a different claim from no claim.
4. **Write the whole file** under the compare-and-swap, header reproduced byte-for-byte.
5. **Report** `POPPED`, naming the frame now in hand and the new depth. **Where the popped frame was
   marked `⚠ stale`, say so** — a frame that outlived a boundary and is closed silently takes with it the
   only signal that the record had drifted from the work.

**Popping nothing is not an error, and the two nothings are different**, exactly as they are for `show`:

- **No snapshot at all** → `STACK-UNKNOWN`. Nobody wrote anything down; this says nothing about whether
  there were diversions.
- **A snapshot with no `## Stack`** → `STACK-EMPTY`. A session recorded its state and had none to record.

Either way **write nothing** — do not rewrite the file to prove it was read, and do not take a hash to
find out. Collapsing the two into "the stack is empty" asserts a fact about the work when the record is
what is absent.

**Popping the last frame off a push-created snapshot leaves a file with a header and nothing else.** That
is the placeholder this skill refuses elsewhere, so **delete the snapshot** in that one case: no `## Why`,
no `## Next`, no `## Stack`, and `captured: never` — nothing was ever captured, and the only thing the
file held has just been popped. Report `POPPED` and say the snapshot was removed. Where a `## Why` or a
`## Next` exists, the file stays: a capture happened, and its payload is not the stack's to discard.

## BOOTSTRAP — `/phil:resume`

**Compute the verdict before presenting anything.** This ordering is the whole safety property.

1. **No `.session-handoff.md`?** Take the `RECONSTRUCT` path below.
2. **Read the fingerprint** from the delimited header.
3. **Compare against the tree now** — current short HEAD, and current dirty state.
4. **Branch on the comparison**, and state the verdict *first*:

The emitted order is **verdict → board triple (step 5) → content (step 6) → owner (step 7)**, and the
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

A confidently-followed stale snapshot is the worst outcome this skill can produce. It is worse than
having no snapshot, because the next session acts on it. Never soften the verdict to "may be out of
date" when the fingerprint proves it is.

### 5. The board is the other record of what is in flight

The freshness verdict compares the snapshot against the **tree**. It can never compare it against the
**board**, where the rest of the team records the same fact — so a snapshot can be `RESUME-CURRENT` with
every check green while the board says different work is in flight.

Report exactly one of `BOARD-AGREES`, `BOARD-DIVERGES`, `BOARD-UNREADABLE` — **beside the freshness
verdict and before the recorded content** — on `RESUME-CURRENT` and `RESUME-STALE` alike. `RECONSTRUCT`
reports none: with no snapshot there is no recorded next action to compare.

- **`BOARD-AGREES`** — one line naming the card. **Report agreement out loud**; a detector silent on the
  agreeing branch is indistinguishable from one that never fires.
- **`BOARD-DIVERGES`** — name **both** sides, label each with its source, and stop.
- **`BOARD-UNREADABLE`** — name the reason and say plainly that the next action was not checked. Most
  repositories carrying this skill have no board, so this branch runs most often. An unreadable board is
  not an agreeing board.

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

### 5b. Present the stack, with its marks

**Render the stack as `show` does** — every frame with what it is, why it was entered, its age, its
`crossed` where non-zero, and `⚠ stale` on any frame at `crossed` 2 or more. Innermost marked.

This is not optional and it is not `show`'s job alone. A frame's staleness becomes *true* at the next
pick-up, so read-back is the moment it matters; leaving it to `show` means the mark is seen only by
someone who already remembered the frame. `commands/resume.md` promises the stack in as many words —
*"present what was decided, the diversion stack you were inside, and what to do next"* — and this step is
where that promise is kept.

Where the snapshot has no `## Stack`, say `Stack — none`. Where there is no snapshot at all, this step
does not run: `RECONSTRUCT` has nothing to render.

### 5c. Read-back over `captured: never`

A snapshot created by `push` (see *push* above) carries a fingerprint and no payload. Read-back over it:

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

### 6. Then, and only then, the content

Show the recorded content clearly marked as historical. Do **not** present the recorded next action as
the thing to do now; offer it as what was intended at the time, for the reader to judge.

### 7. Naming the owner

After the verdict and the content, name the command that owns the work — on every read-back path,
including `RECONSTRUCT`.

**`ROUTE`** — an owner is determined. State it and stop:

```
owner: /nw-execute  (wave: deliver)  → run it to continue
```

**Name it; never run it.** `/phil:resume` has no `Write`, no `Edit`, and read-only `Bash`, and
running the owner would route around all three — `/nw-execute` writes code. This mirrors
`nwave-slice-status`, which prints the resume command as text and never runs it. A read-back reports;
it does not start work.

**`ROUTE-LIVE-WINS`** — the recorded `owner:` disagrees with what the feature's current wave label
implies. **The live label wins**, and the disagreement is reported rather than quietly settled:

```
owner: /nw-execute  (wave: deliver)
  recorded as /nw-distill — the wave advanced since this snapshot was written
```

Silently preferring the live value hides that the snapshot has drifted, which is the one signal that
would tell the reader their capture habit is falling behind.

**`ASK-OWNER`** — no `owner:` recorded and no wave label to derive one from. Say the owner is unknown
and ask. **Do not begin the work.** This is the common case on a mixed board, not an edge case: most
cards are not nWave work, and the absence of a label is not permission.

**`RECONSTRUCT`** — no snapshot exists. Derive the position from whatever owns it: the
`nwave-slice-status` skill for a feature's wave, slice, and step state, and git for the branch and
recent commits.

**Never invoke `/nw-continue` here.** It computes much the same position and then *launches the next
wave* — `skills/nwave-slice-status/SKILL.md` exists because of that side effect. Read-back starts
nothing. Present that, and **label it as reconstructed rather than recorded** — including
that the *why* is unavailable, because nothing derives it.

A recorded briefing carries reasoning that was witnessed. A reconstructed one carries position
inferred from files. They have different warranties; blurring them invents confidence.

## Deriving, not duplicating

At read-back, fetch the derivable from its owner rather than the snapshot:

| Wanted | Ask | Read-only? |
|---|---|---|
| Where an nWave feature stands — wave, slice, step | the `nwave-slice-status` skill | yes |
| Branch, HEAD, working-tree state | `git` | yes |

Both delegates are read-only, and **enforced** so: the `nwave-slice-status` skill writes nothing, and
`/phil:resume`'s `git` grants are scoped to read-only subcommands.

Delegate; do not re-derive. These own their answers and have their own correctness gates.

**The board is not in this table**, and the distinction is worth keeping sharp. These two rows answer
*what to look up instead of recording* — the snapshot was always at risk of duplicating them. The board
answers something else entirely: *what to cross-check the snapshot against*. Nothing here was ever
tempted to record it. Step 5 owns that read; `commands/resume.md` owns why its grant makes the command
declare `mutates: true` while writing nothing.

Note the asymmetry, which is deliberate: at **capture** this state must be refused, and at
**read-back** it must be actively fetched. The rule is not "never touch position" — it is *never at
capture, always at read-back*.

## Decision outcomes

Report the outcome by name, every run — one per phase:

`CAPTURE` · `NO-OP` · `REFUSE-DERIVABLE` · `PROJECTED` · `PROJECTION-UNREFRESHED` · `RESUME-CURRENT` ·
`RESUME-STALE` · `RECONSTRUCT` · `ROUTE` · `ROUTE-LIVE-WINS` · `ASK-OWNER` · `BOARD-AGREES` ·
`BOARD-DIVERGES` · `BOARD-UNREADABLE` · `PUSHED` · `POPPED` · `SHOWN` · `STACK-EMPTY` ·
`STACK-UNKNOWN` · `WRITE-REFUSED`

A capture run reports exactly one of `CAPTURE` or `NO-OP`. `REFUSE-DERIVABLE` is **additional**:
report it alongside `CAPTURE` whenever derivable state was offered and left out, naming what was left
out.

`PROJECTED` and `PROJECTION-UNREFRESHED` are **also additional**: one of them, only alongside `CAPTURE`,
only when the work has a card. **A `CAPTURE` with neither silently skipped the card.** A `NO-OP` never
projects. A read-back reports exactly one of `RESUME-CURRENT`, `RESUME-STALE`, `RECONSTRUCT`, **and**
exactly one of `ROUTE`, `ROUTE-LIVE-WINS`, `ASK-OWNER` — freshness and owner are independent facts.

**A third independent triple** joins them on the paths that have a recorded next action to check:
`RESUME-CURRENT` and `RESUME-STALE` each report exactly one of `BOARD-AGREES`, `BOARD-DIVERGES`, or
`BOARD-UNREADABLE` — **unless there is no recorded next action**, in which case none is reported.
`RECONSTRUCT` is one such case (no snapshot). A `captured: never` snapshot is the other: it has a
snapshot and a working fingerprint, and still nothing to compare. The exemption is the criterion, not
the shape.

**These are independent of the freshness verdict, and coercing one into the other is a gate failure.**
A board divergence is not staleness: the tree may be untouched while the work has moved on, which is
exactly the case #24 was filed for. Report both, and let them disagree.

**A stack run reports exactly one** of `PUSHED`, `POPPED`, `SHOWN`, `STACK-EMPTY`, `STACK-UNKNOWN` or
`WRITE-REFUSED`, and reports none of the capture or read-back outcomes — the three paths do not
interleave. `STACK-EMPTY` and `STACK-UNKNOWN` are separate for the reason the projection keeps `none`
and `unknown` separate: one is a claim about the work, the other about the record. `WRITE-REFUSED` is
terminal on its run; nothing is written and nothing is retried.

## What this skill must never do

- Write the snapshot anywhere but the repo root, or commit it.
- Present a stale snapshot as current, or bury the verdict beneath the content.
- **Refresh the projection before the snapshot is written.** Local first, always — a forge call that
  succeeds while the local write fails leaves the authority behind its own copy.
- **Read the projection block back, at capture or at read-back.** The projection is write-only; that is
  what keeps it from being a second authority.

  **The boundary is the block, not the card.** Read-back reads the board's *Status, position and card
  title* — that is the divergence check, and those facts are the board's own, never a copy of anything
  this skill wrote. It must never read back the `Why` / `Next` / `Stack` it projected, because those
  **are** a copy, and a snapshot reconciled against its own projection has become two authorities.
  Stated on 2026-08-17: until then the rule read "never the card", which the divergence check made
  false while the real invariant went unwritten.
- **Render an absent stack as empty.** Where nothing was projected, the card says `unknown`. Empty
  asserts there were no diversions.
- **Publish the block itself.** `phil:nwave-issue-board` owns the block's format, its markers and its
  timestamp; hand it the content.
- Record wave, slice, step, branch, or file position.
- Write a snapshot for a session that advanced nothing.
- Invent a next action that was not stated.
- **Run** the owning command. Naming it is the whole of routing here; `/phil:resume` starts nothing.
- **Resolve a board divergence.** Detect it, name both sides, stop. Preferring one source discards the
  other's work while reporting success.
- **Write to the board during read-back.** No card moved, no Status set, no comment. The projection at
  CAPTURE step 9 is the **only** sanctioned board write in this skill; read-back has none.
- **Report `BOARD-AGREES` for a board that could not be read**, or report nothing at all. Unreadable is
  a claim about the record; agreement is a claim about the work.
- Record a claimed card or its basis as a field. Tested and not built; the why already carries the basis.
- Restate the wave → command table. `skills/nwave-issue-board/SKILL.md` owns it; derive from there.
- **Merge into a snapshot that changed beneath this session**, on any path. Regenerate whole, or refuse.
- **Retry a refused write.** Retrying resolves a competing write by overwriting it, which is arbitration.
- **Re-derive the header on a `push`.** `captured:`, `commit:`, `dirty:` and `owner:` are CAPTURE's and are
  reproduced byte-for-byte. Re-stamping `commit:` makes `RESUME-STALE` unreachable for ever after.
- **Push a frame with no reason.** The reason is the payload; the what is half-derivable from the diff.
- **Push from a hook.** No hook can see why a human left a task — the ground on which the `Stop` hook was
  deferred.
- **Close a frame the human did not close.** No expiry, no auto-pop, no timeout. A frame the tool closed
  is a frame whose reason nobody read; marking it stale is the honest limit.
- **Pop a frame other than the innermost.**
- **Re-derive a frame's `open since`**, on any path, including `CAPTURE`. The file is authoritative for
  frames already in it. Re-stamping makes every frame postdate its capture and `⚠ stale` unreachable.
- **Write `⚠ stale` into the snapshot.** The mark is computed at render time; the file stores `crossed`.
- **Mark on age.** `crossed` counts wind-downs. A frame open three days inside one session is `crossed 0`
  and is not stale — it is where attention still is.
- **Write to the forge from `/phil:stack`.** The card is refreshed at boundaries, by `/phil:handoff`.

## Acceptance

`acceptance.feature` is the scenario SSOT. **`self-test/README.md` is the fixture register** — it holds
the roster, the must-pass set, what each fixture pins, and the driving rules. Read it before driving the
suite; do not drive from this section alone, and do not maintain a second roster here.

That split is deliberate and was earned twice — `references/why-these-rules.md` records how.

One rule is worth repeating because getting it wrong retires working fixtures: **the fixtures that
predate the board triple supply no `board_state`, so a read-back over them reports `BOARD-UNREADABLE`,
and that is a pass.** The register says which ones and why.

The suite is **model-driven** for the decisions — judging whether a read-back reached the right
outcome is not automatable here. It is **not uncovered**: `tests/test_session_handoff_fixtures.py`
structurally guards every fixture, asserting each is registered and names only outcomes this file
defines. It does not drive them. (`tests/test_self_test_fixtures.py` is a different suite, covering
`refactor-tests`/`refactor`, not these.) Drive each one by giving this skill
the situation in its `manifest.json` and comparing the decision reached against its `expected.md`. Do
that whenever this file, any of the three command loaders, `skills/nwave-issue-board/SKILL.md` or
`skills/issue-board/SKILL.md` changes. Every failure mode here is silent — a snapshot that records too
much looks more complete, a stale one presented as current looks like a smooth resume, and a divergence
check that never fires looks like a board that always agrees.
