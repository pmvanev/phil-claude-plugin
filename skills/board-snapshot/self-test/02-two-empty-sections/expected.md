# Expected — BSNAP-SELFTEST-02

`SNAPSHOT-RENDERED` · `READ-ONLY`

## What must happen

One leading sentence names both empty sections — that nothing is blocked and nothing is in flight. The
reader learns the sections were **checked**, in one line.

Five queued cards render in the order the forge returned them, with one clause saying the order is the
board's own.

## What must NOT happen

No heading is printed over blank space. Two empty headings cost three lines to say what one sentence says
in one, and they read as furniture rather than as information.

The queued cards are not sorted, re-ranked, or reordered by number, age or label. Board position is
consumed; `phil:rank-issues` is the only surface that produces an order.

`SNAPSHOT-CLIPPED` is wrong here. Printing 5 of 12 is N doing its job, not the ceiling forcing a cut.

## The sentence is composed, so the standard applies

This is one of the four clause types this skill writes rather than quotes, so
`${CLAUDE_PLUGIN_ROOT}/rules/writing.md` governs it: active voice, positive form, no padding. *"Nothing is
blocked and nothing is in flight"* passes. *"No cards are currently found to be blocked at this time"*
fails on all three counts while stating the identical fact.

Read the standard as **compose well, never compose short** — the 200-word ceiling is a separate constraint
and already does the bounding.

## Why this fixture exists

Taken verbatim from this repo on 2026-09-08. It is the rendering the maintainer meets most often, and the
one where the temptation to pad — with empty headings, or with all twelve cards — is strongest.
