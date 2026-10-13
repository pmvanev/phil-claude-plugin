# Expected outcome — fixture 07 (an earlier pointer survives a run that cuts no history)

**Situation.** Run this fixture from a committed copy. An earlier run already hardened the file and
left a recovery pointer naming the version before it. Nothing in the file holds history to cut: each
rule is one reflex, and the one wound is already a single line.

**Pass.** The last line is byte-for-byte unchanged, still naming `0000000`. The report says no history
was cut.

**Fail.**
- The pointer is rewritten to name the copy's current commit. The new hash holds the same text, so the
  line now points one hop further from the history it was written to recover.
- The pointer is deleted, or a second pointer is added.
- The wound line is cut. It is one line of why, not history.

Run with a rule that does carry history, the run cuts it and replaces the pointer with the copy's
current commit; that version still carries the `0000000` line, one hop back.
