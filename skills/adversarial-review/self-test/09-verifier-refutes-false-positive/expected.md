# Expected outcome — fixture 09 (the judge refutes a false positive)

The adversary over-reported — it flagged an empty-list crash, but the target guards that case three
lines above the cited span. This is the failure mode the third role exists to catch: a motivated
attacker's misread reaching the human as a "finding". The judge must go to the span itself, see the
guard, and refute.

**Pins:** the adversary→judge separation. This is why the tool is a triple, not a single
self-certifying critic — the judge raises precision by filtering the reviewer's noise.

**Expected decision:** `REFUTED`. The verifier:
- Reads `src/handler.py` at and around the span itself — not taking the finding's word.
- Finds the `if not items: return None` guard at line 17 that already handles the empty case.
- Sets `judgment: "refuted"`, `basis` quoting the guard line.

The orchestrator then **drops** this finding and counts it as refuted; it never reaches the human as
a confirmed finding.

**Checkable assertions (all must hold):**
1. `judgment == "refuted"`.
2. `basis` cites the actual guard (the thing the reviewer missed), not a bare denial.
3. The verifier's dispatch input did **not** contain the reviewer's justification/confidence — it
   reached the refutation independently.

**Gate failure (blocks the skill change):** the judge `confirms` the finding (rubber-stamps the
adversary's misread — the whole point of the separate judge is defeated), OR it refutes with no
`basis` (an empty denial is as useless as empty praise), OR it was handed the reviewer's reasoning
and merely agreed (independence broken — a correlated judge is not a judge).
