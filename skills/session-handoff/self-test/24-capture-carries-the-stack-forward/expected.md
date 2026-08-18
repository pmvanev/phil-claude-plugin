# Expected — 24 (a wind-down through an open stack)

**Pins:** `CAPTURE` step 5, and the rule that makes `⚠ stale` reachable at all.

**Expected decision:** `CAPTURE`. The stack after the write:

```
1. Wave-to-command table · the task in hand · open since 2026-08-12T14:05Z · crossed 2
2. └ The fixture runner · it needed a flag it did not have · open since 2026-08-12T17:05Z · crossed 1
```

Two things happened and nothing else: **every `crossed` went up by one**, and **nothing else moved.**

**The session's account is wrong on purpose, and must lose.** It paraphrases frame 1's reason (*"working
through the routing table"* for *"the task in hand"*), gives a vague time (*"about 2pm"*), and omits
frame 2 completely. A capture that takes the account as its source would rewrite one frame and silently
delete the other — on a path documented as *regenerate the whole file*, where deletion needs no
mechanism, only an omission. **The file is authoritative for frames already in it.**

**Re-deriving `open since` is the failure this fixture exists to catch.** `CAPTURE` holds a `date` grant
and is writing a whole file; stamping "when" at collection time is the natural implementation and it is
catastrophic. Every frame would then postdate its own capture, `crossed` would still increment but the
timestamps would be lies, and the record of when a diversion actually started — the thing no artifact
holds — would be quietly replaced by the time of the last wind-down. This is exactly the header bug
(re-stamping `commit:` disables `RESUME-STALE`), one level down.

**Frame 1 reaches `crossed 2` and becomes stale on the next read.** That is the rule working end to end:
a diversion open through two separate sessions ending, marked at the third pick-up.

**A frame is appended only for a diversion the session took, did not close, and that is not already
present.** Neither applies here, so the stack gains no frame.

**Gate failures:**

- Any change to a frame's what, why, or `open since`.
- Dropping frame 2 because the account omitted it.
- Rewriting frame 1's reason to match the account.
- Not incrementing `crossed`, or incrementing by anything but one, or incrementing only the innermost.
- Setting a new frame's `crossed` to anything but 0 — not applicable here, and a fixture that passes by
  rewriting both counters to 0 has failed.
- Reporting `NO-OP`. A decision and a next action were both stated.
