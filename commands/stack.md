---
description: "Where am I, and why: push a diversion the moment you take it, show the trace at any depth, pop the innermost frame when you come back. Operates on the same snapshot /phil:handoff writes, without ending the session."
argument-hint: "[push \"<what>\" \"<why>\"] | [pop]"
mutates: true
allowed-tools: Read, Bash(git rev-parse:*), Bash(git status:*), Bash(date:*), Bash(python3:*), AskUserQuestion, Skill
---

Load the `session-handoff` skill at `${CLAUDE_PLUGIN_ROOT}/skills/session-handoff/SKILL.md`. Follow the STACK
path. The snapshot format, the compare-and-swap rule, the decision outcomes and the never-do list govern
this path exactly as they govern CAPTURE and BOOTSTRAP.

No argument shows the stack. `push` takes what is being entered and why it is being entered. `pop`
takes nothing and drops the innermost frame only.

There is no `Glob` or `Grep` grant: all verbs operate on one path resolved by `git rev-parse
--show-toplevel`, and a grant with nothing to use it on weakens the argument the rest of this file makes
for the grants that are here. `Bash(git status:*)` is present because creating a snapshot stamps `dirty:`.

**Bare `/phil:stack` writes nothing**, but the grant does not say so — `Bash(python3:*)` is present
because `push` and `pop` write through it, and `allowed-tools` cannot be scoped per verb. The read-only
intent of the show verb lives here and in the skill's never-do list; `mutates: true` is the honest
declaration for the grant as a whole.

**There is no `Write` and no `git hash-object`, and both absences are deliberate.** Every read and write
of the snapshot goes through `session-exchanges.py`, which hashes the bytes itself: the Write tool
refuses to overwrite a file it has not Read whole — which would pull a previous session's replies into
context — and `git hash-object` applies line-ending filters that can make its hash disagree with the
script's.

**Every write is whole-file, guarded by a compare-and-swap.** A push or pop that finds the snapshot
changed between read and write refuses and reports both hashes; it never merges, never retries and
never picks a winner. Resolving two live sessions is out of scope, inherited from `session-handoff`
slice 03.

**The session regenerates the body and never the exchanges region beneath it.** That region holds a
previous session's words, and retyping them is what Anthropic's safety classifier refuses. So a push or
pop reads around it and writes back through the script, which keeps it byte-for-byte:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py head  --file <root>/.session-handoff.md
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py carry --file <root>/.session-handoff.md --expect-sha <h1|absent> --body - <<'SESSION_HANDOFF_BODY'
<the regenerated body>
SESSION_HANDOFF_BODY
```

**`Bash(python3:*)` is wider than its intent, and the prose is the control.** A `Bash(...)` grant may not
carry a path, so the interpreter is granted and the path lives in the invocation above — the
`adversarial-review` pattern in this repo's `CLAUDE.md`, and the one `board-setup` states for its own two
scripts. The grant permits any Python, including a file write or shell redirection; the intent is this
one script, carried here and in the skill's never-do list. It replaces a grant of `Write`, which was no
narrower: it could overwrite any file.
