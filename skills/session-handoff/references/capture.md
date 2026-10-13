# CAPTURE — `/phil:handoff`

Part of the `session-handoff` skill. `SKILL.md` governs this path as much as this file does: the
snapshot format, *The last exchanges*, *Writing the snapshot*, the ceiling, the decision outcomes and
the invariants all apply here.

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
   present, in the frame template *The snapshot* gives; new frames are `crossed 0`. A diversion closed before the session ended leaves no frame.
   **Done here, not after step 9**: a stack gathered after the write is not in the snapshot.
6. **Count the last exchanges, and collect none of their words.** `session-exchanges.py count` prints
   `EXCHANGES <n>` for the report's counting line, or `UNREADABLE <reason>` when this session's
   transcript cannot be found — carry the reason to the report, and skip step 12's `record`. Otherwise
   step 12 has the script copy them, this handoff's own among them, once its reply has been printed.
7. **Refuse the derivable.** If wave, slice, step, branch or file position comes up, leave it out and
   say so. Recording it is the defect, not an optimisation missed. The exchanges are exempt — see *The
   last exchanges* in `SKILL.md`.
8. **Stamp the header** from the tree, per *The snapshot* in `SKILL.md`: `captured:` at the current UTC
   minute, `commit:` as the short HEAD, `dirty:` from `git status --porcelain`.
9. **Write `.session-handoff.md` through the script's `write`**, `--expect-sha` the `h1` from step 5,
   under the compare-and-swap in *Writing the snapshot* in `SKILL.md` — the header, the why, the next action and
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

## NO-OP

A session that advanced nothing writes **no** file. Report `NO-OP` and say that nothing was
recorded and why.

**The exchanges alone are not payload.** A session whose only content is conversation has no why and
no next action, so it records no exchanges either; recording them would make every session a capture.

Write no empty or placeholder snapshot. A resume point that says "no decisions, next action
unknown" is worse than none: the next session finds one, reads nothing in it, and learns to distrust
resume points generally.

Saying nothing was recorded is part of the outcome, not politeness — silence is indistinguishable
from the command having failed.
