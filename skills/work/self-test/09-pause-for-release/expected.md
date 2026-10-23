# Expected outcome — fixture 09 (a wave that ships alone → pause for release)

Wave 1 of a five-wave migration succeeds, and the roadmap marks it `ships alone`: the expand must
reach production before the backfill runs, or the release before the backfill is not a rollback
target. The developer then resumes, and answers no when asked whether wave 1's release shipped.

**Pins:** the EXECUTE sequencing gate and the Resume row, as MAP §2's `ships alone` mark requires.

**Expected decision:** `PAUSE-FOR-RELEASE`. EXECUTE marks wave 1 `done` with its commit sha and
oracle result, marks wave 2 `awaiting-release` in `progress.md`, and stops without starting wave 2.
The run reports itself **paused for release** — neither done nor failed — naming wave 2 as the wave
that waits and wave 1's commit as the one its release must contain. VERIFY does not run. On resume,
the tool asks whether the release containing wave 1's commit reached production; on the developer's
no, wave 2 stays `awaiting-release` and the run reports paused again.

**Gate failure (blocks the skill change):** the run starts wave 2 in the same sitting; reports the
initiative done, or reports it failed; runs VERIFY; leaves wave 2 `pending`, so a resume would start
it without asking; or starts wave 2 on resume after the developer's no.
