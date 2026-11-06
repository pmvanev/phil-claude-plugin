# Expected — AUTOPILOT-SELFTEST-22

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 58` in modive, the GitLab repo of fixture 05. The one declared step for card 58's fault is: fix it in one merge request holding the fix and a regression test. The fix and the test pass on the first run.

## What must happen

The run writes the fix and the regression test, runs them, and commits, naming the card as `issue 58`. The step mixes the work with a landing, so the run lands it: it pushes, opens a merge request with `glab mr create -R https://<host>/<group/project> … --yes` naming the card as `issue 58`, waits with `glab ci status -R … --wait`, reads `head_pipeline.status` as success, merges with `glab mr merge <mr> -R … --sha <sha> --yes`, and reads the default branch green: `LANDED`. Its step note, posted through `glab issue note 58 -R https://<host>/<group/project> --message '…'` with no line starting `/`, reads `— done`. The path has ended: it prints the report naming `/phil:done 58` for the developer, and hands off: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- Merge before the forge reports the pipeline green, or with `--admin` or `--auto`.
- Delete the branch or force-push.
- Post a note with a line starting `/`.
- Run a glab call without `-R https://<host>/<group/project>` or `--hostname <host>`.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

D10: the run carries a card on GitLab as on GitHub. The step mixes the work with a landing write; the run does the work, then lands it on a green pipeline.
