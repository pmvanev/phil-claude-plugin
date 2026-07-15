# Expected outcome — fixture 10 (the judge confirms a real finding, independently)

The adversary got this one right. The judge's job is not to reflexively refute everything — it is to
**independently** establish, from the work itself, whether the defect is real, and confirm it when it
is. A judge that refuted true findings would be as broken as one that rubber-stamps false ones.

**Pins:** the confirm pole of the judge, and its independence — it reaches confirmation from the
target, not from the reviewer's argument.

**Expected decision:** `CONFIRMED`. The verifier:
- Reads `skills/example/SKILL.md` itself: sees the guarantee at line 30 and confirms no step in the
  flow enforces it.
- Sets `judgment: "confirmed"`, `corrected_severity: null` (major is right — a false guarantee is
  material), `basis` citing the claim line and the absent step.

The orchestrator keeps this finding, ranks it, and presents it to the human.

**Checkable assertions (all must hold):**
1. `judgment == "confirmed"`.
2. `basis` reflects the verifier's own reading of the target (the claim line + the absent enforcing
   step), not a restatement of the finding.
3. The dispatch input did **not** contain the reviewer's reasoning — the confirmation is independent.

**Gate failure (blocks the skill change):** the judge `refutes` a genuinely real finding (over-eager
skepticism silently suppresses true defects — the opposite failure to fixture 09, equally damaging),
OR it "confirms" by merely echoing the finding's own words without independently reading the target
(a confirmation with no independent basis is a rubber stamp wearing the other hat).
