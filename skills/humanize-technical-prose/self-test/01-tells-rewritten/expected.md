# Expected — HTP-SELFTEST-01

`WROTE`

## What must happen

- Each of the six tells is rewritten with the fix `ai-eos`'s catalogue names. The participle clause
  and the closing paragraph are cut. *Serves as* becomes *is*. The contrast becomes a plain statement
  of what the budget is. *Plays a crucial role in keeping* becomes what the worker does: it keeps the
  warehouse current.
- The re-check over the changed sentences finds no tell.
- The report's `TELLS:` line counts as many rewritten as found, with `re-check: 0 left`. *Serves as*
  counts only if `ai-eos` reports it, because that catalogue reports copulative avoidance as a ratio.
  The report lists each change by line with its before and after, and ends with the undo line.

## What must NOT happen

- No protected span changes: `MAX_RETRIES`, `INGEST_RETRY_BUDGET`, `ingest.deadletter`, *120*,
  *a minute*, the heading and the shell block stay byte-for-byte.
- No fact appears that the draft did not hold.
- A sentence with no tell is left alone.

## Why this fixture exists

It is the skeleton's happy path, and its protected spans sit next to the tells, so a careless
rewrite would change them.
