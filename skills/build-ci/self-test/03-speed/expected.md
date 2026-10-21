# Expected outcome — fixture 03 (speed)

A GitLab service's last five main pipelines, recorded under `project/history/` as the forge's job lists,
with each job's log under `project/logs/`. The median pipeline takes 12:37. Its critical path is `build`
→ `test` → `package`, with 1:30 of it spent waiting for runners. `lint` is the slowest job at 8:00, and
it runs off the path. The logs show where the path's time goes: `build` and `test` each spend about 3
minutes in `npm ci` with no cache, and `test` waits for `build` though it tests the source and never
reads `dist/`: `vitest.config.ts` includes `test/**`, and the tests import from `src/`.

**How to drive it:** copy `project/` to a scratch directory and follow this working tree's
`skills/build-ci/SKILL.md` with `--speed`. Treat `history/` as what the forge returned for step 1 and
`logs/` as each job's log; fetch nothing. The fixture has no MR pipelines. Answer "no" to the question
whether to make the changes.

**Expected:** a report with the measured wall clock, execution and queue wait; the critical path with each
job's median duration and queue wait; and ranked candidates, each with a saving, an effort class and its
evidence, cut by a stopping line.

**Hard assertions (any failure blocks the change):**

- **The critical path is `build` → `test` → `package`**, measured with
  `skills/build-ci/scripts/pipeline-timings.py`, not guessed from the CI file.
- **Queue wait is reported apart from execution** — about 1:30 of the median — and is not the first
  item, since the best candidate saves more.
- **`lint` and `gitleaks` are not candidates.** Both are off the path; `lint` may be named as off it.
- **Dropping `test`'s wait on `build` ranks first, High at effort S.** `test` tests the source and never
  reads `dist/`, and its result gates nothing `build` does. Alone it brings the median to about 8:25, the
  runner-up, where `lint` becomes the path; no saving is claimed below that.
- **`release` is excluded** from the measure: a person starts it.
- **A dependency cache is never ranked on a guess.** It ranks High only with evidence of what it saves;
  the logs give `npm ci`'s total time, not how much of it a cache restore would skip, so leaving it
  unranked with that reason is correct.
- **Sharding `test` is below the line, or absent.** Its tests run 2:10 of the job's 6:00.
- **The stopping line is drawn,** and the pipeline projected under it is within the ten-minute budget —
  after the first candidate, since that alone reaches the budget.
- **The pass asks before editing, and edits nothing** on "no". It gives the command to re-measure.

**Not a failure:** savings that differ from these by up to a minute; ranking the cache as one candidate
or as one per job; naming the release job's manual start as off the path.
