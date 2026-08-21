# `skills/shared/` — shared reference material, not a skill

This directory deliberately contains **no `SKILL.md`**, so skill auto-discovery skips it. That is
correct, not broken: nothing here is invoked on its own.

The files here are fragments that several skills load by path, so the guidance lives once instead of
being restated — and drifting — in each consumer.

| File | Loaded by |
|---|---|
| `test-runner-detection.md` | `adversarial-review`, `redesign-tests`, `refactor-loop`, `refactor-tests` |
| `decision-request.md` | `groom-issues` |

**This table is hand-maintained and has drifted.** On 2026-08-21 it named `work` and `edd` as loaders
of `test-runner-detection.md` — neither references it — and omitted `adversarial-review` and
`refactor-loop`, which do. The fragment's own header disagreed with both, naming `refactor`. Three
registries, three answers, one truth. `tests/test_shared_fragment_registry.py` now derives the
loaders and fails on disagreement, so the table is checked rather than trusted.

Reference these from a skill by absolute plugin path, so resolution does not depend on the invoking
session's working directory:

```
${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md
```

Adding a `SKILL.md` here would be a mistake — it would register a skill that has no standalone
purpose and could be triggered on its own.
