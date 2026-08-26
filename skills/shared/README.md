# `skills/shared/` — shared reference material, not a skill

This directory deliberately contains **no `SKILL.md`**, so skill auto-discovery skips it. That is
correct, not broken: nothing here is invoked on its own.

The files here are fragments that several **consumers** load by path — skills, agents and commands
alike — so the guidance lives once instead of being restated, and drifting, in each of them.

| File | Consumers (derived) |
|---|---|
| `test-runner-detection.md` | `adversarial-review`, `agents/adversarial-reviewer`, `redesign-tests`, `refactor-loop`, `refactor-tests` |
| `decision-request.md` | `groom-issues` |

**This table was hand-maintained and drifted twice.** On 2026-08-21 it named `work` and `edd` as
loaders of `test-runner-detection.md` — neither references it — and omitted `adversarial-review` and
`refactor-loop`, which do. The fragment's own header disagreed with both. Corrected, and then the
correction was itself found short: it counted only skills, missing `agents/adversarial-reviewer`.

`tests/test_shared_fragment_registry.py` now derives this table across skills, agents, commands and
skills' `references/`, and fails on disagreement. It also asserts the **form** of every reference, not
just its presence — the first version matched a bare relative path and an absolute one equally, so six
broken references passed for free.

**The form is mandatory in a skill, agent or command BODY** — text a loader interpolates and a session
acts on. It does not bind prose *about* the fragments: a fixture register or a design document may write
the readable path, and the form check does not scan those directories. Stated because the next reader
would otherwise either "fix" those references or widen the check to flag them.

Reference these from a skill by absolute plugin path, so resolution does not depend on the invoking
session's working directory:

```
${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md
```

Adding a `SKILL.md` here would be a mistake — it would register a skill that has no standalone
purpose and could be triggered on its own.
