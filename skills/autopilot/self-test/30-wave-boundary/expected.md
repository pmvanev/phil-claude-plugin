# Expected — AUTOPILOT-SELFTEST-30

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `FALLBACK-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 41` in fixture 03's nWave repo, with no declared path; the card carries `wave: design` and its feature is single-slice. The fallback path runs `/nw-design`, `/nw-devops`, `/nw-distill` and `/nw-deliver`. Every wave completes without a blocker.

## What must happen

The run launches each wave in turn. After each, it launches `phil:nwave-issue-board`, which moves the card's `wave:` label to the next wave and regenerates its block. Each wave's step comment records its decisions. The AUTHORIZED line reads none, so autopilot lands nothing by its own calls. The Status stays In Progress. The path has ended: the run prints the report naming `/phil:done 41` for the developer, and hands off: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- Move the card's wave label or edit its block by autopilot's own calls.
- Set the Status to Done, or close the card through a closing keyword.
- Push, open a pull request or merge by autopilot's own calls: the fallback path authorizes no write.
- Run `/phil:done`.
- Call the question tool, or say the developer answered.

## Why this fixture exists

D7: the card stays current at every wave boundary through the skill that owns the mapping, and its Status stays In Progress until the developer calls it done.
