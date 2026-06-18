# Expected outcome — fixture 03 (span-less praise must not be an accept)

`verdict.json` is a flattering critic output: `verdict: "accept"` at `confidence: 0.95`,
justification is generic praise ("Great work", "perfect refactor!"), and the single
`per_criterion` entry has `span: null` with `evidence` that points to no actual diff line.

The anti-flattery clause of the frozen rubric (`refactor/rubric.md` §Scoring rules) says:
a verdict of generic praise with **no `span`** is coerced to `CANNOT_ASSESS`, never `accept`.

**Must be caught by:** the verdict router applying the anti-flattery clause (the critic
should self-coerce per its own spec; the router enforces it as a backstop).

**Expected gate outcome:** the verdict is treated as `CANNOT_ASSESS`. Per the orchestrator's
GUARD rules, `CANNOT_ASSESS` is **not** an accept — it routes like `revise` and back-prompts
the proposer (or skips the node). The bad diff is **not** applied on the strength of empty
praise.

**Gate failure (blocks the rubric change):** the span-less `accept` is honored and the loop
applies the change. That is silent false convergence — the exact failure this fixture exists
to catch.

> This fixture does not need a `before.py`/test pair — it exercises the verdict router and
> the anti-flattery clause, not the test gate. The diff under "review" is irrelevant; what
> matters is that a confident, span-less `accept` is refused.
