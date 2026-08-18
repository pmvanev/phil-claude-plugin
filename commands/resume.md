---
description: "Pick the work back up: read the resume point, state up front whether it is still current or stale against the tree, say whether the board agrees about what is in flight, and only then present what was decided, the diversion stack you were inside, and what to do next. With no resume point, reconstructs the position from the artifacts that own it and says that is what it did."
mutates: true
allowed-tools: Read, Glob, Grep, Bash(git rev-parse:*), Bash(git status:*), Bash(git rev-list:*), Bash(git log:*), Bash(gh api graphql:*), Skill
---

Load the `session-handoff` skill at `${CLAUDE_PLUGIN_ROOT}/skills/session-handoff/SKILL.md`. Follow the BOOTSTRAP path; the
snapshot format, the deriving rules, the decision outcomes, and the never-do list govern all three paths.

**This command writes nothing — not to the repository, and not to the board.** It has no `Write`, no
`Edit` and no bare `Bash`. Its `git` grants are scoped to read-only subcommands, and its one remaining
verb, `gh api graphql`, is used for **board reads only**: reading the project's items and their Status
so the snapshot's next action can be compared against what the board says is in flight.

**It declares `mutates: true` because that verb can carry a mutation, not because this command does.**
`mutates` is a claim about the grant, which is the half a script can verify; the intent lives here and
in the skill's never-do list, which forbids moving a card, setting a Status, or posting a comment on
either path. This is the `adversarial-review` pattern `CLAUDE.md` documents.

The honest trade, stated so nobody discovers it later: this command's read-only guarantee used to be
**enforced** by its tool list and is now **declared**. No `gh` verb both reads Projects v2 reliably and
lacks a writing mode — `gh project item-list` is read-only but can under-report, and an under-report in
a divergence detector is a missed divergence. Sanctioned 2026-08-17 while building issue #24.
