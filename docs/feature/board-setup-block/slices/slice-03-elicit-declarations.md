# Slice 03 — Elicit what no forge records

**Goal:** Ask Robin the questions no forge can answer — the label families first — with the board's own
contents shown as evidence and never adopted as an answer, and write the result outside the markers as
Robin's declaration.

**Stories:** S3 (declare what the forge cannot record, without the tool guessing it)

## Learning hypothesis

**Disproves the elicitation design** if Robin cannot answer the family question from the evidence
offered — if answering still requires opening the forge UI or reading the whole board, the question is
in the wrong form and asking it is the same failure as asking for an id.

**Confirms**, if it passes, that the probe/elicit split has a workable human half, and that a
declaration produced this way is what `phil:groom-issues` rule 4 needs.

## IN scope

- The label-family question: for each label family found on the board, ask whether it is single-valued
  (swap, never add) or multi-valued by decision.
- **Evidence beneath the question, never inside the answer**: the labels in use, their co-occurrence
  counts, and which issues carry more than one. Displayed; never pre-selected; never defaulted to.
- Write the answer **outside** the markers, attributed — `you declared`.
- The decline path: write nothing, and say in the report that rule 4 will keep reporting `unevaluated`
  for that family.
- The ambiguous-reply path: "ok" / "sure" / "sounds right" is treated as unanswered and asked once more,
  naming what is still needed.
- The disagreement path: a declaration that contradicts what the labels suggest is written as given, with
  the disagreement recorded beside it rather than resolved.
- KPI-4 measured: run `/phil:groom-issues` afterwards and confirm rule 4 reports *evaluated*.

## OUT of scope

- Inferring any family, under any confidence, from any evidence ([D6]). This is the one thing the slice
  exists to make impossible.
- Eliciting anything the probe could have answered.
- Assumption confirmation (slice 04) — that reuses this machinery and follows it.
- Any other elicited field beyond label families. Others may exist; this slice establishes the shape.

## Acceptance criteria

1. No family is ever pre-selected, defaulted, or written on silence.
2. A declaration contradicting the labels in use is written as given — verified against this repo, where
   `bug` + `documentation` + `enhancement` co-occur on #2 and #4 **by decision**.
3. A decline writes nothing and the report names what stays unevaluated.
4. An ambiguous reply is asked once more, never resolved by composing.
5. Every elicited line is attributed; an unattributed line is the defect (C3).
6. KPI-4: rule 4 reports *evaluated* on a repo this slice configured.

## Outcome — authored 2026-08-17

| AC | Verdict | Evidence |
|---|---|---|
| 1 | **PASS** | `derive_label_evidence` is tested adversarially against itself: a forbidden-key test asserts no family carries `single_valued`, `multi_valued`, `likely`, `confidence`, `inferred`, `suggested_answer` or `default`. The payload states in its own `note` that it holds no answer. |
| 2 | **PASS (unit), NOT dogfooded** | `test_a_declaration_contradicting_the_evidence_is_written_as_given_with_the_disagreement`. This repo's real answers both *agreed* with observed use, so the path is covered by test and fixture 09, not by the live run. Recorded rather than claimed. |
| 3 | **PASS** | A family absent from `answers` is absent from the output; `render_declarations` returns `None` when nothing was declared. Fixture 08 pins that no "declined" line is written. |
| 4 | **PASS by design** | The ambiguous-reply rule is prose in `SKILL.md` and fixture 08. Not code-enforceable — the ambiguity is in a human's reply, not in a value. |
| 5 | **PASS** | Every declared line carries `*(you declared · <date>)*`; tested. |
| 6 | **DEFERRED** | KPI-4 needs `/phil:groom-issues` run against a repo this slice configured, and the released plugin is behind the working tree. The declared region exists in this repo's `CLAUDE.md`, so the measurement is available to the next session. |

### Learning hypothesis — CONFIRMED, against a real human

**Both questions were answered from the evidence offered, with no forge UI opened.** That is the
hypothesis, and it was tested the only way it can be: by asking a person.

- `(unprefixed)` — `bug`, `documentation`, `enhancement`; counts 7/11/22; co-occurring pairs
  documentation+enhancement 6×, bug+documentation 3×; nine issues carrying more than one →
  **multi-valued by decision**.
- `wave` — one member in use, no co-occurrence observed → **single-valued**.

Both answers match what `CLAUDE.md` already declared by hand, which is a consistency signal and
**not** the test. The test was answerability, and the co-occurrence counts plus the issue numbers were
what made it answerable — a reader can check `#2` and `#4` themselves in seconds.

**The `wave` question needed a caveat the evidence could not supply.** Zero observed co-occurrence is
consistent with single-valued but does not demonstrate it, because only one member is in use. That was
stated in the option rather than left for the answerer to notice — evidence that under-determines an
answer must say so, or it argues for a conclusion it cannot support.

### Two findings

**A `co_occurrence` keyed by pairs is not JSON-serialisable**, and the first real run died on
`TypeError: keys must be str … not tuple`. Rendered as a list of `{"pair": [...], "count": n}`.

**The test that should have caught it was vacuous.** It read
`assert pairs[k] == 3 if isinstance(pairs, dict) else True` — which is `True` whenever the guard is
false, so it passed by not testing. *A conditional inside an assertion can make a test pass by
declining to run.* Replaced with an explicit round-trip test.

## Dependencies

Slices 01 and 02 — the region must exist and coexist before anything is written beside it.

## Effort · reference class

≤1 day. Reference class: `groom-issues` slice 04 / `/phil:groom-ask` — present, offer, write only what
was sanctioned, label the provenance. Its 2026-08-14 scribe→editor amendment is the directly reusable
prior art, including the finding that an *unlabelled* field rather than a *drafted* one is the defect.

## Taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one question form, one writer, one report line |
| Depends on a new abstraction? | Reuses 01's probe and 02's placement |
| Disproves a pre-commitment? | Yes — that the human half is answerable from evidence |
| Synthetic data? | No — this repo's real labels and their real co-occurrence |
| Identical to another slice but for scale? | No |
