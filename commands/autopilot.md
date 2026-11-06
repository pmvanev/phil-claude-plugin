---
description: "Carry a card through its repo's build path, on GitHub or GitLab: claim it through /phil:start's steps, read and record the build path, then run each step through the command that owns it — answering questions by recorded rule or recommendation, recording each step's decisions on the card, and stopping only for a blocker, described on the card and handed off. --plan stops before the first step. Lands nothing yet, and never calls a card done."
argument-hint: "<issue number, URL, title or description> [--plan] [answer to a standing blocker]"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(git rev-parse:*), Bash(git worktree list:*), Bash(git fetch:*), Bash(gh api graphql:*), Bash(gh project item-add:*), Bash(gh project item-edit:*), Bash(gh issue edit:*), Bash(gh issue comment:*), Bash(glab api:*), Bash(jq:*), Bash(glab issue update:*), Bash(glab issue note:*), EnterWorktree, ExitWorktree
---

Load the `autopilot` skill at `${CLAUDE_PLUGIN_ROOT}/skills/autopilot/SKILL.md` and run its CLAIM, PATH,
RECORD, RUN and REPORT steps for the card `$ARGUMENTS` names. With no argument, ask which card to carry;
never infer it from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, name
`/phil:board-setup` and report `CANNOT-RUN`. Pass `-R <owner/repo>` on every `gh issue` call, and pass
the owner and repo as variables to `gh api graphql`, which takes no `-R`. On GitLab, follow
`/phil:start`'s `references/gitlab.md` and the skill's `references/record.md`: pass
`-R https://<host>/<group/project>` on every `glab issue` call and `--hostname <host>` on every
`glab api` call.

The grant covers autopilot's own calls: the claim, the worktree, the comments on the card, and launching
each step's command or skill and `/phil:handoff`. The work a step does — editing, testing, committing,
launching an agent — runs under the session's own permissions, and a call the session denies is a
blocker.

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
- Push nothing, open no pull or merge request, and merge nothing: this release lands nothing.
- In autopilot's own calls, run `git` only as `rev-parse`, `worktree list --porcelain` and
  `fetch origin <default>`; a step's commits run under the session's permissions.
- Cut a worktree only through `EnterWorktree`, and call `ExitWorktree` only with `keep`.

No tool boundary backs these limits.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing a comment or the report, as the skill
directs, and leave every quoted line of `CLAUDE.md`, `AGENTS.md` or the card in its own words.

Print exactly one terminal outcome — `PLANNED`, `CARRIED`, `BLOCKED`, `STOPPED`, `NO-MATCH`,
`REFUSED-CLOSED` or `CANNOT-RUN` — with each report line that fires, and `WROTE-NOTHING` on every run
that wrote nothing.
