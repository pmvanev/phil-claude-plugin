# STACK — `/phil:stack`

Part of the `session-handoff` skill. `SKILL.md` governs this path as much as this file does: the
snapshot format, *The last exchanges*, *Writing the snapshot*, the ceiling, the decision outcomes and
the invariants all apply here.

The stack is the only payload with **operations**. The why and the next action are stated once at
wind-down; a diversion happens mid-session, and the reason for it is only in the human's head while it
is happening. These three verbs exist so that reason can be caught then rather than reconstructed later.

All three read the snapshot through `head`. `push` and `pop` write the body back through `carry`, under
*Writing the snapshot* in `SKILL.md`, header reproduced byte-for-byte; `show` writes nothing.

## push — `/phil:stack push "<what>" "<why>"`

1. **Require the why.** A frame naming only what was entered records the half that is derivable from the
   files being touched and drops the half that is not. Where `<why>` is missing, ask for it, and write the
   frame only once the human has given it — never a reason inferred from the diff.

   **That ask follows the decision-request standard `SKILL.md` names.** Load it before the call.

   Two things that standard cannot know: the reason for a diversion exists only in the human's head at
   that moment, so the ask offers no guessed reason as an option; and the frame's `what` is already
   on screen, so it belongs in the context block rather than the counted ask.

2. **Read the snapshot through `head`**; the `SHA` it prints is `h1`. `SHA absent` is the create
   path below.
3. **Append the frame** innermost-last, in the frame template *The snapshot* in `SKILL.md` gives,
   stamped with the **full** current UTC minute and `crossed 0`. **Every frame carries the full date**, deeper ones included,
   because `show` subtracts an age from it. Staleness is `crossed`'s, never this field's.

   Where the file has no `## Stack` yet, create it at the end of the body. `carry` puts any exchanges
   region back beneath it, so the region stays last, where it must be.
4. **Write the body back through `carry`**, `--expect-sha` `h1`, or `absent` where no snapshot existed.
   It keeps the region byte-for-byte.
5. **Report** `PUSHED`, echoing the frame and the new depth, so a mistyped reason is visible at once.

**Where no snapshot exists, create one carrying the stack alone.** A diversion is payload, so this is
not the `NO-OP` case — but the why and the next action are **absent**, never invented.

Such a file still needs a header. Write `captured: never` and stamp `commit:` and `dirty:` from the tree
per *The snapshot* — the one sanctioned exception to the header rule, since there is no prior header to reproduce.
`captured: never` is the load-bearing token: a fingerprint exists, and no payload was ever captured
against it. What read-back does with that is BOOTSTRAP step 5c, in `references/bootstrap.md`.

**Never refresh the projection from `push`.** The card is refreshed at boundaries, by `/phil:handoff`;
a forge write per push would put the board on the critical path of a mid-session note.

## show — `/phil:stack`, bare

1. **Read the snapshot through `head`.** Ignore its hash; nothing is written. `SHA absent` is `unknown`.
2. **Render the trace**: every frame with what it is, why it was pushed, and how long it has been open.
   Mark the innermost — that is where attention is — and mark `⚠ stale` any frame whose `crossed` is 2
   or more, per *The snapshot* in `SKILL.md`. Render `crossed` where it is non-zero, so the mark shows its
   working rather than asserting a judgement.
3. **Report** `SHOWN`, or one of the two empties below.

**`unknown` and `none` are different answers and must not be collapsed.** No snapshot at all →
`unknown` (a claim about the record). A snapshot with no `## Stack` → `none` (a claim about the work).

## pop — `/phil:stack pop`

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
