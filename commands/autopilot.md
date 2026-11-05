---
description: "Carry a card through its repo's build path. This release claims the card through /phil:start's steps, reads the build path from CLAUDE.md and AGENTS.md, prints each step beside the line it came from with the writes the path authorizes, records both on the card, and stops before the first step. GitHub only."
argument-hint: "<issue number, URL, title or description>"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Bash(git rev-parse:*), Bash(git worktree list:*), Bash(git fetch:*), Bash(gh api graphql:*), Bash(gh project item-add:*), Bash(gh project item-edit:*), Bash(gh issue edit:*), Bash(gh issue comment:*), EnterWorktree, ExitWorktree
---

Load the `autopilot` skill at `${CLAUDE_PLUGIN_ROOT}/skills/autopilot/SKILL.md` and run its CLAIM, PATH,
RECORD and REPORT steps for the card `$ARGUMENTS` names. With no argument, ask which card to carry; never
infer it from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, name `/phil:board-setup` and
report `CANNOT-RUN`. Where the forge line names GitLab, say the command covers GitHub only and report
`CANNOT-RUN` with `GITHUB-ONLY`. Pass `-R <owner/repo>` on every `gh issue` call, and pass the owner and
repo as variables to `gh api graphql`, which takes no `-R`.

**Stop before the first step of the path.** Write only `/phil:start`'s claim and worktree — its board item, Status and
assignee, each read back; a fetch of the default branch; a worktree Claude Code's worktree tool cuts —
and one path comment on the card.

- Send only `query` documents through `gh api graphql`.
- Use `gh issue edit` only with `--add-assignee`, and `gh project item-edit` only to set the
  Status option; never pass `--remove-assignee` or `--clear`.
- Use `gh issue comment` only with `-R` and `--body-file -`; never `--edit-last` or `--delete-last`.
- File no card.
- Run `git` only for `rev-parse`, `worktree list --porcelain` and `fetch origin <default>`.
- Cut a worktree only through `EnterWorktree`, and call `ExitWorktree` only with `keep`.

No tool boundary backs these limits.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the comment and the report, as the skill
directs, and leave every quoted line of `CLAUDE.md`, `AGENTS.md` or the card in its own words.

Print exactly one terminal outcome — `PLANNED`, `STOPPED`, `NO-MATCH`, `REFUSED-CLOSED` or `CANNOT-RUN`
— with each report line that fires, and `WROTE-NOTHING` on every run that wrote nothing.
