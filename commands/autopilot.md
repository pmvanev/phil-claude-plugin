---
description: "Carry a card through its repo's build path, on GitHub or GitLab: claim it, read and record the build path, run each step through the command that owns it, and land the work on a green pipeline — deciding questions by rule or recommendation, recording each step's decisions on the card, and stopping only for a blocker, described and handed off. --plan stops before the first step. Never calls a card done."
argument-hint: "<issue number, URL, title or description> [--plan] [answer to a standing blocker]"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(git rev-parse:*), Bash(git worktree list:*), Bash(git fetch:*), Bash(gh api graphql:*), Bash(gh project item-add:*), Bash(gh project item-edit:*), Bash(gh issue edit:*), Bash(gh issue comment:*), Bash(git push:*), Bash(gh pr create:*), Bash(gh pr checks:*), Bash(gh pr merge:*), Bash(gh run list:*), Bash(gh run watch:*), Bash(glab api:*), Bash(jq:*), Bash(glab issue update:*), Bash(glab issue note:*), Bash(glab mr create:*), Bash(glab mr merge:*), Bash(glab ci status:*), EnterWorktree, ExitWorktree
---

Load the `autopilot` skill at `${CLAUDE_PLUGIN_ROOT}/skills/autopilot/SKILL.md` and run its CLAIM, PATH,
RECORD, RUN and REPORT steps for the card `$ARGUMENTS` names. With no argument, ask which card to carry;
never infer it from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, name
`/phil:board-setup` and report `CANNOT-RUN`. Pass `-R <owner/repo>` on every `gh issue` call, and pass
the owner and repo as variables to `gh api graphql`, which takes no `-R`. On GitLab, follow
`/phil:start`'s `references/gitlab.md` and the skill's references: pass
`-R https://<host>/<group/project>` on every `glab` call that takes a repo and `--hostname <host>` on
every `glab api` call.

The grant covers autopilot's own calls: the claim, the worktree, the comments on the card, the landing
— push, request, wait, merge — and launching each step's command or skill and `/phil:handoff`. The work
a step does — editing, testing, committing, launching an agent, walking a change in a browser — runs
under the session's own permissions, and a call the session denies is a blocker.

- Send only `query` documents through `gh api graphql`.
- Send `glab api` only GETs: never `-f`, `-F`, `--field`, `--raw-field`, `--input`, `--form`, `-X` or
  `--method`. Pipe `jq` only from it.
- Use `gh issue edit` only with `--add-assignee`, and `gh project item-edit` only to set the
  Status option; never pass `--remove-assignee` or `--clear`.
- Use `glab issue update` only with `--label` and `--unlabel` for the status labels, or with
  `--assignee +<login>`; a login without the `+` replaces every assignee.
- Use `gh issue comment` only with `-R` and `--body-file -`, and `glab issue note` only with `-R` and
  `--message`; never `--edit-last` or `--delete-last`.
- File no card, run no `/phil:done`, and close no card: done is the developer's, after inspecting.
- Land as the skill's `references/land.md` says: push without `--force`, name the card in the
  request as `issue <n>`, and merge only on a pipeline the forge reports green, with
  `--match-head-commit` or `--sha`; never `--admin` or `--auto`, always `--auto-merge=false` on
  GitLab, and never `--delete-branch` or `--remove-source-branch` without `=false`.
- In autopilot's own calls, run `git` only as `rev-parse`, `worktree list --porcelain`,
  `fetch origin <default>` and `push -u origin <branch>`; a step's commits run under the session's
  permissions.
- Cut a worktree only through `EnterWorktree`, and call `ExitWorktree` only with `keep`.

No tool boundary backs these limits.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing a comment or the report, as the skill
directs, and leave every quoted line of `CLAUDE.md`, `AGENTS.md` or the card in its own words.

Print exactly one terminal outcome — `PLANNED`, `CARRIED`, `BLOCKED`, `STOPPED`, `NO-MATCH`,
`REFUSED-CLOSED` or `CANNOT-RUN` — with each report line that fires, and `WROTE-NOTHING` on every run
that wrote nothing.
