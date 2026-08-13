---
description: "Pick the work back up: read the resume point, state up front whether it is still current or stale against the tree, and only then present what was decided and what to do next. With no resume point, reconstructs the position from the artifacts that own it and says that is what it did."
mutates: false
allowed-tools: Read, Glob, Grep, Bash(git rev-parse:*), Bash(git status:*), Bash(git rev-list:*), Bash(git log:*), Skill
---

Load the `session-handoff` skill at `${CLAUDE_PLUGIN_ROOT}/skills/session-handoff/SKILL.md`. Follow the BOOTSTRAP path; the
snapshot format, the deriving rules, the decision outcomes, and the never-do list govern both paths.

This command never writes. It has no `Write` or `Edit`, and its `Bash` is scoped to read-only git
invocations, so the read-only guarantee is enforced rather than merely declared.
