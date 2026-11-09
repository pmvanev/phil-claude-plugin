---
description: "Check that a card's every ask landed and its pull requests merged into a green default branch, then, on one yes, comment, set Status to Done, close it, retire its snapshots, delete its branches and remove its clean, unlocked worktrees, whoever made them. With no card, check the session's own work and clear what it left. GitHub or GitLab. Never merges or forces. For unfinished work, use /phil:handoff."
argument-hint: "[issue-number]"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(git rev-parse:*), Bash(git log:*), Bash(ls:*), Bash(gh issue view:*), Bash(gh api graphql:*), Bash(gh issue comment:*), Bash(gh project item-edit:*), Bash(gh issue close:*), Bash(gh issue edit:*), Bash(glab api:*), Bash(jq:*), Bash(glab issue note:*), Bash(glab issue update:*), Bash(glab issue close:*), Bash(git worktree list:*), Bash(git worktree remove:*), ExitWorktree, Bash(git branch -d:*), Bash(git branch -D:*), Bash(git merge-base:*), Bash(git rev-list --count:*), Bash(git push --delete:*), Bash(git remote get-url:*), Bash(python3:*)
---

Load the `done` skill at `${CLAUDE_PLUGIN_ROOT}/skills/done/SKILL.md` and run its FIND, ACCOUNT, LANDED,
REPORT, RESOLVE, PLAN and CLOSE steps for the card `$ARGUMENTS` names. With no argument, run without a
card, as the skill's `references/no-card.md` directs: check the session's own work, and never infer a card
from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, stop and
name `/phil:board-setup`. Pass `-R <owner/repo>` on every `gh issue` call, and the owner and repo as
variables to `gh api graphql`, which takes no `-R`. On GitLab, follow the skill's `references/gitlab.md`:
Pass `-R https://<host>/<group/project>` on every `glab issue` call and `--hostname <host>` on every
`glab api` call.

**Write nothing before the developer's one yes, and never merge.** After the yes, write only the closing
comment, the Status, the close, the generated block's refresh and the cleanup, in that order. Stop at the
first close write that fails; a refusal during the cleanup leaves that item and goes on.

- Send only `query` documents through `gh api graphql`.
- Send `glab api` only GETs: never `-f`, `-F`, `--field`, `--raw-field`, `--input`, `--form`, `-X` or
  `--method`. Pipe `jq` only from it.
- Use `glab issue update` only with `--unlabel` for the status labels, or with `--description`.
- Use `gh issue edit --body-file` and `glab issue update --description` only inside the block refresh.
- Use `git log` and `ls` only for the refresh's reads and FORCE's list of the commits a delete would lose.
- Use `git rev-list --count` only to count the commits from a snapshot's recorded commit to `HEAD`,
  where that commit is an ancestor of `HEAD`.
- Pass `--output` to no git command: it writes a file from `log` and `rev-list`.
- Remove only a worktree on the work's own merged branch that `worktree-state.py --expect-head` reads
  `CLEAN` at the merged tip, whoever made it, never with `--force`, and never one another session locks:
  only `EnterWorktree`'s lock on this session's worktree is no bar. List every other worktree with its
  commands. Remove the one this session runs in last:
  through `ExitWorktree` where `EnterWorktree` made it in this session, otherwise through
  `git worktree remove`, and, where it holds a snapshot, only on the third answer.
- Pass `discard_changes: true` to `ExitWorktree` only where that read came back `CLEAN`, just before
  the call.
- Never pass `--force` or `-f`. Pass `-D` only for a branch the developer chose to force-delete at its own
  question. The one force-family flag allowed is the remote delete's `--force-with-lease=<ref>:<oid>`.
- Run `python3` only on `${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py` with `head` or `retire`, and
  on `${CLAUDE_PLUGIN_ROOT}/scripts/worktree-state.py`.

No tool boundary backs these limits.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the report and the closing comment, as the
skill directs, and leave every quoted ask in the developer's own words.

Report exactly one terminal outcome — `NOT-READY`, `STOPPED`, `CLOSED`, `CLOSE-FAILED` or `FINISHED` —
with each report line that fires, and `WROTE-NOTHING` on every run that wrote nothing.
