# Global Development Standards

Development and writing standards live in `${CLAUDE_PLUGIN_ROOT}/rules/`. Rules load automatically based on the files you touch — no manual reading required.

## Key Principles (always apply)

- **Test first.** Write a failing test before production code.
- **Separate structure from behavior.** Refactoring commits and behavior-change commits are separate.
- **Dependencies point inward.** Business rules never import infrastructure.
- **Make every word tell.** Active voice, no needless words, clear on first read.
- **Empirical design over speculation.** Solve for what is really there, not imagined futures.

## Build path for this plugin

This repo's product is a plugin — skills, commands, agents, rules. Two tools own the two halves, and
neither substitutes for the other:

- **Understand it with `nw-discuss`.** New feature, new skill, new command: run DISCUSS before
  authoring. It produces the persona, the JTBD, the locked decisions and the slice split that the
  `docs/feature/<name>/` artifacts then hold. Skip it and the slice brief is invented at authoring
  time by whoever is typing.
- **Author, review and vet with `plugin-dev`.** Consult `plugin-dev:skill-development`,
  `command-development`, `agent-development` or `plugin-structure` **before writing the file**, not
  after — they own the schema, the frontmatter fields and the layout. Then run
  `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` over the result. Neither is optional
  because a sibling file is a convenient template: copying the shape of an existing command
  propagates whatever that command got wrong and records nothing about whether it was checked.

DESIGN/DISTILL/DELIVER do **not** run here — the deliverable is prose, and this repo settled twice
that skills are authored rather than waved (`todo.md` 2026-06-17; edd-loop DDD8).

**Say in the commit which of the two ran.** Slice 03 of `groom-issues` was authored on 2026-08-13
from the slice brief and its sibling commands, with `plugin-dev` never loaded — a deviation from the
build path its own `feature-delta.md` declares, invisible afterwards because nothing records
compliance either way.

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
- **A closing keyword in a commit message closes the card *and* sets Status=Done.** It fires on the
  bare `#N` and the rest of the sentence is never read: `fixed #22's unlinked path` closed #22 on
  2026-08-13, in a commit whose subject was another issue's slice. Write `issue 22` or `the #22 body`
  whenever the commit is not the fix. Recovery is two steps, because **`gh issue reopen` restores the
  issue and not the field** — the card is left OPEN while sitting in Done, and no view flags that
  combination. Set Status back by hand, and check with the open-in-Done query below.
- Verify the two can't drift: an open issue in Done, or a closed one outside it, is always a defect.
  Compare `gh issue list --state open --json number` against the project's items and their Status —
  the same one call that reads the board already returns both halves.
- `gh auth` needs the `project` scope — present as of 2026-08-12; `gh auth refresh -s project` if it
  is lost.
- Read the board with `gh api graphql`, never `gh project item-list` — item-list served a stale
  title for #10 on 2026-08-12 and can under-report. GraphQL returns items in board-position order,
  and that order is authoritative: the top Todo card is what to work on next.
- Docs root for absolute links (GitHub emits relative paths verbatim and they 404):
  `https://github.com/pmvanev/phil-claude-plugin/blob/main/`
- **Label families.** `wave: *` is **single-valued — swap, never add** (`phil:nwave-issue-board`).
  GitHub has no scoped labels, so nothing enforces it: a feature walked DISCUSS→DELIVER accumulates
  four wave labels and the record of where it stands becomes unreadable while every command reported
  success. `bug` · `documentation` · `enhancement` are **multi-valued by decision, not by neglect** —
  this plugin's product is prose, so `documentation` names a surface, never a kind of work that could
  compete with `enhancement`. The two answer different questions, so a card carrying both (#2, #4) is
  correct. This bullet is the declaration `phil:groom-issues` rule 4 reads; label descriptions may
  echo it and lose on disagreement.
- Forge mechanics: `phil:issue-board`. nWave feature/slice/step mapping: `phil:nwave-issue-board`.
