# Expected — DONE-SELFTEST-13

`CLOSED`

## Situation

Mid-session the developer asked to move the card to In Progress and to add a scope line to its body. The board shows In Progress and the body holds the line. The card's one pull request merged into main, which is green.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close

## What must happen

ASKS reads `2: 2 done, 0 open`, the Status ask citing the board read and the scope ask citing the card's body. The developer answers `yes`, and the card closes comment-first.

## What must NOT happen

- Mark a card edit open because no pull request carries it.
- Verify a code ask from the card's body.
- Merge anything.

## Why this fixture exists

Dogfood, `/phil:done 75` on 1.17.0 (2026-11-02): three of eight asks edited the card or the board, and the evidence table named only a pull request, a commit or a file.
