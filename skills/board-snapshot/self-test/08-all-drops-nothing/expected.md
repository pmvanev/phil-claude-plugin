# Expected — BSNAP-SELFTEST-08

`SNAPSHOT-RENDERED` · `UNCOLUMNED` · `READ-ONLY`

## What must happen

Forty rows, one per open card, in board order. Each carries a number, a title and a description of 100
words or fewer. The uncolumned card is among them, marked as sitting in no column.

The output is long. That is correct.

## What must NOT happen

No card is dropped. No total ceiling is applied — the standing check's 200 words governs the standing
check and nothing else.

`SNAPSHOT-CLIPPED` is not reported. In this mode it can only mean a card went missing.

## Why this fixture exists

The per-mode bound is the decision the feature turns on. A total ceiling over forty cards buys five words
each, and a read that drops thirty-five cards to stay short has answered a different question than the
one asked.
