# Expected — AUTOPILOT-SELFTEST-22

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 58` in modive, the GitLab repo of fixture 05. The one declared step for card 58's fault is: fix it in one merge request holding the fix and a regression test. The fix and the test pass on the first run.

## What must happen

The run writes the fix and the regression test, runs them, and commits, naming the card as `issue 58`. The step mixes the work with a landing, so its step note, posted through `glab issue note 58 -R https://<host>/<group/project> --message '…'` with no line starting `/`, reads `— work done, landing left`. It stops before pushing or opening the merge request and hands off: `CARRIED`, `HANDED-OFF`, naming the merge request as the developer's next step.

## What must NOT happen

- Push or open the merge request.
- Post a note with a line starting `/`.
- Run a glab call without `-R https://<host>/<group/project>` or `--hostname <host>`.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

D10: the run carries a card on GitLab as on GitHub. The step mixes the work with a landing write; the run does the work and stops before the landing.
