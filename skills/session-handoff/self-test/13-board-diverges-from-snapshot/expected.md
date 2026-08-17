# Expected outcome — fixture 13 (the tree agrees, the board does not)

**This is the case `RESUME-STALE` cannot see, and the reason #24 exists.** The fingerprint matches
exactly — same commit, same clean tree — so every freshness check in the skill passes. Nothing about
the tree has moved. What moved is the *work*, and the tree is not where that is recorded.

Replayed from the live 2026-08-13 observation in
[`slice-03-claimed-card-link.md`](https://github.com/pmvanev/phil-claude-plugin/blob/main/docs/feature/session-handoff/slices/slice-03-claimed-card-link.md)
§ *The residual*: the snapshot's `Next` named a dogfood run, the board's top Todo was #15, and a human
resolved it by reading both. Nothing detected it.

**Pins:** issue #24 done-when — *"Read-back reports a divergence between the snapshot's `Next` and the
board's top Todo card, naming both and saying which is which — and does not resolve it."*

## Expected decision

Two outcomes, both reported, in this order:

1. **`RESUME-CURRENT`** — the fingerprint matches. This verdict is correct and must not be downgraded
   to `STALE` because the board disagrees. They are statements about different things.
2. **`BOARD-DIVERGES`** — the recorded next action and the board's in-flight claim name different
   work. Both are named, each labelled with its source:

```
BOARD-DIVERGES — the two records of what is in flight disagree.
  snapshot Next (captured 2026-08-13T21:10Z):
    dogfood /phil:groom-issues against this repo's own board
  board, top Todo (no card In Progress):
    #15 groom-issues slice 03 — set-level operations, all ask-first
Neither is authoritative over the other. Resolve before proceeding.
```

## Why the freshness verdict must stay `RESUME-CURRENT`

Folding the divergence into `RESUME-STALE` would be the cheap fix and it is wrong twice. It reports
the tree as having moved when it has not, and it hides the divergence inside a verdict whose stated
remedy — *the recorded next action may no longer apply* — is about commits. Two independent facts,
two independent outcomes, exactly as the freshness verdict and the owner are already independent.

## Gate failure (blocks the skill change)

- the divergence is detected and then **resolved** — one source preferred, the other dropped, however
  reasonably. Neither is authoritative; picking one silently discards the other's work while reporting
  success. This is the same boundary fixture `10` draws for competing claims.
- only one side is named. "The board disagrees" is not actionable; the reader cannot adjudicate what
  they cannot see.
- the freshness verdict is coerced to `RESUME-STALE`, or `RESUME-CURRENT` is withheld.
- the divergence is reported as a footnote after the briefing, rather than beside the verdict.
- the board is **written to** — a card moved, a status set — to make the two agree.

## The bias this fixture fixes in place

The match between a next action and a card title is **semantic, not string equality**, so it is a
judgement that can go either way. Bias toward reporting divergence: the outcome is advisory and
resolves nothing, so a false positive costs the reader one line, while a false negative is the exact
silent failure the card was written to kill.
