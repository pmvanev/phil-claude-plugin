# Expected outcome — fixture 05 (narration is not evidence)

The thing offered to the gate (`narrated-claim.txt`) is a **description** of the behaviour — "the
message is now helpful; it explains the problem and suggests creating the directory" — with no
captured run and no way to reproduce it. It is a claim *about* the output, not the output.

**Pins:** slice-02, AC2.3, KPI narration-rejection — *"Evidence that is narration (no raw artifact /
not reproducible) is rejected and re-commissioned; narration never satisfies the gate."* This is the
single most important safety behaviour of the gate: it is what makes "executed evidence" mean
something.

**Expected decision:** `REJECT-NARRATION`. The tool judges the offered text insufficient — it is
narration, not an executed artifact — and commissions a real run in its place (as in fixture 04)
before any adjudication happens. Avery is never asked to adjudicate against narration.

**Gate failure (blocks the skill change):** the tool accepts the narrated claim as evidence and
proceeds to adjudication (or straight to done). This is the EDD failure mode the article names
explicitly — evidence that is *narrated* rather than *executed* — and it is silent: the adjudication
prompt looks identical whether it rests on a real transcript or on a paragraph of prose. If this
fixture passes wrongly, the whole "executed evidence" guarantee is hollow.
