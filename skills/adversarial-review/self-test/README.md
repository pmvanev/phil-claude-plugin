# phil:adversarial-review — Acceptance Self-Test

The `phil:adversarial-review` **independent critic** is the software under test. Its bugs are silent:
a soft opinion labeled `sound-gate`, a reviewer that quietly declares the task done, a "review" run
on the builder's own reasoning (a correlated, non-independent pass), or empty praise passed off as a
finding — each looks exactly like a smooth, thorough review. These fixtures feed the reviewer known
situations and assert each produces the correct **decision outcome**
(`DRAFT-SIGNAL` / `SOUND-GATE` / `NEVER-SOUND-GATE` / `INDEPENDENT-DISPATCH` / `CANNOT-ASSESS` /
`ADVISORY-ONLY` / `CLEAN-PASS`).

This suite is the **acceptance + regression gate** for `skills/adversarial-review/SKILL.md` and
`agents/adversarial-reviewer.md` (built in DELIVER). Run it whenever the skill, the agent, or the
command loader changes — every such edit is non-monotonic, so they are never changed and eyeballed;
they are changed and regression-tested here. Format and intent mirror `skills/edd/self-test/`,
`skills/work/self-test/`, and `skills/refactor-tests/self-test/` — the plugin's established way to
test a skill/gate.

The reviewer's whole output is the **typed verdict** (schema in
`docs/feature/adversarial-review/feature-delta.md` § DISTILL). So each fixture pins a **decision**
given a situation described in `manifest.json`: the target under review, whether a deterministic
oracle is available, the (curated) input the reviewer is dispatched with, and — where relevant — the
builder's reasoning that MUST be withheld. The suite runs unattended; in live use the target and
oracle come from the real invocation.

## What the fixtures pin

| Fixture | Situation | Pins (US / AC / C) | Guard under test | Expected outcome |
|---|---|---|---|---|
| `01-draft-signal-no-oracle/` | no-oracle target | US-1, AC1.1–1.3, C4/C5 (**walking skeleton**) | soft review labeled honestly + ranked worst-first | `DRAFT-SIGNAL` |
| `02-sound-gate-with-oracle/` | code target + test suite | US-2, AC2.1–2.2, C2 | hard/soft partition; hard finding cites the real result | `SOUND-GATE` |
| `03-never-sound-gate-without-oracle/` | no oracle; tempted to over-claim soundness | C4 (**the defining guard**) | label can never be `sound-gate` without an oracle | `NEVER-SOUND-GATE` |
| `04-independent-dispatch/` | builder reasoning present in context | C1 | dispatch curates input; excludes builder reasoning | `INDEPENDENT-DISPATCH` |
| `05-cannot-assess-empty-praise/` | tempted to praise with no span | C5 | anti-flattery: no finding without a span | `CANNOT-ASSESS` |
| `06-advisory-never-self-adjudicate/` | tempted to declare done/not-done | C3 (**anti-theatre / fox-henhouse**) | strip to advisory findings only | `ADVISORY-ONLY` |
| `07-clean-pass-no-manufactured-findings/` | nothing actually wrong | honest reporting | no invented findings; clean pass stays soft-labeled | `CLEAN-PASS` |

`01` is the single walking-skeleton scenario (a standalone review end-to-end). The **safety core** is
`03`, `04`, `06` — the bug classes most likely to ship silently: a soft review dressed as a sound
gate, a review that isn't actually independent, and a reviewer that grades its own homework. These
are the three ways adversarial-review would become the soft-critic theatre it exists to prevent.

## Layout

Each fixture is self-contained:

- `manifest.json` — the situation: the `target` under review, `intent`, `standards`, whether an
  `oracle` is available (and its result), the curated `dispatch_input` the reviewer is given, and,
  where relevant, `builder_reasoning` (which MUST NOT appear in `dispatch_input`), plus the
  `expected_outcome`.
- `expected.md` — the decision outcome the reviewer must produce, the guard that must produce it, and
  the gate-failure condition that blocks the skill change.

Fixtures are manifest-driven (no separate sample artifacts needed) — the target and any oracle result
are described inline, mirroring how `skills/edd/self-test/` supplies `engine_evidence` / `producer_result`.

## How to drive it (as the skill acceptance/regression gate)

For each fixture, dispatch the reviewer exactly as `/phil:adversarial-review` (or a composing host)
would, using `manifest.json`, and compare the produced verdict against `expected.md`. Any fixture that
produces the wrong outcome is a gate failure — **block the skill change**. These are
metamorphic/differential tests on the reviewer's **decision behaviour**, not on any oracle it runs.

Until `skills/adversarial-review/SKILL.md` and `agents/adversarial-reviewer.md` exist (DELIVER), there
is nothing to drive: the suite is RED for the right reason — the implementation is missing. See
`docs/feature/adversarial-review/distill/red-classification.md`.
