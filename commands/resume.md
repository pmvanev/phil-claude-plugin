---
description: "Pick the work back up: read the resume point, state up front whether it is still current or stale against the tree, say whether the board agrees about what is in flight, and only then present what was decided, the diversion stack you were inside, and what to do next. All of it in about 300 words of plain English — and where the verdict, the divergence and the stack cannot fit in that, it says the bound gave way rather than dropping any of them. With no resume point, reconstructs the position from the artifacts that own it and says that is what it did."
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

**The report is bounded at 300 words, and the verdict is not what gives ground.** The freshness verdict,
the board outcome with both named sides of a divergence, every stack frame with its staleness mark, the
next action and the owner route are all mandatory. Only the recorded decisions and ruled-out approaches
are withheld to fit, under `REPORT-CLIPPED` with a count; where the mandatory content alone exceeds the
bound the run prints it anyway and reports `CEILING-BREACHED`. Neither a silent clip nor a silent breach
is permitted. The skill owns the rules, under *The report has a ceiling; the record never does*.
