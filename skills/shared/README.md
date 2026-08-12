# `skills/shared/` — shared reference material, not a skill

This directory deliberately contains **no `SKILL.md`**, so skill auto-discovery skips it. That is
correct, not broken: nothing here is invoked on its own.

The files here are fragments that several skills load by path, so the guidance lives once instead of
being restated — and drifting — in each consumer.

| File | Loaded by |
|---|---|
| `test-runner-detection.md` | `refactor-tests`, `redesign-tests`, `work`, `edd` |

Reference these from a skill by absolute plugin path, so resolution does not depend on the invoking
session's working directory:

```
${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md
```

Adding a `SKILL.md` here would be a mistake — it would register a skill that has no standalone
purpose and could be triggered on its own.
