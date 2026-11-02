---
description: "Say whether a card is ready to close: every ask it received — its checklist, its Done-when items and this session's requests — with evidence a call verified or marked open, and whether the work landed, every pull request merged and main green. Writes nothing and never merges. To put a session down unfinished, use /phil:handoff instead."
argument-hint: "<issue-number>"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(git rev-parse:*), Bash(gh issue view:*), Bash(gh api graphql:*)
---

Load the `done` skill at `${CLAUDE_PLUGIN_ROOT}/skills/done/SKILL.md` and run its FIND, ACCOUNT, LANDED
and REPORT steps for the card `$ARGUMENTS` names. With no argument, ask for the issue number; never infer it
from the branch.

Read the repo from the forge line in the working tree's `CLAUDE.md`. With none, stop and name
`/phil:board-setup`. Pass `-R <owner/repo>` on every `gh issue` call, and the owner and repo as variables
to `gh api graphql`, which takes no `-R`.

**This command writes nothing, and never merges.** It declares `mutates: true` because the
`gh api graphql` grant accepts a mutation document; the skill's invariants forbid sending one, and no
tool boundary backs them. Send only `query` documents.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report, as the skill directs, and
leave every quoted ask in the developer's own words.

Report exactly one terminal outcome — `READY` or `NOT-READY` — with each report line that fires, and
`WROTE-NOTHING` on every run.
