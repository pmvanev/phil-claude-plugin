# Expected — WSUM-SELFTEST-03

`SUMMARY-RENDERED` · `READ-ONLY`

## What must happen

The most recently touched feature is resolved and summarised. The output names it and its date, and says
plainly that the default is the most recently **touched** feature.

## What must NOT happen

The output does not call it the most recently completed stage. Nothing records completion, and the two
differ exactly here: a feature touched an hour ago sorts above one finished last week.

Completion is not inferred from the artifact's contents. That is a status derivation, and every
derivation over these files belongs to `phil:nwave-slice-status` — a second one drifts against the first.

The target is not taken from the branch, the editor, or the conversation.

## Why this fixture exists

A wrong target produces a summary that is internally perfect and about the wrong feature. Naming the
artifact and its date is the only thing that makes that visible in the first line rather than never.
