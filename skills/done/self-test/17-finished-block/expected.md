# Expected — DONE-SELFTEST-17

`CLOSED` · `BLOCK-REFRESHED`

## Situation

In an nWave repo the card's body holds `<!-- nwave:status:begin -->`, with a projected why, next action and stack. Every ask is done and the work landed.

## The developer answers

`yes`

## Writes, in order

the closing comment, then Status=Done, then the close, then the generated block's refresh

## What must happen

The block's writer renders the finished line from the closed issue's `closedAt`. `/phil:done` touches nothing inside the markers.

## What must NOT happen

- Edit anything between the markers itself.
- Refresh the block without the plan having shown it.
- Leave the projected next action standing on a closed card.
- Render `Stack: unknown` on the closed card.
- Merge anything.

## Why this fixture exists

D4 and AC3.3: the block has one writer, and a plain refresh would keep the projected next action and stack on finished work, or render `unknown` once no snapshot remains.
