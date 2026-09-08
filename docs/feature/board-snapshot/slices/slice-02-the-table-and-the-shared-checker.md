# Slice 02 — The per-card table, and the checker underneath it

**Goal:** Ship `--all`, printing every open card as number, title and a description of 100 words or
fewer; and, as its precursor, split the shipped word counter from the vocabulary rules it is welded to.

**Stories:** S2, and S4 as a precursor commit
**Answers:** issue #34's shape question, and the reuse decision taken 2026-09-08

## Learning hypothesis

**Disproves [D1] — that one command can carry both reads — if the two modes turn out to share neither
their data nor their composition rules.** The standing check needs Status and board order; the table
needs every body. If slice 01's call cannot serve both, these are two commands wearing one name and the
flag is a lie.

**Disproves [D10] — that anything is genuinely shared with the existing enforcer — if separating the word
ceiling from the vocabulary list leaves a counter so thin that the extraction costs more than the copy.**

**Confirms**, if both hold, that the third surface asking for this shape can consume it rather than
re-derive it.

## IN scope

- **Precursor commit, landing first and separately:** parameterise the decision-request hook so the word
  ceiling and the forbidden-vocabulary list are independent. Behaviour byte-unchanged, proven by that
  hook's own suite before anything else is written. **[D12]** — this is not a slice, because it ships no
  user-visible output.
- `--all`: every open card, one row each, number and title verbatim, description composed from the body.
- **[D4]** — bounded per card at 100 words, unbounded in total. Nothing is dropped to fit a budget.
- Cards sitting in no column are named as such, never omitted.
- The description is **composed**, never the first sentence of the body and never the title reworded.
  **`rules/writing.md` governs it, per [D13]** — and [D13]'s contradiction with the sibling scan is
  recorded in the delta, not resolved here.
- Fixtures: KPI-2 on this repo's live twelve cards; KPI-4 proving two call sites; KPI-5 proving the hook
  unmoved.
- Version bump.

## OUT scope

- Stripping internal handles from the descriptions — slice 03. This slice bounds the length; the next one
  bounds the vocabulary. Splitting them is what makes [D11] testable.
- Changing what the decision-request hook *enforces*. The extraction moves code, never rules.
- Any total ceiling on the table. [D4] refuses it, because dropping a card is the one failure a board read
  may not have.
- Resolving [D13]. It needs a mechanism and it is a route-2 finding against the repo.

## Acceptance criteria

S2's four and S4's three. KPI-5 blocks the slice: a hook whose behaviour moved fails it outright.

## Dependencies

Slice 01, for the command and the forge read.

## Effort

One day. The precursor is the risky half and it is guarded by an existing suite.

## Reference class

`board-prose-standard` slice 02 — a driver extracted beside a live second consumer rather than ahead of it.

## Dogfood moment

Same day: run `--all` against this board and compare it against the table hand-composed on 2026-09-08.
**That table is the reference output**, and a description materially worse than its hand-written
counterpart is a finding, not a nit.

## Taste tests

- **Ships 4+ new components?** No — one flag, one extraction.
- **Depends on a new abstraction?** It *is* the abstraction, landing beside its second consumer. That is
  the taste test being satisfied, not dodged.
- **Disproves a pre-commitment?** Two: [D1] and [D10].
- **Synthetic data only?** No. Twelve live cards, and a hand-written reference output to lose against.
- **Only-infrastructure slice?** No — S2 carries the value, S4 is a precursor commit inside it.

## Pre-slice SPIKE

None. The extraction's shape is readable from the hook, which is 186 lines.
