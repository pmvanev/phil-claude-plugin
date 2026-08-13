# Global Development Standards

Development and writing standards live in `${CLAUDE_PLUGIN_ROOT}/rules/`. Rules load automatically based on the files you touch — no manual reading required.

## Key Principles (always apply)

- **Test first.** Write a failing test before production code.
- **Separate structure from behavior.** Refactoring commits and behavior-change commits are separate.
- **Dependencies point inward.** Business rules never import infrastructure.
- **Make every word tell.** Active voice, no needless words, clear on first read.
- **Empirical design over speculation.** Solve for what is really there, not imagined futures.

## Resuming work

**Starting a session to continue existing work? Run `/phil:resume` before anything else.** It reads
the session snapshot (`.session-handoff.md`, git-ignored and machine-local) and states up front
whether it is current or stale against the tree, then names the command that owns the work without
running it. With no snapshot it reconstructs from the artifacts and says that is what it did.

Put a session down with `/phil:handoff`. It records only what a fresh session cannot derive — the
decisions, the approaches ruled out, the intended next action — and refuses to copy anything the
artifacts already own.

## Issue board

- Forge: GitHub — pass `-R pmvanev/phil-claude-plugin` on every `gh` call. Issue #12 exists in every
  repo, so an inferred remote mutates the wrong one successfully.
- Board: user project 3, `phil plugin`. The kanban is view 2 —
  https://github.com/users/pmvanev/projects/3/views/2 (view 1 is the table).
- Status is a project **field**, not a label. An issue must be `gh project item-add`ed before any
  field can be set; editing one that was never added does nothing.
- IDs: project `PVT_kwHOANPp-M4Bf-px` · Status field `PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs` · options
  Todo `f75ad846`, In Progress `47fc9ee4`, Done `98236657`.
- **Auto-close on Done is ENABLED.** Setting Status=Done closes the issue; a `gh issue close -c`
  afterwards reports "already closed" and **silently drops the comment**. Post the closing
  comment first, then set Status. Moving Done→Todo does not reopen — use `gh issue reopen`.
- `gh auth` needs the `project` scope — present as of 2026-08-12; `gh auth refresh -s project` if it
  is lost.
- Read the board with `gh api graphql`, never `gh project item-list` — item-list served a stale
  title for #10 on 2026-08-12 and can under-report. GraphQL returns items in board-position order,
  and that order is authoritative: the top Todo card is what to work on next.
- Docs root for absolute links (GitHub emits relative paths verbatim and they 404):
  `https://github.com/pmvanev/phil-claude-plugin/blob/main/`
- Forge mechanics: `phil:issue-board`. nWave feature/slice/step mapping: `phil:nwave-issue-board`.
