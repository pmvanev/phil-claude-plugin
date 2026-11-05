# Expected — HTP-SELFTEST-09

`PROFILE-NOT-BUILT` · `SAMPLE-REFUSED`

## What must happen

The script refuses the run. `SAMPLE-REFUSED` lists `session.jsonl` as a transcript, and the report says no
profile was built, so the author can name the samples again without the transcript.

## What must NOT happen

- The transcript is not read.
- The profile is not quietly built from the other sample alone.

## Why this fixture exists

Typed prompts measure as instructions, not prose. The script enforces the decision to read only
named documents, and this is where it fires.
