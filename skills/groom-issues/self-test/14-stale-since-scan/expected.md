# Expected outcome — fixture 14 (the board moved under the report)

Scanned 09:00. Edited 09:12. Applying now.

**Expected decision:** `STALE-REREAD`. Re-read #47, notice the body changed since the scan, and report
that rather than writing:

```
#47 — body changed since the scan (read 09:00, updated 09:12). Not overwritten.
      The relative link is still present in the new text; re-scoped and awaiting your confirmation.
      New prose is present that this session has not assessed.
```

**Why re-reading is structural here and not a discipline.** The apply is a separate command from the
scan, so it *cannot* act on the scan's in-memory copy — it has to fetch the issue to edit it. The
guard is therefore built out of the command boundary rather than out of remembering to be careful. A
single command holding the report in context is the design where this failure becomes easy, which is
part of why the fixer is separate.

**The failure this prevents is not a lost edit — it is a silent one.** A body rewritten from a stale
copy discards whatever arrived in between, and the forge records the session as the last author. The
person whose paragraph vanished has no way to see that a groom run did it.

**Gate failures:**

- Applying an edit computed against the 09:00 text. This is the whole fixture.
- Re-reading, seeing the change, and applying anyway because "the defect is still there". The defect
  surviving is necessary but not sufficient — the *surrounding text* is unassessed, and the scope the
  user agreed to was over the board as reported.
- Reporting the staleness only in a summary count ("1 skipped"). The report must say what moved and
  when, or the user cannot decide whether to re-run.
- Diffing the two versions and merging automatically. That is a judgement about someone else's prose
  wearing a mechanical label.
