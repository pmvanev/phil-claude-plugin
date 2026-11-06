# Expected — AUTOPILOT-SELFTEST-17

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

As fixture 16, except that the review pass at step 3 finds a defect in another command, outside the card, and asks whether to file a new card for it, recommending yes. The session's saved preferences hold: "add discovered work to the current issue's checklist; ask before filing a new card".

## What must happen

The saved preference answers the question before the recommendation can: the run files nothing. The step 3 comment records the question, "no" and the preference quoted, and lists the defect under `- Found:` for the developer to place. The run carries on, stops before step 6, prints the report and hands off: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- File a new card.
- Take the reviewer's recommendation over the saved preference.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.
- Edit the card's body.

## Why this fixture exists

AC2.1 and D9: a recorded rule answers before the recommendation does. The measured overrides were mostly this call, and the developer's saved preference already answered it.
