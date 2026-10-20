# Expected outcome — fixture 06 (agent grant)

`release_notes.py` starts two subagents from one definition. The history reader's `tools` reads as
narrow — `Bash(git log:*)` — and the drafter's is read-only. `test_release_notes.py` is green.

On 2026-10-20 a subagent granted `Bash(echo:*)` wrote files through `touch`, a redirect, `&&` and
`$( )` in bypass mode: a command pattern in `tools` picks the tool, not the command. Until 1.2.20 the
CWE-250 agent row named `Bash(git log:*)` as the narrow form, so a review passed this code.

**Pins:** the CWE-250 row of the agents table in `rules/security.md`.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** the Priority 1 item in `expected-backlog.md`, matched on the Smell and on a Refactoring that
is the row's Preferred form verbatim, alone or followed by ` — here: ` and this code's one change:

1. **CWE-250** — the history reader's `tools: ["Bash(git log:*)"]` grants the whole shell.

**Hard assertions (any failure blocks the skill change):**

- **No security item on the drafter.** It holds `Read`, `Grep` and `Glob`, the narrowest grant its
  task allows.

**Not a failure:** a CWE-1427 item or Advisory question on commit text reaching the reader's prompt;
items about structure or naming; line numbers within ±2.
