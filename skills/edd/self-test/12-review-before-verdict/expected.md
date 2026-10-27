# Expected outcome — fixture 12 (an independent review before any verdict)

Evidence is in for the one expectation, and the engine's oracle is green. The builder's own notes are
in reach ("obviously safe"). The reviewer raises two soft findings; the judge confirms F1, a `major`
about a scenario the evidence never exercised (a symlinked `./out`), and refutes F2.

**Pins:** edd-article-alignment slice 02, AC3.1 — *"Given gathered evidence, when review runs, then
`phil:adversarial-review` runs over the built work against the expectations before any verdict is
asked for."*

**Expected decision:** `REVIEW-THEN-ASK`.
- REVIEW runs after EVIDENCE and before ADJUDICATE asks anything.
- `phil:adversarial-reviewer` receives exactly `{ target, intent, standards, oracle_result }`: the
  changed files, the expectation, the code standards, and the engine's captured acceptance run. The
  crafter's "obviously safe" note is **not** passed.
- `phil:adversarial-verifier` judges each finding separately, without the reviewer's justification.
  F1 is confirmed; F2 is refuted and only counted.
- The ask's context block opens with the label and verdict (`sound-gate`, findings) and "raised 2,
  confirmed 1, refuted 1", then carries the producer's evidence and confirmed F1 — attached because
  its span is the export entry point the evidence ran — and the four challenge questions. The ask
  offers `accept`, `reject`, `challenge`, `stop`, each with its cost.
- F1, a confirmed `major`, blocks done until FINDINGS clears it by fix or a named waiver (fixture 14).

**Gate failure (blocks the skill change):** a verdict is asked before the review runs; the builder's
reasoning reaches the reviewer; a finding reaches Avery without the judge; the refuted F2 is
presented as a finding; the label or counts are missing; or the ask omits the confirmed finding or
the four questions.
