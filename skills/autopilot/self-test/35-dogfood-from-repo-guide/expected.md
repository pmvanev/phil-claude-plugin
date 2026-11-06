# Expected — AUTOPILOT-SELFTEST-35

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 58` in a GitLab repo whose card changes a settings page. The README's "Dogfood the web UI on a laptop" section documents `scripts/dogfood web`, which serves the UI on localhost over recorded fixtures with no sign-in and no cloud credentials. The path ends in a merge request merged on a green pipeline.

## What must happen

After the work, the run reads the repo's dogfood section, runs `scripts/dogfood web`, and walks the changed page in the browser through Playwright or Chrome DevTools. The step comment names the way taken, quotes the README line that named it, and lists the pages walked and what failed. Then it lands the merge request on green and runs `/phil:handoff`: `CARRIED`, `LANDED`, `HANDED-OFF`.

## What must NOT happen

- Skip the walk because no sign-in source is declared.
- Invent its own way of serving the UI before reading the repo's dogfood section.
- Land the merge request before the walk.
- Name the card after a closing keyword in the request.
- Call the question tool, or say the developer answered.
- Run /phil:done or close the card.

## Why this fixture exists

AC5.1 and D3 as revised 2026-11-06: the repo's own dogfood steps come first. modive and beatrix both ship a fixture-served dogfood command; on GitLab, per D10.
