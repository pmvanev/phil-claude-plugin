---
name: session-handoff
description: Skill bundle for the phil:handoff and phil:resume commands — carries work across the session boundary. Records only what a fresh session cannot derive (the reasoning, the next action, the diversion stack), stamps a tree fingerprint, and projects a write-only copy onto the feature's card. On read-back it states a current/stale verdict against the tree, reports whether the board agrees about what is in flight — naming a divergence and never resolving it — and then names the owning command without running it. Refuses to record derivable state, and never reads its own projection back.
---

# Session handoff — capture and resume

Two commands over one spine. `/phil:handoff` puts a session down; `/phil:resume` picks the work up.

The value is narrow and specific: **record only what a fresh session cannot work out for itself.**
Everything else is derived at read-back from whatever already owns it. A snapshot that also records
the derivable becomes a second authority over the same fact, and the two drift.

Slices 01 and 02. **The claimed-card link was slice 03, and was tested and deliberately not built** —
its hypothesis (*the board already carries enough*) held. Do not improvise it, and do not read its
absence as an oversight to correct: the board's top Todo card answers *what is next*, and the basis for
a claim is what the `Why` section is already for. Recording it as a field would duplicate prose that
carries it, which is the drift this skill exists to prevent. The finding is in
[`slice-03-claimed-card-link.md`](https://github.com/pmvanev/phil-claude-plugin/blob/main/docs/feature/session-handoff/slices/slice-03-claimed-card-link.md).

**One residual survived that investigation and shipped separately: the board divergence check below**
(issue #24, 2026-08-17). It is the narrow thing slice 03's verdict left standing — not *record which
card was claimed*, but *notice when the two records of what is in flight disagree*. It records nothing
and resolves nothing, so it does not reopen slice 03.

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

1. Wave-to-command table — the task in hand · open since 2026-08-12T14:05Z
2. └ Fixture 07 contradicted it, so it had to be settled first · open since 16:40Z
3.   └ The fixture runner needed a flag it did not have · open since 17:05Z
```

**The stack is innermost-last, numbered, and each frame carries what it is, why it was pushed, and when.**
Read bottom-up to find where attention is; read top-down to find what it was diverted from. A frame is
popped by deleting its line, so the file is the stack rather than a log of stack operations.

**Omit the section entirely when nothing was diverted.** An empty `## Stack` heading reads as a claim that
the work was straightforward, which is a different thing from no claim at all.

The delimited header is machine-readable with `grep`/`sed`; the body is prose for a human. Read the
fingerprint from the header, never by parsing the prose.

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
3b. **Record the owning command**, when the work has one. Derive it from the feature issue's wave
   label using the table in `skills/nwave-issue-board/SKILL.md` — that skill owns the wave label and
   owns the mapping. Do not restate the table here; a second copy is a second authority. Omit
   `owner:` entirely when no wave label applies. Most work has no owner, and that is not a defect.
3c. **Collect the work stack**, if the session was diverted. One frame per diversion, innermost last, each
   with what it is, why it was pushed, and when. A diversion that was closed before the session ended
   leaves no frame — the stack records where attention *is*, not where it has been. **Collected here, with
   the other payload, because step 6 writes the file**: a stack gathered after the write is a stack the
   snapshot does not contain.
4. **Refuse the derivable.** If wave, slice, step, branch, or file position comes up, leave it out.
   Say plainly that it is left out because it is derived at read-back. This is not an optimisation;
   recording it is the defect.
5. **Stamp the header.** `captured:` is the current time in UTC at minute precision
   (`2026-08-12T17:30Z`); `commit` is `git rev-parse --short HEAD`; `git status --porcelain`
   non-empty means `dirty: yes`.
6. **Write `.session-handoff.md`**, overwriting any previous snapshot outright — never merging into
   it. There is one snapshot per repository root, so a competing snapshot would need a second worktree
   on the same repo; that case was examined with slice 03 and left unhandled deliberately.
7. **Refresh the projection on the feature's card, if the work has one.** Local file first, always: the
   snapshot is the authority and a failed forge call must never cost it. Publishing is
   `phil:nwave-issue-board`'s — hand it the why, the next action and the stack with their capture
   timestamp, and let it own the block. **Never read the card back.** A forge failure leaves the snapshot
   intact and is reported as an un-refreshed projection, not as a failed capture.
8. **Report** `CAPTURE`, and echo what was recorded so a mistake is visible immediately. Say whether the
   projection was refreshed, and where it was not.

**The projection exists because a teammate cannot read this file.** `.session-handoff.md` is git-ignored
and machine-local by ADR-013, whose consequences state outright that *"nothing is shared with a
teammate"* — accepted for v1, with the partitioned local-plus-board option named as the documented path
if that need appeared. It appeared. The partition is exactly as that ADR wrote it: **this file stays the
single authority; the card carries a generated, timestamped, write-only projection of it.** Nothing is
read back, so no second authority exists to drift.

**The cost, stated so nobody discovers it as a bug:** a teammate sees only what the last `/phil:handoff`
projected. Where no snapshot was ever projected, the card's stack section must render `unknown` — never
empty. An empty stack asserts *no diversions*, which is a claim; `unknown` asserts *nobody wrote it down*,
which is the truth.

### NO-OP

A session that advanced nothing writes **no** file. Report `NO-OP` and say that nothing was
recorded and why.

Do not write an empty or placeholder snapshot. A resume point that says "no decisions, next action
unknown" is worse than none: the next session finds one, reads nothing in it, and learns to distrust
resume points generally.

Saying nothing was recorded is part of the outcome, not politeness — silence is indistinguishable
from the command having failed.

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

**The freshness verdict compares the snapshot against the tree. It can never compare it against the
board, and the board is where the rest of the team records the same fact.** So a snapshot can be
`RESUME-CURRENT` — same commit, same clean tree, every check green — while the board says something
different is in flight, and nothing says so.

Observed 2026-08-13 and carded as #24: the snapshot's `Next` named a dogfood run; the board's top Todo
was #15, different work entirely. It was harmless, because the dogfood had happened in an intervening
session. **A human noticed it. Nothing else could have.**

The two sources fail in opposite directions and a session cannot tell which it is holding:

- **Snapshot ahead of the board** — work was claimed and the card never moved. Following the board
  restarts work already under way.
- **Board ahead of the snapshot** — the card advanced in another session. Following the snapshot
  redoes spent work.

Report one of three outcomes, **beside the freshness verdict and before the recorded content** — on
`RESUME-CURRENT` and `RESUME-STALE` alike. `RECONSTRUCT` reports none of them: with no snapshot there
is no recorded next action, so there is nothing to compare. Reporting the board's in-flight card there
as *reconstructed position* is defensible and is deliberately **out of scope** for #24, not argued
against.

**`BOARD-AGREES`** — the recorded next action and the board's in-flight claim name the same work. One
line, naming the card:

```
BOARD-AGREES — snapshot Next and the board's in-flight card (#24, In Progress) name the same work.
```

**Report agreement out loud.** A detector silent on the agreeing branch is indistinguishable from one
that is broken, mis-wired, or reading an empty board — the *check nobody runs reports compliance by
staying quiet* defect this repository keeps rediscovering.

**`BOARD-DIVERGES`** — they name different work. Name **both**, label each with its source, and stop:

```
BOARD-DIVERGES — the two records of what is in flight disagree.
  snapshot Next (captured 2026-08-13T21:10Z):
    dogfood /phil:groom-issues against this repo's own board
  board, top Todo (no card In Progress):
    #15 groom-issues slice 03 — set-level operations, all ask-first
Neither is authoritative over the other. Resolve before proceeding.
```

**`BOARD-UNREADABLE`** — there is no board, or it cannot be reached. Name the reason, and say plainly
what was not checked:

```
BOARD-UNREADABLE — no board constants in CLAUDE.md and no `project` scope on the token.
The snapshot's Next was NOT checked against a board.
```

Most repositories carrying this skill have no board, so **this is the branch that runs most often**. An
unreadable board is not an agreeing board, for the same reason an absent stack renders `unknown` rather
than empty: one is a claim about the record, the other a claim about the work.

Four rules govern the comparison:

- **The board's in-flight claim is the `In Progress` card where one exists, and the top Todo card
  otherwise.** Comparing against the top Todo alone reports a session that correctly claimed its card
  as diverging from whatever sits above it. Where `In Progress` goes unused the branch never fires.
  The reasoning is in `self-test/14-board-agrees-with-snapshot/expected.md`.
- **The match is semantic, not string equality, so bias toward reporting divergence.** The outcome is
  advisory and resolves nothing: a false positive costs the reader one line, a false negative is the
  silent failure the check exists to kill.
- **Detect; never resolve.** Do not prefer one source, do not drop the other, do not rank them. Neither
  is authoritative over the other, and picking one silently discards the other's work while reporting
  success — the same boundary slice 03 drew for competing claims.
- **Read the board; never write it.** No card is moved, no Status is set, no comment is posted to make
  the two agree. Reconciling is a human's act — and where the forge's mirror workflows are enabled, a
  Status write is also an issue write, so there is no small correction available here either.

**`phil:issue-board` owns how a board is read**, including which call is trustworthy on each forge and
which under-reports. Delegate to it rather than inlining the mechanics; an under-reporting read here is
a **missed divergence**, the one failure this check cannot notice about itself. The repository's own
`CLAUDE.md` supplies the board's constants.

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
`BOARD-DIVERGES` · `BOARD-UNREADABLE`

A capture run reports exactly one of `CAPTURE` or `NO-OP`. `REFUSE-DERIVABLE` is **additional**:
report it alongside `CAPTURE` whenever derivable state was offered and left out, naming what was left
out.

`PROJECTED` and `PROJECTION-UNREFRESHED` are **also additional**, and only one of them appears, only
alongside `CAPTURE`, and only when the work has a card. **A `CAPTURE` with neither is a capture that
silently skipped the card** — which is the whole failure this pair exists to make visible, because the
snapshot is written either way and the run looks successful. `PROJECTION-UNREFRESHED` names what went
wrong and states that the snapshot stands regardless; a `NO-OP` never projects, because there is nothing
to project. A read-back run reports exactly one of `RESUME-CURRENT`, `RESUME-STALE`, or `RECONSTRUCT`, **and**
exactly one of `ROUTE`, `ROUTE-LIVE-WINS`, or `ASK-OWNER` — the freshness verdict and the owner are
independent facts, and a stale snapshot still has an owner worth naming.

**A third independent triple** joins them on the two paths that have a recorded next action to check:
`RESUME-CURRENT` and `RESUME-STALE` each report exactly one of `BOARD-AGREES`, `BOARD-DIVERGES`, or
`BOARD-UNREADABLE`. `RECONSTRUCT` reports none — with no snapshot there is nothing to compare.

**These are independent of the freshness verdict, and coercing one into the other is a gate failure.**
A board divergence is not staleness: the tree may be untouched while the work has moved on, which is
exactly the case #24 was filed for. Report both, and let them disagree.

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
  CAPTURE step 7 is the **only** sanctioned board write in this skill; read-back has none.
- **Report `BOARD-AGREES` for a board that could not be read**, or report nothing at all. Unreadable is
  a claim about the record; agreement is a claim about the work.
- Record a claimed card or its basis as a field. Tested and not built; the why already carries the basis.
- Restate the wave → command table. `skills/nwave-issue-board/SKILL.md` owns it; derive from there.

## Acceptance

`acceptance.feature` is the scenario SSOT. **`self-test/README.md` is the fixture register** — it holds
the roster, the must-pass set, what each fixture pins, and the driving rules. Read it before driving the
suite; do not drive from this section alone, and do not maintain a second roster here.

That split is deliberate and was earned twice. This paragraph carried its own fixture count, said
"ten" when there were twelve, and went stale again inside the commit that corrected it. A roster in two
places is a roster that disagrees with itself.

One rule is worth repeating because getting it wrong retires working fixtures: **the fixtures that
predate the board triple supply no `board_state`, so a read-back over them reports `BOARD-UNREADABLE`,
and that is a pass.** The register says which ones and why.

The suite is **model-driven, not automated** — there is no CI runner in this plugin, and
`tests/test_self_test_fixtures.py` does not drive these fixtures. Drive each one by giving this skill
the situation in its `manifest.json` and comparing the decision reached against its `expected.md`. Do
that whenever this file, either command loader, `skills/nwave-issue-board/SKILL.md` or
`skills/issue-board/SKILL.md` changes. Every failure mode here is silent — a snapshot that records too
much looks more complete, a stale one presented as current looks like a smooth resume, and a divergence
check that never fires looks like a board that always agrees.
