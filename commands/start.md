---
description: "Pick a card up: resolve a number, title or description to one open card, or file one in your words on a yes when nothing matches; refuse a closed card and ask before a card in Done or someone else's; claim it — In Progress, assigned to the signed-in account, read back — move into its worktree, describe what it asks and how anyone will know it is done, and recommend one route with its reason, launched only on a yes. A card already underway names /phil:resume."
argument-hint: "<issue number, URL, title or description>"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(git rev-parse:*), Bash(gh api graphql:*), Bash(gh issue create:*), Bash(gh project item-add:*), Bash(gh project item-edit:*), Bash(gh issue edit:*), Bash(git worktree list:*), Bash(git fetch:*), EnterWorktree, ExitWorktree
---

Load the `start` skill at `${CLAUDE_PLUGIN_ROOT}/skills/start/SKILL.md` and run its RESOLVE, CHECK,
CLAIM, WORKTREE, DESCRIBE, ROUTE and REPORT steps for the card `$ARGUMENTS` names. With no argument,
ask which card to start; never infer it from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, name
`/phil:board-setup` and report `CANNOT-RUN`. Pass `-R <owner/repo>` on every `gh issue` call, and pass
the owner and repo as variables to `gh api graphql`, which takes no `-R`.

**Write only the claim and the worktree before the launch**: a card filed on the developer's yes, its
board item, the Status and an assignee, each read back; a fetch of the default branch; and a worktree
Claude Code's worktree tool cuts. A launched route, inline included, writes under its own rules.

- Send only `query` documents through `gh api graphql`.
- Use `gh issue edit` only with `--add-assignee`, and `gh project item-edit` only to set the Status
  option; never pass `--remove-assignee` or `--clear`.
- Run `gh issue create` only for a card the developer said yes to filing, titled in their words.
- Run `git` only for `rev-parse`, `worktree list --porcelain` and `fetch origin <default>`.
- Cut a worktree only through `EnterWorktree`, and call `ExitWorktree` only with `keep`.

No tool boundary backs these limits.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the description and the report, as the
skill directs, and leave every quoted line of the card or of `CLAUDE.md` in its own words.

Launch the recommended route only on the developer's yes. Print the outcome tokens before the launch:
exactly one terminal outcome — `LAUNCHED`, `NOT-LAUNCHED`, `UNDERWAY`, `STOPPED`, `NO-MATCH`,
`REFUSED-CLOSED` or `CANNOT-RUN` — with each report line that fires, and `WROTE-NOTHING` on every run
that wrote nothing.
