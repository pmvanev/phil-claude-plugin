---
description: "Check that a card's every ask landed and its pull requests merged into a green default branch, then, on one yes, comment, set Status to Done and close it. Never merges. For unfinished work, use /phil:handoff."
argument-hint: "<issue-number>"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(git rev-parse:*), Bash(git log:*), Bash(ls:*), Bash(gh issue view:*), Bash(gh api graphql:*), Bash(gh issue comment:*), Bash(gh project item-edit:*), Bash(gh issue close:*), Bash(gh issue edit:*)
---

Load the `done` skill at `${CLAUDE_PLUGIN_ROOT}/skills/done/SKILL.md` and run its FIND, ACCOUNT, LANDED,
REPORT, RESOLVE, PLAN and CLOSE steps for the card `$ARGUMENTS` names. With no argument, ask for the issue
number; never infer it from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, stop and
name `/phil:board-setup`. Pass `-R <owner/repo>` on every `gh issue` call, and the owner and repo as
variables to `gh api graphql`, which takes no `-R`.

**Write nothing before the developer's one yes, and never merge.** After the yes, write only the closing
comment, the Status, the close and the generated block's refresh, in that order, and stop at the first
that fails. Send only `query` documents through `gh api graphql`. Use `gh issue edit` only with
`--body-file`, and only inside the block refresh; use `git log` and `ls` only for that refresh's reads.
No tool boundary backs these limits.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report and the closing comment, as the
skill directs, and leave every quoted ask in the developer's own words.

Report exactly one terminal outcome — `NOT-READY`, `STOPPED`, `CLOSED` or `CLOSE-FAILED` — with each
report line that fires, and `WROTE-NOTHING` on every run that wrote nothing.
