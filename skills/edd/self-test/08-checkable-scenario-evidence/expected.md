# Expected outcome — fixture 08 (scenario evidence for a checkable expectation)

The developer did not opt out. The expectation is checkable, and nwave's acceptance test proves it —
but under edd-article-alignment D1 the developer still sees the scenario itself.

**Pins:** edd-article-alignment slice 01, AC2.1 — *"Given checkable expectations and no opt-out, when
evidence runs, then each gets a scenario's inputs and verbatim output from the non-builder producer,
with its reproduce command."*

**Expected decision:** `GATE-COMMISSION`. The tool dispatches `phil:edd-evidence-producer`, a
different agent from the nwave crafter that built, and presents:
- the scenario's inputs (two records, an empty `./out`);
- the verbatim output, including the `ls` showing nothing was written;
- the reproduce command.

It runs no acceptance check of its own: the engine's oracle verdict stands, and the evidence shows the
developer the behaviour behind it.

**Gate failure (blocks the skill change):** the checkable expectation skips evidence without an
opt-out; the evidence omits its inputs or paraphrases the output; or the producer is the builder.
