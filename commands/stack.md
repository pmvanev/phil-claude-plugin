---
description: "Where am I, and why: push a diversion the moment you take it, show the trace at any depth, pop the innermost frame when you come back. Operates on the same snapshot /phil:handoff writes, without ending the session."
argument-hint: "[push \"<what>\" \"<why>\"] | [pop]"
mutates: true
allowed-tools: Read, Write, Bash(git rev-parse:*), Bash(git status:*), Bash(git hash-object:*), Bash(date:*), AskUserQuestion, Skill
---

Load the `session-handoff` skill at `${CLAUDE_PLUGIN_ROOT}/skills/session-handoff/SKILL.md`. Follow the STACK
path. The snapshot format, the compare-and-swap rule, the decision outcomes and the never-do list govern
this path exactly as they govern CAPTURE and BOOTSTRAP.

No argument shows the stack. `push` takes what is being entered and why it is being entered. `pop`
takes nothing and drops the innermost frame only.

There is no `Glob` or `Grep` grant: all verbs operate on one path resolved by `git rev-parse
--show-toplevel`, and a grant with nothing to use it on weakens the argument the rest of this file makes
for the grants that are here. `Bash(git status:*)` is present because creating a snapshot stamps `dirty:`.

**Bare `/phil:stack` writes nothing**, but the grant does not say so — `Write` is present because `push`
and `pop` need it, and `allowed-tools` cannot be scoped per verb. The read-only intent of the show verb
lives here and in the skill's never-do list; `mutates: true` is the honest declaration for the grant as
a whole.

**`git hash-object` is granted and is NOT on the read-only allowlist**, deliberately: `-w` writes the
object into the database. This command never passes it, but a verb with a writing mode has no place in
a list whose entries are promises. Checked by `scripts/check-readonly-commands.py`.

**Every write is whole-file, guarded by a compare-and-swap.** A push or pop that finds the snapshot
changed between read and write refuses and reports both hashes; it never merges, never retries and
never picks a winner. Resolving two live sessions is out of scope, inherited from `session-handoff`
slice 03.
