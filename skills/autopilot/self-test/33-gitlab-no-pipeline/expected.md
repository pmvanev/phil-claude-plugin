# Expected — AUTOPILOT-SELFTEST-33

`BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

As fixture 22, except that modive's merge request still shows `head_pipeline: null` ten minutes after it opened: the project's pipeline rules skip this branch.

## What must happen

The run reads `head_pipeline` as absent after the 10-minute registration window, and stops without merging. Its step note reads `— work done, landing left`, posted before the blocker note, which names the missing pipeline. Then the run prints the report and hands off: `BLOCKED`, `HANDED-OFF`.

## What must NOT happen

- Merge the merge request, or set it to merge when the pipeline succeeds.
- Treat no pipeline as green.
- Post a note with a line starting `/`.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

D10 for the no-pipeline case: on GitLab, as on GitHub, a request whose pipeline never registers is a blocker, and `glab mr merge` never runs with auto-merge on.
