# Expected outcome — fixture 03 (WALKING SKELETON: approve → commit)

The happy path and the end-to-end proof for slice 01. Baseline green; `move.patch` is a
*correct* Extract Fixture — the two duplicated `cart = {...}` literals become one shared
`sample_cart` pytest fixture. The assertion set is byte-identical before and after; the suite
stays green.

**Pins:** AC2.1 (propose shows the diff, the named move, and a one-line rationale, and applies
nothing until approval) and AC2.2 (on approval: apply, re-run the suite, commit only if green).

**How the loop drives it — the full apply-then-review cycle (DD4 / ADR-002):**
1. Propose: surface the named move (`Extract Fixture/Helper`), the target span, and the
   one-line rationale. **No diff is printed in chat.**
2. Apply `move.patch` to the working tree.
3. Run the suite (sanity). It is green.
4. Pause: ask the developer to review the *uncommitted diff in their IDE* and answer the
   structured **approve / reject / skip / quit** prompt (AskUserQuestion).
5. Decision = **approve** (this fixture) → `git commit` (exactly one commit for this item).

**Expected gate outcome:** `COMMIT`. One commit containing only the `test_cart.py` change,
the suite green at commit time.

**Gate failure (blocks the skill change):** the tool commits before the human approves; prints
the diff into chat instead of pausing for IDE review; commits more than one item; or commits
while the suite is red.

> The `@walking_skeleton` scenario in `../acceptance.feature` is this fixture. It is the
> demo proof: a non-technical stakeholder can confirm "yes — it cleaned a test only after I
> said so, and only because the suite stayed green."
