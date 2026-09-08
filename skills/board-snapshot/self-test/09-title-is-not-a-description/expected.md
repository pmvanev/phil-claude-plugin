# Expected — BSNAP-SELFTEST-09

`SNAPSHOT-RENDERED` · `READ-ONLY`

## What must happen

The title appears verbatim. The description is composed from the body and says what the card is for and
what would change if it were done — under 100 words, and under the writing standard.

Where the body leaves a real question open, the description says so. On a card of this kind the open
question is often the most useful thing in a hundred words.

## What must NOT happen

The title is not reworded into the description. The `reworded_title` counterexample in the manifest is
the exact failure: it is accurate, it is short, and it tells a reader nothing they did not have from the
title column.

The body's opening sentences are not lifted. Cards routinely open with context and state their purpose
several paragraphs later.

The description does not exceed 100 words. The `over_the_bound` counterexample is a real breach, and the
driver checks that it genuinely is one rather than trusting the label.

## Why this fixture exists

This mode's whole deliverable is compression. Both failures — rewording the title and lifting the opening
— produce a table that looks right and carries no information the reader did not already have.
