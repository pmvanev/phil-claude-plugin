# Why these rules — the reasoning behind the spine

Reference for `skills/session-handoff/SKILL.md`. Everything here is addressed to someone **changing**
the skill, not to a session running it. The rules themselves live in `SKILL.md` and are authoritative;
if the two ever disagree, `SKILL.md` wins and this file is stale.

Split out 2026-08-18 on `plugin-dev:skill-reviewer`'s finding: the file had reached 5,656 words with the
justification interleaved with the procedure, so a session executing `push` was reading incident
narratives on the way past. The split is by **kind**, not by path — nothing loads a fraction of a
`SKILL.md`, so splitting the three paths into three files would simply mean loading all three.

## The claimed-card link was tested and deliberately not built

Slice 03's hypothesis — *the board already carries enough* — held. Do not improvise it, and do not read
its absence as an oversight to correct: the board's top Todo card answers *what is next*, and the basis
for a claim is what the `Why` section is already for. Recording it as a field would duplicate prose that
carries it, which is the drift this skill exists to prevent. The finding is in
[`slice-03-claimed-card-link.md`](https://github.com/pmvanev/phil-claude-plugin/blob/main/docs/feature/session-handoff/slices/slice-03-claimed-card-link.md).

One residual survived that investigation and shipped separately as the **board divergence check** (issue
#24). It is the narrow thing slice 03's verdict left standing — not *record which card was claimed*, but
*notice when the two records of what is in flight disagree*. It records nothing and resolves nothing, so
it does not reopen slice 03. See `board-divergence.md`.

## Why whole-file regeneration is the safe form, not the crude one

One writer that owns everything it rewrites cannot destroy a section it forgot about, because there is
no section it does not read. This is the property `skills/nwave-issue-board/SKILL.md` relies on for the
projected block — arrived at there after a partial refresh silently deleted the reasoning it did not
know it held.

## Why the concurrency guard is content and not identity

An earlier design stamped a session id in the header and refused a foreign one. That refuses the primary
path: resuming a *previous* session's snapshot is what this file exists for, so every session after the
first would be blocked on its first `push`. Comparing content catches the failure that matters — a lost
update, where A reads, B writes, A writes, and B's frame is gone with a call that reports success — and
needs no identity at all, which also means nothing has to survive compaction.

Recorded as DESIGN DDD-1 in `docs/feature/live-work-stack/feature-delta.md`, superseding a locked
DISCUSS decision.

**On `core.autocrlf`:** probed 2026-08-18. `git hash-object` normalises line endings under
`autocrlf=true` and `input`, so a CRLF file and its LF twin hash identically. It is still a pure function
of content and config, so hashing an unchanged file twice always agrees and **the compare-and-swap
produces no spurious refusals.** The narrow residue: a competing write that changes *only* line endings
is invisible to the guard. Not fixtured, because a fixture there would test git's determinism rather than
this skill's behaviour.

## Why the snapshot is per-worktree

`git rev-parse --show-toplevel` returns a linked worktree's own root, so each worktree already carries
its own snapshot — a fact of the shipped code rather than a decision anyone recorded. It is also right: a
worktree is a separate workspace holding separate work in flight. Two worktrees on one feature therefore
hold two snapshots and project to one card, which is arbitration, and still out of scope. This closed
ADR-013's open question.

## Why the projection exists, and why it is write-only

`.session-handoff.md` is git-ignored and machine-local by ADR-013, whose consequences state outright that
*"nothing is shared with a teammate"* — accepted for v1, with the partitioned local-plus-board option
named as the documented path if that need appeared. It appeared. The partition is exactly as that ADR
wrote it: **this file stays the single authority; the card carries a generated, timestamped, write-only
projection of it.** Nothing is read back, so no second authority exists to drift.

The cost, stated so nobody discovers it as a bug: a teammate sees only what the last `/phil:handoff`
projected. Where no snapshot was ever projected, the card's stack section renders `unknown` — never
empty. An empty stack asserts *no diversions*, which is a claim; `unknown` asserts *nobody wrote it
down*, which is the truth.

## Why the fixture roster lives in one place

`self-test/README.md` is the register, and `SKILL.md`'s Acceptance section must not carry a second copy.
That paragraph once held its own fixture count, said "ten" when there were twelve, and went stale again
inside the commit that corrected it. **A roster in two places is a roster that disagrees with itself.**

## Why the stale threshold is two

`CAPTURE` stamps `captured:` at wind-down, so **every frame open at that moment necessarily predates it.**
An earlier draft of the staleness rule compared `open since` against `captured:` and marked anything
earlier. That marks *every frame carried across a boundary* — which is precisely what this feature exists
to do, so the mark fired on the designed behaviour and on the abandoned frame alike, with the same glyph.

A mark that fires on the normal case is not an alarm, it is a decoration, and a decoration is what people
stop reading. That is this board's recurring defect wearing a different hat: a check whose output carries
no information still looks like coverage.

`N > 1` was the discriminator, and the first draft dropped it on the ground that the format could not
compute it — true of that format. The header carries one `captured:`, overwritten at every capture, so the
second-to-last is gone and no comparison recovers it.

**Storing one integer per frame buys the discriminator back.** `crossed` counts wind-downs survived:
written `0` by `push`, incremented by `CAPTURE` for every frame already in the file. At `crossed 2` the
claim is real — the diversion was open through two separate sessions ending.

The cost, accepted deliberately: `CAPTURE` becomes a writer of frame state, which an earlier design
refused. That refusal was a preference rather than a law, and `CAPTURE` already regenerates the whole
file. What it may **not** do is re-derive `open since` — that is the header bug one level down, and it
would make `⚠ stale` unreachable for ever after.

## Why read-back renders the stack, and `show` is not enough

A frame's staleness becomes *true* at the next pick-up. Leaving the mark to `show` alone means it is seen
only by someone who ran `/phil:stack` — i.e. someone who already remembered the frame. Issue #29's
done-when is that a never-popped frame is *visible*, and `commands/resume.md` promises the stack in as
many words, so BOOTSTRAP renders it.
