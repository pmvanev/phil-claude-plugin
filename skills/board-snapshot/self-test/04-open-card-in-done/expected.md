# Expected — BSNAP-SELFTEST-04

`SNAPSHOT-RENDERED` · `DRIFT` · `READ-ONLY`

## What must happen

The three sections render normally. **One** drift line names both halves — the open card in Done and the
closed card outside it — and names `/phil:groom-issues` as what acts on them.

The drift line is counted in the 200 words like everything else.

## What must NOT happen

Nothing is written. No Status is set, nothing is closed, nothing is reopened. This command holds no write
and the drift is handed over rather than repaired.

The line is not exempted from the ceiling. A line outside the budget is the budget leaking, and the
budget is the feature.

## Why this fixture exists

`gh issue reopen` restores the issue and not the field, so an open card sitting in Done is the documented
aftermath of a recovery — and no board view flags the combination. The single call that fills the three
sections already returns both halves, so reporting it costs one line.
