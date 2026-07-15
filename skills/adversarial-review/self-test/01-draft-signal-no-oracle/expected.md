# Expected outcome — fixture 01 (walking skeleton: honest soft review of a no-oracle target)

The target is prose with no deterministic oracle. The reviewer must still deliver a real adversarial
critique — but label it honestly as a soft signal, not a verified gate.

**Pins:** US-1, AC1.1–AC1.3 (walking skeleton). This is the thinnest end-to-end proof: invoke →
independent review → typed, advisory, ranked, span-and-evidence verdict labeled `draft-signal`.

**Expected decision:** `DRAFT-SIGNAL`. The verdict:
- `overall_label: "draft-signal"` — no oracle backed the review (C4).
- `verdict: "findings"` with the two real weaknesses surfaced, **ranked worst-first**: the
  unenforced safety-rule claim (major — the skill asserts a guarantee nothing implements) above the
  vague "validate the input" step (minor — unclear but not a false guarantee).
- Every finding carries a `span` (the offending lines) and `evidence` (the intent/standard it
  violates). (C5)
- **No `done` / `not_done` / `approved` field anywhere** — advisory only (C3). The human decides.

**Checkable assertions (all must hold):**
1. `overall_label == "draft-signal"`.
2. Findings are ordered by severity worst-first; the unenforced-guarantee finding outranks the
   vague-step finding.
3. Each finding has a non-empty `span` and `evidence`.
4. The verdict contains no field or sentence adjudicating whether the task is done.

**Gate failure (blocks the skill change):** the verdict is labeled `sound-gate` with no oracle
(defeats C4 — see fixture 03); OR a finding is emitted with no span/evidence (C5); OR the reviewer
states the task passes/fails (C3); OR the real major weakness is buried below nits (anxiety B).
Each is silent — the review would read as thorough while being dishonest about its own standing.
