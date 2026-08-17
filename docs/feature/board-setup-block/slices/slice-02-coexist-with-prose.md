# Slice 02 — Coexist with prose the probe cannot regenerate

**Goal:** Insert the region into a `CLAUDE.md` whose `## Issue board` section is already full of
hand-written prose, without disturbing a byte of it — and report what the probe now confirms,
contradicts, or cannot evaluate.

**Stories:** S2 (add generated constants to a repo whose block is already hand-written)

## Learning hypothesis

**Disproves the delimited-region model** ([D4]) if the region cannot be placed without either
duplicating facts the prose already states, or orphaning prose that then reads as contradicting the
generated lines beside it. If placement forces a choice between duplication and contradiction, the
model is wrong and the whole-section-with-provenance alternative has to be reconsidered.

**Confirms**, if it passes, that a generated region can live inside a hand-written file — which is what
separates this feature from every other generated block in the plugin, where nothing human belongs.

**Dogfood target: this repo.** Its block is the hardest available case — mostly hazards recorded after
contact, none of it reproducible by any probe, and several lines stating facts the region will now own.

## IN scope

- Read and classify the existing file: no section · section without markers · region current · region stale.
- Insert the region into an existing section without wrapping, moving, reordering or reformatting any
  existing line.
- A drift report over the content **outside** the markers, in three buckets: **confirms** (the prose
  agrees with the probe), **contradicts** (it disagrees), **cannot evaluate** (nothing probed bears on it).
- The **retire offer**: for a contradicting line stating a fact the region now owns, offer to remove it —
  applied only on an explicit answer, declined silently leaves no trace.
- Refusals: malformed markers (`begin` without `end`, or nested); file changed between read and write.

## OUT of scope

- Rewriting or reflowing any hand-written line. The only permitted change outside the markers is
  deleting one whole line, on an explicit answer.
- Migrating this repo's block wholesale — #32 puts that out of scope and this slice honours it.
- Elicitation (slice 03) and assumption labels (slice 04).

## Acceptance criteria

1. Content outside the markers is **byte-identical** before and after, on every path including failure
   and including the refusal paths — verified with `git diff` restricted to those line ranges.
2. A contradicting hand-written line is reported and **not edited**.
3. The retire offer applies only on an explicit answer; silence writes nothing and records nothing.
4. `begin` without `end` refuses with the file unchanged. The region's extent is never guessed.
5. Placement is deterministic: two runs against the same file put the region in the same place.

## Dependencies

Slice 01 (the probe).

## Effort · reference class

≤1 day. Reference class: `groom-issues` slice 02 — mechanical changes inside an agreed boundary, each
reported with the reason it needed no judgement.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — a reader, a placer, a drift report |
| Depends on a new abstraction? | Reuses slice 01's probe |
| Disproves a pre-commitment? | Yes — [D4], the second-largest untested commitment |
| Synthetic data? | No — this repo's real `CLAUDE.md` |
| Identical to another slice but for scale? | No — differs from 01 by the presence of prose, not by size |
