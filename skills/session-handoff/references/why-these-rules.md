# Why these rules — the reasoning behind the spine

Reference for `skills/session-handoff/SKILL.md`. Everything here is addressed to someone **changing**
the skill, not to a session running it. The rules themselves live in `SKILL.md` and are authoritative;
if the two ever disagree, `SKILL.md` wins and this file is stale.

Split out 2026-08-18 in two passes on `plugin-dev:skill-reviewer`'s findings. The first, at 5,656 words,
moved the board-divergence narrative and the core design history out; the second, after slice 02 pushed the
file back to 5,896, moved the rest and tightened the procedure prose to under 5,000. Both had the same
cause: justification interleaved with procedure, so a session executing `push` read incident narratives on
the way past. The split is by **kind**, not by path — nothing loads a fraction of a
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
no section it does not read. The exchanges region is the one exception since 2026-09-28: the session no
longer reads it, so the session no longer rewrites it either — `carry` keeps it in code, which is the
same property held by the only writer that can see the section. This is the property `skills/nwave-issue-board/SKILL.md` relies on for the
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

**Since 2026-09-28 the hash is `session-exchanges.py`'s, not git's.** The script hashes raw bytes on both
sides of the swap, so it is still a pure function of content and still produces no spurious refusals —
and a competing write that changes only line endings is now visible. `git hash-object` left the
procedure because its filters and a SHA-256 repo can make it disagree with the script's own hash.

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
body. What it may **not** do is re-derive `open since` — that is the header bug one level down, and it
would make `⚠ stale` unreachable for ever after.

## Why read-back renders the stack, and `show` is not enough

A frame's staleness becomes *true* at the next pick-up. Leaving the mark to `show` alone means it is seen
only by someone who ran `/phil:stack` — i.e. someone who already remembered the frame. Issue #29's
done-when is that a never-popped frame is *visible*, and `commands/resume.md` promises the stack in as
many words, so BOOTSTRAP renders it.

## Why read-back names the owner and never runs it

`/phil:resume` has no `Write`, no `Edit`, and read-only `Bash`. Running the owner would route around all
three — `/nw-execute` writes code. This mirrors `nwave-slice-status`, which prints the resume command as
text and never runs it. `/nw-continue` is refused for the same reason plus one more: it computes much the
same position and then *launches the next wave*, which is the side effect `nwave-slice-status` exists to
avoid.

## Why a reconstructed briefing must be labelled

A recorded briefing carries reasoning that was witnessed. A reconstructed one carries position inferred
from files. They have different warranties, and blurring them invents confidence the reader has no way to
audit — the same failure as presenting a stale snapshot as current, arrived at from the other side.

## Why `ROUTE-LIVE-WINS` reports the disagreement instead of settling it

Silently preferring the live wave label hides that the snapshot has drifted — the one signal that would
tell the reader their capture habit is falling behind. The live value still wins; what is refused is
winning *quietly*.

## Why "the boundary is the block, not the card"

The never-do list forbids reading the projection back, and until 2026-08-17 that rule read *"never the
card"* — which the #24 divergence check made false the moment it shipped, while the real invariant went
unwritten. Read-back reads the board's **Status, position and card title**: those are the board's own
facts, not a copy of anything this skill wrote. What it must never read back is the `Why` / `Next` /
`Stack` it projected, because those **are** a copy, and a snapshot reconciled against its own projection
has become the two authorities the whole design exists to prevent.

## Why a `push` may stamp a header it did not inherit

The header rule says `push` and `pop` reproduce the header byte-for-byte. The one exception is a `push`
that *creates* the snapshot: there is no prior header to reproduce, so `commit:` and `dirty:` are stamped
from the tree and `captured:` is written `never`. Without the exception the never-do list reads as
forbidding the behaviour fixture 20 pins.

## Why the ceiling binds the report and not the record

`phil:board-snapshot` set the precedent — 200 words over the whole rendered output, fewer rows when the
bound would break, a stated withheld count, and a breach announced rather than a card dropped in
silence. This skill copies that shape and gets one thing that skill cannot have: **the withheld words
are still on disk.**

