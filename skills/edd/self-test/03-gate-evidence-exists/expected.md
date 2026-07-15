# Expected outcome — fixture 03 (qualitative expectation, evidence already exists)

The expectation ("the wizard feels welcoming") is genuinely qualitative — with a concrete reason
("welcoming" is a tone judgment). But the engine (nwave DELIVER) **already produced** a real
end-to-end run transcript of the wizard as its demo step (`existing-wizard-transcript.txt`). That
transcript is exactly the executed evidence the gate needs.

**Pins:** slice-02, AC2.1 — *"When the engine already produced relevant executed evidence, the gate
points the human at it rather than commissioning new evidence."* This is the gate scaling toward
zero cost.

**Expected decision:** `GATE-POINT-EXISTING`. The tool points Avery at the existing captured
transcript, commissions **no** new evidence (no `edd-evidence-producer` run), and asks Avery to
adjudicate "welcoming?" against that real transcript.

**Gate failure (blocks the skill change):** the tool commissions a fresh evidence run when a
relevant executed artifact already exists. That is redundant ceremony — the scaled gate is supposed
to reuse what the engine already produced. (It is not a *safety* failure like accepting narration,
but it is the cost-inflation failure the "scales, not binary" design exists to prevent.)

**Who judges "relevant":** relevance is **Avery's adjudication call, not a gate check.** The gate's
job is to surface the available executed evidence and ask; if Avery decides the transcript does not
actually bear on "welcoming" (stale, wrong path, different flow), that is an adjudication **reject**
that iterates the expectation (→ commission fresh evidence, as fixture 04) — it is **not** a gate
failure. The gate never tries to decide relevance on Avery's behalf.
