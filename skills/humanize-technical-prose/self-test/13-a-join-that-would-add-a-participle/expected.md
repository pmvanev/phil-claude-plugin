# Expected — HTP-SELFTEST-13

`WROTE`

## What must happen

- Sentences are joined toward the profile's median with *and*, *then*, *so* or a subordinate clause,
  such as *After the backoff expires, the job retries the call.*
- Step 5 re-runs the hunt over every joined sentence. Any join that trips the detector goes back to
  its Step 3 form.
- The report's voice line ends `tells after: 0`.

## What must NOT happen

- No trailing *-ing* clause is bolted onto a joined sentence.
- A participle is not kept on the grounds that the author's samples hold them.
- The numbers and *dead-letter table* stay as written.

## Why this fixture exists

A voice pass that imitates the writer can bring back what the tells pass removed. Here the
participle is the easiest join, and Step 5 is what stops it.
