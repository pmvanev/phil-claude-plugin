---
name: session-handoff
description: Skill bundle for the phil:handoff, phil:resume and phil:stack commands — carries work across the session boundary and tracks where attention is inside one. Use when asked "where was I", "what was I doing before this", to push or record a diversion as it happens, to show the work stack mid-session, or to put a session down and pick it up. Records only what a fresh session cannot derive (the reasoning, the next action, the diversion stack, and the session's last three exchanges, copied verbatim from the transcript by a script and kept local), stamps a tree fingerprint, and projects a write-only copy onto the feature's card. On read-back it states a current/stale verdict, reports whether the board agrees about what is in flight — naming a divergence and never resolving it — then names the owning command without running it. Both reports are held to about 300 words; the stack view is not. Refuses to record derivable state, and never reads its own projection back.
---

# Session handoff — capture and resume

Three commands over one spine. `/phil:handoff` puts a session down; `/phil:resume` picks the work
up; `/phil:stack` tracks where attention sits inside one session. The first two report under a
300-word ceiling and the third deliberately does not — see *The report has a ceiling*.

The value is narrow and specific: **record only what a fresh session cannot work out for itself.**
Everything else is derived at read-back from whatever already owns it. A snapshot that also records
the derivable becomes a second authority over the same fact, and the two drift.

**The claimed-card link was slice 03, tested and deliberately not built.** Do not improvise it, and do
not read its absence as an oversight to correct — the reasoning is in `references/why-these-rules.md`.

## Reference files

Justification lives beside the procedure, not inside it. Read these when **changing** this skill:

- **`references/why-these-rules.md`** — the design history behind these rules: why the concurrency guard
  is content and not identity, why whole-file regeneration is safe, why the snapshot is per-worktree, why
  the projection is write-only, **why the stale threshold is two**, why read-back names the owner without
  running it, why a reconstructed briefing must be labelled, why *the boundary is the block, not the
  card*, why a `push` may stamp a header it did not inherit, **why the exchanges are copied by a
  script**, and what slice 03 settled.
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
| **The last exchanges** — the final three prompts and replies, the handoff's own included | **Yes, verbatim** | The next session starts with none of the conversation. Copied from the transcript by a script, never typed by this session — see *The last exchanges*. |
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
2. └ Fixture 07 · it contradicted the table, so it had to be settled first · open since 2026-08-12T16:40Z · crossed 1
3.   └ The fixture runner · it needed a flag it did not have · open since 2026-08-12T17:05Z · crossed 1

<!-- session-handoff:exchanges -->
### Prompt 1

does fixture 07 still contradict the table?

### Reply 1

It does. Row 4 routes DELIVER to `/nw-deliver`; the fixture expects `/nw-execute`.

### Prompt 2
…
### Reply 3
…
<!-- /session-handoff:exchanges -->
```

**The stack is innermost-last, numbered, and each frame carries what it is, why it was pushed, when, and
how many wind-downs it has survived**, in that order, separated by ` · `. Read bottom-up to find where attention is; read top-down to find what
it was diverted from. A frame is popped by deleting its line, so the file is the stack rather than a log
of stack operations.

**Every frame stamps the full `YYYY-MM-DDTHH:MMZ`, including the deeper ones.** The abbreviated form this
format shipped with was a readability nicety while the stack was only rendered; `show` and BOOTSTRAP
step 5b subtract an **age** from it now, and a frame carried across a handoff has likely crossed midnight.
The staleness rule does **not** read it — that is `crossed`'s job, and the two must not be conflated.

**`crossed` counts the wind-downs a frame has survived.** `push` writes `0`; `CAPTURE` adds 1 to every
frame already in the file. `CAPTURE` is the only thing besides `push` that writes any frame field, and
`crossed` is the only field it writes.

Two invariants follow, and a snapshot breaking either is corrupt rather than merely odd:

- **`crossed` never increases with depth.** Every frame present at a capture increments together, and a
  child cannot have been present at a capture its parent missed. `parent ≥ child`, always.
- **`crossed 0` means pushed since the last capture.** A frame whose `open since` predates a non-`never`
  `captured:` was in the file at that capture, so it is at least 1.

**A capture that records nothing new does not increment.** `/phil:handoff` run twice for one wind-down —
a correction, a second look — is not two wind-downs. Increment only where this capture's why or next
action differs from what is on disk. Without that, running handoff twice takes every open frame from 0
to 2 and marks the whole stack stale inside one session: the false alarm the threshold exists to
prevent, arriving from the other side.

**A frame carrying no `crossed` reads as unknown, never as 0.** Render `crossed ?` and never mark it. The
field is hand-editable and snapshots predate it; treating absent as zero under-reports silently, which is
the failure the mark exists to catch.

**Omit the section entirely when nothing was diverted.** An empty heading claims the work was
straightforward, which is a different thing from no claim at all.

**A frame with `crossed` of 2 or more is marked `⚠ stale`.** Two, not one: every frame carried across a
boundary has survived one, so marking at one marks the normal case. Why the threshold is two, and why
`crossed` is stored rather than derived: `references/why-these-rules.md` § *Why the stale threshold is two*.

**Never mark on age.** `crossed` counts wind-downs, not elapsed time. A frame open three days inside one
session is `crossed 0` and is where attention still is. Every frame renders its age so a human can judge
what the tool will not.

**The mark is computed at render time and never written to the file.** The snapshot stores `crossed`;
`⚠ stale` appears only in `show` and `pop`'s report.

**This rule's source is here.** `skills/nwave-issue-board/SKILL.md` restates it for the projected copy;
if the two disagree, this one wins.

The delimited header is machine-readable with `grep`/`sed`; the body is prose for a human. Read the
fingerprint from the header, never by parsing the prose.

## The last exchanges

**The final three exchanges of the session, the handoff's own the last of them, copied word for word
between the `session-handoff:exchanges` markers, last in the file.** Fewer where the session held
fewer. Decided 2026-09-24: the why and the next action say what was concluded, and the exchanges say
what was being talked about — the one thing a fresh session has none of.

**`${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py` is the region's only writer, and no exchange ever
passes through this session's own output.** Never type a prompt or a reply into a Write, an Edit, a
command or a printed line. The script copies them from the transcript Claude Code already keeps and
prints counts and hashes, never words. 0.97.0 had the session copy them itself, and Anthropic's safety
classifier refused 7 of 8 real handoffs for it — `references/why-these-rules.md` § *Why the exchanges
are copied by a script*.

- **An exchange is one human turn and everything this session printed until the next one.** An answer
  to a question this session asked mid-turn belongs to the exchange that asked it; it opens no new one.
- **A prompt is what the human typed.** For a slash command, the command line with its arguments —
  `/phil:handoff "pausing before the migration"` — never the body it expanded to. Pasted material stays.
  A built-in the harness answers itself, such as `/model` or `/clear`, opens no exchange.
- **A reply is the text this session printed**, its pieces joined in order. Tool calls, their inputs
  and their output are left out: they are the derivable half, and the bulk. Thinking is never printed,
  so it is never part of a reply.
- **Recorded, never composed.** The discriminator is *who composed the words*, and recording composes
  none: a reply is never regenerated, tightened or summarised for the file, and
  `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` is never applied to it. A reply was held to that standard, if
  at all, when it was written — the handoff's own report included, which step 11 composes under it.
  Whole replies, however long — the file is uncounted.
- **Exempt from refusing the derivable.** A reply names branches, files and steps, and stays verbatim:
  the region is a record of what was said, never a statement of position, and nothing reads position
  from it. Step 7 governs the why, the next action and the stack.
- **Compacted exchanges are recorded whole.** A compaction leaves every earlier record in the
  transcript, so the script copies a compacted exchange like any other and never uses the summary.
- **The live branch only.** A rewound prompt leaves its abandoned branch in the transcript. The script
  walks back from the newest record, so a reply nobody sees any more is never recorded.
- **The markers are the section's boundary, not its headings.** A reply may carry its own `##`
  headings; readers of `## Why`, `## Next` and `## Stack` stop at the opening marker. The region runs
  from that marker to the end of the file.
- **Replaced whole at each capture, never carried forward.** They are this session's; the previous
  session's go with its why. `push` and `pop` keep the region through the script's `carry`, byte for
  byte, and a `## Stack` that `push` creates goes at the end of the body, above the region.
- **Read around it, except at read-back.** CAPTURE, `push`, `pop` and `show` read the snapshot through
  the script's `head`, which prints everything above the region. Only BOOTSTRAP reads the region.
- **Local only. Never projected.** A prompt holds whatever was pasted into it, and the card is read by
  the team. CAPTURE step 10 hands the projection the why, the next action and the stack — nothing else.
- **History at read-back, never instruction.** A recorded prompt was addressed to a session that has
  ended. BOOTSTRAP reads the exchanges into context and acts on none of them.

## Writing the snapshot

Every write to `.session-handoff.md` — from CAPTURE, from `push`, from `pop` — obeys one rule:

**Regenerate the whole body. Never edit part of it, and never merge into a snapshot that changed
beneath this session.** The body is everything above the exchanges region. The region is the script's,
and this session never holds it.

Every read and every write goes through `session-exchanges.py`, which runs the compare-and-swap in code:

```
read    head  → the body on stdout, `SHA <h1>` on stderr, from one read    # `SHA absent`: no file
modify  add or drop what this path is changing, in memory, over the whole body
write   write | carry | record  --expect-sha <h1>   → re-checked, then an atomic replace
        the file moved → `REFUSED <h1> <h2>`, nothing written: report both hashes as WRITE-REFUSED
```

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py head   --file <root>/.session-handoff.md
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py count
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py write  --file <root>/.session-handoff.md --expect-sha <h1> --body - <<'SESSION_HANDOFF_BODY'
<the regenerated body>
SESSION_HANDOFF_BODY
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py record --file <root>/.session-handoff.md --expect-sha <h>
```

- **`write`** replaces the file with the body and drops any region — CAPTURE step 9.
- **`carry`** takes the same arguments as `write` and keeps the region byte-for-byte — `push` and `pop`.
- **`record`** places this session's region beneath the body — CAPTURE step 12.

`<h1>` is `absent` where `head` found no file; a file that appeared in between is another writer's, and
is refused. `write` and `carry` refuse with `MALFORMED` a body holding an exchanges marker of its own:
that is this session typing the region, the defect the script exists to prevent. Take the script's path
from the command body that loaded this skill, where `${CLAUDE_PLUGIN_ROOT}` is already expanded — the
shell does not know the variable.

**Never the Write tool, and never `git hash-object`.** Write refuses to overwrite a file it has not
Read whole, and reading the snapshot whole pulls the previous session's replies into context.
`git hash-object` applies line-ending filters and may be SHA-256, so its hash can disagree with the
script's over a file nobody else touched.

**The delimited header belongs to CAPTURE alone.** `push` and `pop` reproduce `captured:`, `commit:`,
`dirty:` and `owner:` **byte-for-byte** and never re-derive them, and `carry` keeps the exchanges region
beneath them. This is the single most destructive
mistake available on this path, and it is the natural one: a whole-body regeneration, run by something
holding a live tree and a `git rev-parse` grant, will re-stamp a fingerprint unless told not to. Re-stamp
it and `commit:` always matches `HEAD`, so `RESUME-STALE` never fires again — the worst outcome this skill
can produce, arrived at by a routine mid-session note.

**The why and the next action are composed by this session, so compose them against
`${CLAUDE_PLUGIN_ROOT}/rules/writing.md`.** They are written once, here, and `phil:nwave-issue-board`
renders them verbatim onto the card — so a padded sentence written here is padded on the surface with
the widest audience. Facts first, active voice, the emphatic word last. **Concision is one of the
standard's eleven principles of composition and never a licence to drop a decision or a ruled-out
approach**, because what a fresh session cannot derive is the whole reason the snapshot exists.

**The standard reaches the REPORT, not only the snapshot.** The paragraph above governs what goes
*into* the file. These are the sentences the paths **print**: the verdict and its distance, the wording
of the three board outcomes and of a divergence's two named sides, the withheld-count clause, the clause
labelling a briefing reconstructed rather than recorded, the `NO-OP` sentence saying nothing was
recorded and why, and the refusal naming the frame it did not write.

**Out, and passed through verbatim:** a frame's `what` and `why`, an `owner:` token, a commit hash, a
timestamp, a card title read from the board, and every outcome code. **The discriminator is the one
`${CLAUDE_PLUGIN_ROOT}/rules/writing.md` is applied by throughout this plugin — who composed the words,
never where they sit.** Terminal-only output exempts nothing; an enumeration lags as the report grows,
and the discriminator does not.

**The STACK is excluded, and it is the sharpest case in the family.** A frame's `what` and `why` are the
human's own arguments to `push`, and *the reason for a diversion exists only in the human's head at that
moment* — so existing frames are reproduced **byte-for-byte** and a new frame records what the human
said. Tightening a frame would leave the snapshot asserting the human's words over a sentence this
session had edited: the same defect `phil:groom-issues` forbids at a `you wrote` field, one surface over.
Pinned by `self-test/27-stack-frame-not-tightened/`.

`captured:` means *when the payload was captured*, not *when the file was last touched*. A push is not a
capture.

**A failed compare-and-swap refuses and reports. It never retries and never loops.** Retrying resolves a
competing write by overwriting it, which is arbitration; competing claims are **detected, not resolved**
here.

Report `WRITE-REFUSED` with both hashes **and the frame that was not recorded** — the pushed frame, or
the popped one — then stop. The reason for a diversion exists only in the human's head at that moment, so
a refusal that swallows it costs exactly what this feature was built to catch.

The file is **per-worktree**, not per-repo — `git rev-parse --show-toplevel` returns a linked worktree's
own root.

Why regeneration is safe, why the guard is content rather than identity, and where `core.autocrlf` lands:
`references/why-these-rules.md`.

## The report has a ceiling; the record never does

**300 words, counted over the whole rendered output of `/phil:handoff` and `/phil:resume`, including
every report line and every outcome code.**

**The ceiling binds the report and never the snapshot.** `.session-handoff.md` is written whole and
uncounted. A run that trims the file to fit its own output has inverted this skill: clipping a report
withholds a sentence a reader can fetch, and clipping the record destroys the one thing a fresh session
cannot derive.

**These never give ground, on either path:** the freshness verdict with its distance, the board outcome
and both named sides of a divergence, every stack frame with its age, its `crossed` where non-zero and
its `⚠ stale` mark, the next action, the owner route, the projection line, and the one line counting
the exchanges — at CAPTURE always, from step 6's count, since the region is written only after the
report prints; at read-back wherever the snapshot has one. **The exchanges themselves are never printed on either path** — the line is the
whole of their share of the report. Each is either a safety
property or a single line, and a report that drops one has spent the ceiling on the wrong half.

**The one line CAPTURE step 12 may print after the report sits outside the ceiling** — a refused or
unreadable `record`. The report was bounded before that outcome existed, and a refusal is never withheld
to fit.

**Mandatory means the frame, not a fuller rendering of it.** `crossed` stays suppressed at zero exactly
as *show* step 2 and step 5b specify — the ceiling never overrides a render rule, and reading it as a
licence to print more would make the bound its own cause.

**The why gives ground first, and CAPTURE's echo gives ground with it.** Print fewer decisions and
ruled-out approaches, state how many were withheld, and name the file holding them all. **Count the
withheld against the whole recorded population**, not against what was printed: a reader shown two
decisions needs to know whether seven wait in the file or none do.

**When the two rules collide, the ceiling yields and the run says so.** Print all the mandatory content,
breach, and state that the mandatory content exceeded the ceiling. **Dropping a stack frame is the worse
failure**, because a frame withheld to save words is a diversion nobody will remember — the loss this
skill exists to prevent.

**The two paths are not equally safe to clip, and the difference is stated rather than discovered.** On
read-back the withheld words are one file read away and the reader is often not their author. On CAPTURE
the author is present and the echo is the only proofread the record ever gets — step 11 exists so *a
mistake is visible immediately* — so a clipped echo weakens the one check that catches a
mis-recorded decision while the person who could fix it is still here. The echo is bounded anyway,
because an unbounded one reintroduces the wall of text the ceiling exists to prevent; the mitigation is
that `REPORT-CLIPPED` names the count, which tells the author there is something unread. **Accepted
cost, not a solved problem.** Pinned by `self-test/31-capture-echo-clipped/`.

**Never breach in silence and never clip in silence.**

**`/phil:stack` has no ceiling, deliberately** — stated here so nobody supplies the missing regime as a
tidiness fix. A read-back's own frames are mandatory content above, so the bound never reaches them
either; only the why gives ground.

Why the asymmetry makes a ceiling safe here, the arithmetic behind the collision case, and the accepted
cost of two prose regimes: `references/why-these-rules.md`.

## CAPTURE — `/phil:handoff`

1. **Decide whether anything happened.** The payload is the why and the next action. If neither can be
   stated, take the `NO-OP` path below, **however many files changed** — churn is derivable from git.

   `$ARGUMENTS`, when present, is the session's own account. Raw material for the why and the next
   action, never the record itself, and subject to every rule below.
2. **Collect the why.** State the decisions reached and, critically, the approaches **ruled out and
   why**. A decision without its discarded alternatives invites the next session to re-propose them.
3. **Collect the next action** — one sentence, concrete enough to start from.
4. **Record the owning command**, when the work has one. Derive it from the feature issue's wave label
   using the table in `skills/nwave-issue-board/SKILL.md`, which owns both. Omit `owner:` entirely when
   no wave label applies — most work has no owner, and that is not a defect.
5. **Carry the work stack forward, and increment it.** Read the snapshot through `head`; the `SHA` it
   prints is `h1`. The frames already in `.session-handoff.md` are **authoritative**: reproduce each
   one's what, why and `open since` **byte-for-byte**, and add 1 to its
   `crossed`. Never re-derive `open since` from the account or the clock — that makes every frame
   postdate its own capture and `⚠ stale` unreachable for ever after.

   Append a frame only for a diversion the session took, did **not** close, and that is not already
   present; new frames are `crossed 0`. A diversion closed before the session ended leaves no frame.
   **Done here, not after step 9**: a stack gathered after the write is not in the snapshot.
6. **Count the last exchanges, and collect none of their words.** `session-exchanges.py count` prints
   `EXCHANGES <n>` for the report's counting line, or `UNREADABLE <reason>` when this session's
   transcript cannot be found — carry the reason to the report, and skip step 12's `record`. Otherwise
   step 12 has the script copy them, this handoff's own among them, once its reply has been printed.
7. **Refuse the derivable.** If wave, slice, step, branch or file position comes up, leave it out and
   say so. Recording it is the defect, not an optimisation missed. The exchanges are exempt — see *The
   last exchanges*.
8. **Stamp the header.** `captured:` is the current time in UTC at minute precision
   (`2026-08-12T17:30Z`); `commit` is `git rev-parse --short HEAD`; `git status --porcelain`
   non-empty means `dirty: yes`.
9. **Write `.session-handoff.md` through the script's `write`**, `--expect-sha` the `h1` from step 5,
   under the compare-and-swap in *Writing the snapshot* above — the header, the why, the next action and
   the stack, **with no exchanges region**. `write` drops the previous session's, and this session's
   words are `record`'s to place. It prints `WROTE <h>`: that `<h>` is step 12's hash, so no window
   opens between writing and hashing. Never merge into a snapshot that changed beneath this session.
10. **Refresh the projection on the feature's card, if the work has one.** Local file first, always — a
   failed forge call must never cost the authority. Hand `phil:nwave-issue-board` the why, the next
   action and the stack with their capture timestamp; it owns the block. **Never the exchanges.** **Never
   read the card back.** A forge failure is an un-refreshed projection, not a failed capture.
11. **Compose the report** `CAPTURE`, echoing what was recorded so a mistake is visible immediately. Say
   whether the projection was refreshed, and where it was not, and in one line how many exchanges step 12
   will record — step 6's count, or its reason where there is none. **The echo obeys the 300-word ceiling and the file does not** — where the echo is clipped,
   report `REPORT-CLIPPED` with the withheld count and say the snapshot holds everything. A capture is
   never weakened to shorten its own echo.
12. **Print the report, then record the exchanges.** Print step 11's report exactly: it is this
   handoff's reply. Then run `session-exchanges.py record`, `--expect-sha` the `<h>` step 9's `write`
   printed. It copies the last three exchanges — this one and its just-printed report included — into
   the region, and prints `RECORDED <n> <sha>` and none of their words. **Print first because the
   transcript holds only what was printed.** **On `RECORDED`, print nothing further**: the recorded
   reply ends at the report, and a line after it would make what was printed differ from what was
   recorded. **Two writes because the report cannot precede the first**: it states the projection's
   outcome, and the projection must follow the local write.

   **Where `record` is refused**, another writer changed the file after step 9, and what it now holds
   is not this session's to describe. Print one more line: `WRITE-REFUSED`, both hashes, and that no
   exchanges were recorded and the file may no longer hold what step 9 wrote. Never retry and never
   merge. Report it beside `CAPTURE`, because the capture happened; never claim its payload still stands.
   **Where it prints `UNREADABLE`**, print its reason and that no exchanges were recorded. The capture
   stands; nothing else changed.

**Where no snapshot was ever projected, the card's stack section must render `unknown` — never empty.**
An empty stack asserts *no diversions*, which is a claim; `unknown` asserts *nobody wrote it down*.

Why the projection exists at all, and why it is write-only: `references/why-these-rules.md`.

### NO-OP

A session that advanced nothing writes **no** file. Report `NO-OP` and say that nothing was
recorded and why.

**The exchanges alone are not payload.** A session whose only content is conversation has no why and
no next action, so it records no exchanges either; recording them would make every session a capture.

Do not write an empty or placeholder snapshot. A resume point that says "no decisions, next action
unknown" is worse than none: the next session finds one, reads nothing in it, and learns to distrust
resume points generally.

Saying nothing was recorded is part of the outcome, not politeness — silence is indistinguishable
from the command having failed.

## STACK — `/phil:stack`

The stack is the only payload with **operations**. The why and the next action are stated once at
wind-down; a diversion happens mid-session, and the reason for it is only in the human's head while it
is happening. These three verbs exist so that reason can be caught then rather than reconstructed later.

All three read the snapshot through `head`. `push` and `pop` write the body back through `carry`, under
*Writing the snapshot*, header reproduced byte-for-byte; `show` writes nothing.

### push — `/phil:stack push "<what>" "<why>"`

1. **Require the why.** A frame naming only what was entered records the half that is derivable from the
   files being touched and drops the half that is not. Where `<why>` is missing, ask for it; do not infer
   it from the diff and do not write the frame without it.

   **That ask follows `${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md`.** Load it before the call. So does `ASK-OWNER` below.

   Two things that standard cannot know: the reason for a diversion exists only in the human's head at
   that moment, so the ask must not offer a guessed one as an option; and the frame's `what` is already
   on screen, so it belongs in the context block rather than the counted ask.

2. **Read the snapshot through `head`**; the `SHA` it prints is `h1`. `SHA absent` is the create
   path below.
3. **Append the frame** innermost-last, numbered, indented one step deeper than its parent, and stamped
   with the **full** current UTC minute plus a zero counter:

   ```
   <N>. <indent><└ if N>1><what> · <why> · open since <YYYY-MM-DDTHH:MM>Z · crossed 0
   ```

   Frame 1 carries no `└` and no indent. **Every frame carries the full date**, deeper ones included,
   because `show` subtracts an age from it. Staleness is `crossed`'s, never this field's.

   Where the file has no `## Stack` yet, create it at the end of the body. `carry` puts any exchanges
   region back beneath it, so the region stays last, where it must be.
4. **Write the body back through `carry`**, `--expect-sha` `h1`, or `absent` where no snapshot existed.
   It keeps the region byte-for-byte.
5. **Report** `PUSHED`, echoing the frame and the new depth, so a mistyped reason is visible at once.

**Where no snapshot exists, create one carrying the stack alone.** A diversion is payload, so this is
not the `NO-OP` case — but the why and the next action are **absent**, never invented.

Such a file still needs a header. Write `captured: never` and stamp `commit:` and `dirty:` from the tree
— the one sanctioned exception to the header rule, since there is no prior header to reproduce.
`captured: never` is the load-bearing token: a fingerprint exists, and no payload was ever captured
against it. What read-back does with that is *Read-back over `captured: never`* below.

**Never refresh the projection from `push`.** The card is refreshed at boundaries, by `/phil:handoff`;
a forge write per push would put the board on the critical path of a mid-session note.

### show — `/phil:stack`, bare

1. **Read the snapshot through `head`.** Ignore its hash; nothing is written. `SHA absent` is `unknown`.
2. **Render the trace**: every frame with what it is, why it was pushed, and how long it has been open.
   Mark the innermost — that is where attention is — and mark `⚠ stale` any frame whose `crossed` is 2
   or more, per *The snapshot* above. Render `crossed` where it is non-zero, so the mark shows its
   working rather than asserting a judgement.
3. **Report** `SHOWN`, or one of the two empties below.

**`unknown` and `none` are different answers and must not be collapsed.** No snapshot at all →
`unknown` (a claim about the record). A snapshot with no `## Stack` → `none` (a claim about the work).

### pop — `/phil:stack pop`

1. **Read the snapshot through `head`**; the `SHA` it prints is `h1`. `SHA absent` is `STACK-UNKNOWN`.
2. **Delete the innermost frame only** — the last line of `## Stack`. Popping anything else is editing
   the stack rather than navigating it; do that by hand, which the prose format allows on purpose.
3. **Remove the `## Stack` section entirely** when the last frame goes. An empty heading asserts the work
   was straightforward.
4. **Write the body back through `carry`**, header reproduced byte-for-byte.
5. **Report** `POPPED`, naming the frame now in hand and the new depth. **Where the popped frame was
   `⚠ stale`, say so** — closed silently, it takes with it the only signal that the record had drifted.

**Popping nothing is not an error, and the two nothings are different**, exactly as for `show`: no
snapshot at all → `STACK-UNKNOWN`; a snapshot with no `## Stack` → `STACK-EMPTY`. Either way **write
nothing**, and take no hash. Collapsing them asserts a fact about the work when the record is what is
absent.

**Popping the last frame off a push-created snapshot** — no `## Why`, no `## Next`, `captured: never` —
would leave a header and nothing else, which is the placeholder this skill refuses. **Delete the snapshot**
in that one case and say so. Where a `## Why` or `## Next` exists the file stays: a capture happened, and
its payload is not the stack's to discard.

## BOOTSTRAP — `/phil:resume`

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

### 7. Naming the owner

After the verdict and the content, name the command that owns the work — on every read-back path,
including `RECONSTRUCT`.

**`ROUTE`** — an owner is determined. State it and stop:

```
owner: /nw-execute  (wave: deliver)  → run it to continue
```

**Name it; never run it.** A read-back reports; it does not start work.

**`ROUTE-LIVE-WINS`** — the recorded `owner:` disagrees with what the feature's current wave label
implies. **The live label wins**, and the disagreement is reported rather than quietly settled:

```
owner: /nw-execute  (wave: deliver)
  recorded as /nw-distill — the wave advanced since this snapshot was written
```

**`ASK-OWNER`** — no `owner:` recorded and no wave label to derive one from. Say the owner is unknown
and ask. **Do not begin the work.** This is the common case on a mixed board, not an edge case: most
cards are not nWave work, and the absence of a label is not permission.

**`RECONSTRUCT`** — no snapshot exists. Derive the position from whatever owns it: the
`nwave-slice-status` skill for a feature's wave, slice, and step state, and git for the branch and
recent commits.

**Never invoke `/nw-continue` here** — it launches the next wave. **Label the briefing reconstructed,
not recorded**, including that the *why* is unavailable, because nothing derives it. The two carry
different warranties; `references/why-these-rules.md` says why blurring them invents confidence.

## Deriving, not duplicating

At read-back, fetch the derivable from its owner rather than the snapshot:

| Wanted | Ask | Read-only? |
|---|---|---|
| Where an nWave feature stands — wave, slice, step | the `nwave-slice-status` skill | yes |
| Branch, HEAD, working-tree state | `git` | yes |

Both delegates are read-only, and **enforced** so: the `nwave-slice-status` skill writes nothing, and
`/phil:resume`'s `git` grants are scoped to read-only subcommands.

Delegate; do not re-derive. These own their answers and have their own correctness gates.

**The board is not in this table** — these rows answer *what to look up instead of recording*; the board
answers *what to cross-check against*. Step 5 owns that read.

The asymmetry is deliberate: **never at capture, always at read-back.** The rule is not "never touch
position".

## Decision outcomes

Report the outcome by name, every run — one per phase:

`CAPTURE` · `NO-OP` · `REFUSE-DERIVABLE` · `PROJECTED` · `PROJECTION-UNREFRESHED` · `RESUME-CURRENT` ·
`RESUME-STALE` · `RECONSTRUCT` · `ROUTE` · `ROUTE-LIVE-WINS` · `ASK-OWNER` · `BOARD-AGREES` ·
`BOARD-DIVERGES` · `BOARD-UNREADABLE` · `PUSHED` · `POPPED` · `SHOWN` · `STACK-EMPTY` ·
`STACK-UNKNOWN` · `WRITE-REFUSED` · `REPORT-CLIPPED` · `CEILING-BREACHED`

A capture run reports exactly one of `CAPTURE` or `NO-OP`. `WRITE-REFUSED` is **additional** on a
capture only at step 12, beside `CAPTURE` and never terminal there: the capture was written at step 9,
and the refusal says the file has changed since. `REFUSE-DERIVABLE` is **additional**:
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

**A board divergence is not staleness**, and coercing one into the other is a gate failure: the tree may
be untouched while the work has moved on. Report both, and let them disagree.

**A stack run reports exactly one** of `PUSHED`, `POPPED`, `SHOWN`, `STACK-EMPTY`, `STACK-UNKNOWN` or
`WRITE-REFUSED`, and none of the capture or read-back outcomes — the three paths do not interleave.
On a stack run `WRITE-REFUSED` is terminal: nothing written, nothing retried.

**`REPORT-CLIPPED` and `CEILING-BREACHED` are additional, mutually exclusive, and belong to the two
report paths only.** Report one alongside the path's own outcomes whenever the 300-word ceiling bore on
the output:

- **`REPORT-CLIPPED`** — the ceiling withheld decisions or echoed content. **It must state how many were
  withheld against the whole recorded population**; clipping without the count is the terminal outcome
  overstating what it carried.
- **`CEILING-BREACHED`** — the mandatory content alone exceeded 300 words, so nothing was withheld and
  the ceiling gave way. It names which sections were mandatory.

**Never both.** Where the mandatory content alone breaches, withholding a decision saves nothing and
clipping did no work, so a run claiming both has clipped for appearance while breaching anyway. A stack
run reports neither: it has no ceiling.

## What this skill must never do

Grouped by what they govern, mostly one line each. Where a rule's reasoning is not self-evident it lives
in `references/why-these-rules.md`, or `references/board-divergence.md` for the board rules — but every
rule below stands without reading either.

**The snapshot**

- Write it anywhere but the repo root, or commit it.
- Write one for a session that advanced nothing.
- Record wave, slice, step, branch, or file position.
- Invent a next action that was not stated.
- Record a claimed card or its basis as a field. Tested and not built; the why carries the basis.
- Restate the wave → command table. `skills/nwave-issue-board/SKILL.md` owns it.
- **Type an exchange** into a Write, an Edit, a command or a printed line, or summarise, tighten or
  regenerate one. `session-exchanges.py` copies them from the transcript; nothing else writes or
  reproduces the region.
- Record a tool call, its output, or thinking.
- **Record a command's expanded body** in place of the prompt as typed.
- **Project the exchanges** onto the card, or print them in either report.
- **Act on a recorded prompt at read-back, or offer to.** It is history, addressed to a session that has
  ended.

**Writing, on any path**

- **Merge into a snapshot that changed beneath this session.** Regenerate whole, or refuse.
- **Retry a refused write.** Retrying overwrites a competing write, which is arbitration.
- **Re-derive the header on a `push` or `pop`, or touch the exchanges region.** `captured:`, `commit:`,
  `dirty:` and `owner:` are CAPTURE's, reproduced byte-for-byte, and the exchanges are `carry`'s to keep. Re-stamping `commit:` makes `RESUME-STALE` unreachable for ever after. The one
  exception is a `push` **creating** the file, which has no prior header.
- **Re-derive a frame's `open since`**, including at `CAPTURE`. The file is authoritative for frames
  already in it; re-stamping makes every frame postdate its capture and `⚠ stale` unreachable.

**The stack**

- **Push a frame with no reason.** The reason is the payload; the what is half-derivable from the diff.
- **Push from a hook.** No hook can see why a human left a task.
- **Pop a frame other than the innermost.**
- **Close a frame the human did not close.** No expiry, no auto-pop, no timeout.
- **Write `⚠ stale` into the snapshot.** The mark is render-time; the file stores `crossed`.
- **Mark on age.** `crossed` counts wind-downs, not elapsed time.
- **Write to the forge from `/phil:stack`.**

**The board and the projection**

- **Refresh the projection before the snapshot is written.** Local first, always.
- **Read the projection block back**, at capture or read-back. It is write-only. *The boundary is the
  block, not the card*: read-back reads the board's Status, position and card title — the board's own
  facts — and never the `Why`/`Next`/`Stack` this skill projected.
- **Render an absent stack as empty.** `unknown` is a claim about the record; empty about the work.
- **Publish the block itself.** `phil:nwave-issue-board` owns its format, markers and timestamp.
- **Resolve a board divergence.** Detect, name both sides, stop.
- **Write to the board during read-back.** The projection at CAPTURE step 10 is the only sanctioned board
  write in this skill.
- **Report `BOARD-AGREES` for a board that could not be read**, or report nothing at all.

**The ceiling**

- **Breach it in silence, or clip in silence.** Both make the terminal outcome overstate the report.
- **Clip the snapshot to fit the report.** The file is uncounted; the ceiling is a display bound.
- **Drop a verdict, a board outcome, a named side of a divergence, a stack frame, the next action, the
  owner route, the projection line or the exchanges line — at CAPTURE always, at read-back where there is a region to count — to stay under it.** The why gives ground; these do not. Dropping
  the projection line reproduces the silent card-skip that `PROJECTED` / `PROJECTION-UNREFRESHED` exist
  to make visible.
- **Report `REPORT-CLIPPED` without the withheld count**, or report it together with `CEILING-BREACHED`.
- **Apply a ceiling to `/phil:stack`.** Its absence is a decision, recorded above.

**Read-back**

- Present a stale snapshot as current, or bury the verdict beneath the content.
- **Run** the owning command. Naming it is the whole of routing here.

## Acceptance

`acceptance.feature` is the scenario SSOT. **`self-test/README.md` is the fixture register** — it holds
the roster, the must-pass set, what each fixture pins, and the driving rules. Read it before driving the
suite; do not drive from this section alone, and do not maintain a second roster here.

That split is deliberate and was earned twice — `references/why-these-rules.md` records how.

One rule is worth repeating because getting it wrong retires working fixtures: **the fixtures that
predate the board triple supply no `board_state`, so a read-back over them reports `BOARD-UNREADABLE`,
and that is a pass.** The register says which ones and why.

The suite is **model-driven** for the decisions; `tests/test_session_handoff_fixtures.py` structurally
guards every fixture but does not drive them. Drive each by giving this skill the situation in its
`manifest.json` and comparing the decision reached against its `expected.md` — whenever this file, any
of the three command loaders, `skills/nwave-issue-board/SKILL.md` or `skills/issue-board/SKILL.md`
changes. **Every failure mode here is silent**, which is why it is regression-tested rather than
eyeballed.
