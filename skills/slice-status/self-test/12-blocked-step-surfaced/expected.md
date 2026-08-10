# Expected outcome — fixture 12 (a failed step is not merely the next one)

Positionally, `02-02` is the first not-done step, so the default rule calls it `current` and moves
on. But it is not waiting to be started — it was started and it failed. A returning user reading
`current` will pick it up expecting fresh work and rediscover the failure themselves.

**Expected decision:** `BLOCKED`.

**Checkable assertions (all must hold):**

1. `02-02` is `blocked`, not `current`.
2. Its Notes cell names the failure point recorded in `.develop-progress.json` — one clause, enough
   to recognise it.
3. `02-03` is not promoted to `current`. Nothing advances past a blocked step.
4. The failure is reported, not diagnosed. No root-cause analysis, no proposed fix, and above all
   the failing test is **not re-run** to confirm it — that would violate the first hard rule.

**Gate failure (blocks the skill change):** `02-02` shown as `current` or `next` with no sign it
failed; OR running the suite to check whether the recorded failure still reproduces; OR offering to
fix it. Every one of those turns a status question into an intervention.