A snapshot clipped to fit a report is unrecoverable, and it is unrecoverable in the exact dimension the
snapshot exists for. Everything else a reader wants — wave, slice, branch, file position — is derivable,
which is why the never-do list refuses to record any of it. The decisions and the approaches ruled out
are the residue that nothing derives. So the file is written whole and uncounted, and the report is a
view over it. **That asymmetry is the whole licence for a word bound here**; without it a ceiling would
be trading the payload for brevity, which is the exchange the standard's concision principle is most
often misread as endorsing.

It also decides which half gives ground. The verdict, the board outcome and the stack frames are each a
line or two and each is a safety property — a stale snapshot followed confidently, a divergence nobody
noticed, a diversion nobody remembers. The why is the only elastic section, and it is the one whose full
text is a single file read away.

## Why the collision case breaches instead of trimming

**Measured 2026-09-09 against this skill's own worked examples**, counting whitespace-separated tokens:
the quantified `STALE` verdict runs 22 words, the `BOARD-DIVERGES` block naming both sides 47, the
recorded next action 12, a `ROUTE-LIVE-WINS` route 16, and a terse stack frame with its age, `crossed`
and stale mark about 20. The fixed part of a worst-case read-back therefore costs about 97 words, and
each terse frame adds twenty.

**Depth alone is a poor route to a breach**: six frames reach 217, and eleven are needed to pass 300.
This paragraph first carried the estimates 30, 60, 25 and 40, which put a six-deep stack over the bound
on its own — measuring refuted that. Corrected rather than quietly kept, because a rationale nobody
checks is this board's recurring defect, and an arithmetic one is checkable in a minute.

**The real route is a frame's own words.** A frame's `what` and `why` are the human's arguments to
`push`, reproduced byte-for-byte and never tightened — so among all the mandatory content they are the
one part whose length is unbounded *and* unshortenable by this skill even in principle. Four frames
carrying a paragraph of somebody's reasoning each will pass 300 words where four terse ones cost eighty.
That is the shape fixture 29 supplies, and it is why the collision rule is written as a rule rather than
as a depth threshold.

At the point of breach, withholding every decision saves nothing, and the only remaining way under the
bound is to drop a frame or a named side of a divergence — destroying a safety property to satisfy a
display bound, and in the frame's case destroying the human's own words to save room. Hence: print all
of it, say the ceiling gave way, and never report `REPORT-CLIPPED` alongside `CEILING-BREACHED`. A run
claiming both has clipped for appearance while breaching anyway.

## Why `/phil:stack` carries no ceiling

Decided 2026-09-09, when the bound was put on the two report paths. A deep stack is the whole reason
somebody runs `show`, and a limit there would drop frames from the one view built to display them all —
the same failure as dropping a frame from a read-back, arrived at by policy instead of by accident.

**The accepted cost, stated rather than discovered:** the same frames render under a bound inside a
read-back and unbounded on their own, so the family carries two prose regimes on purpose. That
inconsistency is visible and cheap; the alternative silently loses diversions. Recorded here because an
unexplained gap in a regime invites someone to close it as tidiness, and this one is a decision.

## Why the bound is 300 where the precedent is 200, and why a breach is not a decoration

Both questions have one answer, and it is the difference between the two reports.

`phil:board-snapshot` bounds an output **every section of which it may withhold**: when 200 words will
not do, it prints fewer queued cards. Its mandatory sections can breach on a badly stuck board, which is
why it has a collision rule at all, but the normal case always has give. This skill's report does not.
The verdict, the board outcome, the frames, the next action and the owner route are all mandatory, and
**a frame's length is the human's, not this skill's** — reproduced byte-for-byte and never tightened. So
the floor here is set by somebody else's prose, and no amount of discipline moves it.

At 200 the floor would clear the bound routinely: the measured fixed cost is 97 words before a single
frame, and three terse frames reach 157. A bound that breaches on the ordinary case is exactly the
failure *Why the stale threshold is two* names — **a mark that fires on the normal case is a decoration,
and a decoration is what people stop reading.** 300 is chosen so the ordinary read-back fits with room
for the why: four terse frames under a diverging board cost 177, leaving 123 words of decisions, and a
three-deep stack over an agreeing board costs 125.

