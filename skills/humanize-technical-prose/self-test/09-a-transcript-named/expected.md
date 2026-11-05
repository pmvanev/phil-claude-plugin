# Expected — HTP-SELFTEST-09

`PROFILE-NOT-BUILT` · `TRANSCRIPT-REFUSED`

## What must happen

The script refuses the run. `TRANSCRIPT-REFUSED` lists `session.jsonl`, and the report says no
profile was built, so the author can name the samples again without the transcript.

## What must NOT happen

- The transcript is not read.
- The profile is not quietly built from the other sample alone.

## Why this fixture exists

Typed prompts measure as instructions, not prose. The script enforces the decision to read only
named documents, and this is where it fires.
