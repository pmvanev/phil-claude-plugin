# Expected — 17 (the compare-and-swap fires, and stops there)

**Pins:** slice-01 AC3, and the arbitration boundary inherited from slice 03.

**Expected decision:** `WRITE-REFUSED`. Nothing is written. Both hashes are named so the human can see what
happened rather than being told it failed:

```
WRITE-REFUSED — .session-handoff.md changed between read and write.
  read   a1b2c3d
  verify 9f8e7d6
  Your frame was NOT recorded: fixture runner · the runner needs a flag it does not have
  Another session or worktree is writing this snapshot. Nothing has been merged or overwritten.
```

**Why refuse rather than retry.** A retry loop resolves a competing write by overwriting it. That is
arbitration between two live sessions, which `session-handoff` slice 03 declared out of scope and this
feature inherits verbatim: competing claims are **detected, not resolved**. Retrying would also succeed
almost always, which is what makes it tempting and what makes the data loss it causes invisible.

**Why the frame is echoed in the refusal.** The reason for the diversion is the payload and it exists only
in the human's head at this moment. A refusal that discards it silently costs exactly the thing the feature
was built to catch. Print it back so it can be re-pushed or written down.

**Why both hashes.** "Something changed" is unactionable. Naming the hashes lets the human confirm the file
really moved rather than suspecting the tool.

**Gate failures:**

- Retrying, in a loop or once. Terminal means terminal.
- Merging the two versions, in any form — most seductively "the other session only added a frame, so keep
  both". That is arbitration, and it is a judgement no tool here is licensed to make.
- Writing anyway because the change looked unrelated. The check is the whole guarantee; a conditional check
  is no check.
- Dropping the frame from the report.
- Reporting a generic error. `WRITE-REFUSED` is a specific, expected outcome, not a fault.
