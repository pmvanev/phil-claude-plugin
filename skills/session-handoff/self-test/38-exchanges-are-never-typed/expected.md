# Expected — 38 (the exchanges never pass through the session)

**Expected decision:** `CAPTURE`.

## What must happen

1. The snapshot is read through `session-exchanges.py head`. The previous session's region never
   enters this session's context at capture.
2. `count` supplies the report's counting line. No exchange is collected.
3. Step 9's `write` holds the header, the why, the next action and the stack — **no exchanges region**,
   neither the previous session's nor this one's.
4. The report is printed. Then `record` runs, and prints `RECORDED 3 <sha>`. Nothing it wrote is
   printed or read back.

## Why this fixture exists

0.97.0 had the session write its own last three replies into the snapshot. Anthropic's
`reasoning_extraction` classifier refused 7 of the 8 real handoffs that followed as *duplicating model
outputs* — the stop landed on the Write carrying the replies, so the region was never once written, and
one session went on refusing ordinary prompts for eight turns afterwards. The one withheld copy that
survives matched its original only 58%, longest exact stretch 225 characters: asked to copy, the session
retyped. No fixture caught it, because every fixture described *what* the region must hold and none
said *who may put it there*.

## Gate failures

- **Any prompt or reply in the session's own output**, however it is framed — a Write, an Edit, a
  heredoc, a quoted echo in the report. The classifier reads output, not intent.
- **Reading the whole snapshot at capture.** It pulls the previous session's replies into context for
  no purpose; step 5 needs only the stack above the region.
- **Typing the exchanges when `record` prints `UNREADABLE`.** Report the reason and that none were
  recorded; the capture stands without them.
