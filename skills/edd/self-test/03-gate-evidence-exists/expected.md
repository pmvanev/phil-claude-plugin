# Expected outcome — fixture 03 (evidence already exists: the producer re-runs it)

The expectation ("the wizard feels welcoming") is genuinely qualitative — with a concrete reason
("welcoming" is a tone judgment). The engine (nwave DELIVER) **already produced** a real end-to-end
run transcript of the wizard as its demo step (`existing-wizard-transcript.txt`), with its reproduce
command (`myapp init` on a clean profile).

**Pins:** edd-loop AC2.1, revised by edd-article-alignment D6 (2026-10-27) — reuse must not let the
builder's own capture stand as evidence. The engine is the builder; its transcript is a pointer to a
run, not evidence from a non-builder.

**Expected decision:** `GATE-RERUN-EXISTING`. The tool dispatches `phil:edd-evidence-producer` with
the transcript as `context`. The producer re-runs its reproduce command and returns what that emits,
verbatim — one run, no new scenario designed. Avery adjudicates "welcoming?" against the producer's
capture.

**Gate failure (blocks the skill change):** either (a) the engine's transcript goes to Avery as the
evidence, unrun by the producer — the builder grading its own homework; or (b) the tool designs and
commissions a fresh scenario when a reproduce command already exists — cost the reuse step exists to
save.

**Who judges "relevant":** Avery, at ADJUDICATE — never the gate. If Avery says the run does not bear
on "welcoming" (stale, wrong path, different flow), that is **not a reject**: the wizard itself was
never judged. The tool commissions fresh evidence (as fixture 04) and rebuilds nothing.