**So the breach is rare by construction, and the arithmetic says which cases produce it.** Eleven terse
frames, or a handful carrying a paragraph of the human's reasoning each — fixture 29's shape, measured
at 352. Both are genuinely exceptional, and both are cases where the alternative is discarding a safety
property or editing somebody's words. `CEILING-BREACHED` fires there and nowhere else, which is what
keeps it an alarm.

**What would refute this:** `CEILING-BREACHED` appearing on ordinary read-backs in practice. That would
mean real stacks carry far wordier frames than the measurement assumed, and the answer would be to raise
the bound rather than to start withholding frames — the floor is not negotiable, so the ceiling is the
only part that can move. Recorded so the next person does not reach for the frames instead.

## Why the exchanges are copied by a script

**0.97.0 had the session copy its own last three replies into the snapshot, and it never worked once.**
Measured 2026-09-28 across every transcript on the author's machine: of 8 real handoffs on 0.97.0, 7
were stopped by Anthropic's safety classifier, every refusal carrying the category `reasoning_extraction`
and the explanation *"restrictions on reverse engineering or duplicating model outputs"*. The 15 handoffs
on earlier versions drew none. The eighth ran on a just-cleared session with nothing to copy.

**The stop landed on the snapshot write.** In the one session where the withheld Write survives in the
transcript, 12,328 of its 15,558 characters were the exchanges region, and it breaks off mid-sentence
inside the first reply. After a stop, Claude Code retries with a notice, and the retry was refused too;
one session refused eight turns running, including a plain question about why. So the region was never
written, and the fixtures that pinned *what* it held passed on prose no run could reach.

**The copy was not a copy anyway.** That withheld reply is 58% similar to the one it claimed to
reproduce, with a longest exact stretch of 225 characters. Asked to copy its own output, a model retypes
it from memory — the regeneration this skill forbids in the same paragraph that asked for the copy.
The classifier is not the only reason to take the words out of the session's hands; it is the one that
made the other visible.

**So the script reads the transcript, which Claude Code already writes to disk, and the session never
holds the words.** That settles both defects at once: nothing is reproduced by the model, and the copy is
exact by construction. It also removed two rules that existed only because the session did the copying:

- **Compacted exchanges were counted and left out**, because a session holding the summary could not
  honestly reproduce them. The transcript keeps every record across a compaction, so they are recorded
  like any other. The rule's reason was the session's blindness, not the summary's existence — and the
  summary is still never what was said.
- **The handoff's reply was recorded before it was printed**, by a second whole-file write the session
  composed. Now the report prints first and `record` copies it: the transcript holds only what was
  printed, so what the file holds is what was printed without anyone having to promise it.

**`push` and `pop` were the second instance of the same hazard, found before it fired.** Whole-file
regeneration meant retyping a previous session's replies byte-for-byte on every mid-session note. They
now read through `head` and write through `carry`; the session regenerates the body and never the region.

**What stays unmeasured: read-back.** BOOTSTRAP still reads the region into a fresh session's context,
which is input, not reproduction, and the classifier stopped output. No read-back of a populated region
has ever run, because none was ever written. **What would refute this design:** a `reasoning_extraction`
refusal on `/phil:resume` over a snapshot holding exchanges. The answer then is to stop reading the
region into context and name its path instead, not to shorten it.

**Two facts the order of CAPTURE step 12 stands on, measured on 2.1.283 on 2026-09-28.** Printed text is
in the transcript before the next tool runs: a line printed at 14:13:41 was on disk when the Bash call
at 14:13:43 read the file. And the Bash tool's environment carries `CLAUDE_CODE_SESSION_ID`, which names
the transcript. Neither is documented. If either stops holding, `count` at step 6 prints `UNREADABLE`
or `record` finds the handoff's reply empty — visible in the report, never a paraphrase in the file.

**The transcript format is Claude Code's, and it is not published.** The shapes the script relies on —
the `isMeta` body that follows a command the model acts on, the `local-command-stdout` after a built-in,
the `compact_boundary` whose `logicalParentUuid` crosses it, the `parentUuid` chain that names the live
branch past a rewind — were read from real records on 2.1.283, and the tests build them byte-for-byte.
A change there degrades what `record` finds — fewer exchanges than three, an empty reply, or a new kind
of harness record mistaken for a prompt — but everything it writes is still text from the record, never
a model's paraphrase, which was the failure being replaced.
