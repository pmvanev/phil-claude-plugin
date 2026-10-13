---
description: "Say where the issue board stands right now: what is blocked and what each waits on, what is in flight, and the next few in the board's own order, in 200 words or fewer. With --all, every open card instead, as a number, a title and a plain-English description of 100 words or fewer — no total ceiling, nothing dropped. Reports drift and never fixes it. For what is WRONG with the cards use /phil:groom-issues instead."
argument-hint: "[<owner/repo>] [--all] [--next N]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(gh api graphql:*), Bash(gh issue view:*), Bash(gh issue list:*)
---

Load the `board-snapshot` skill at `${CLAUDE_PLUGIN_ROOT}/skills/board-snapshot/SKILL.md` and render the
standing check it describes.

Read the board constants — the owner, the project number and the Status field — from the working tree's
`CLAUDE.md` before making any call. Do not probe for them: `/phil:board-setup` owns writing them, and a
snapshot that re-derived them would be a second authority over a fact the repo already records.

The target is the repo the constants' forge line names. `<owner/repo>`, when given, must match it: the
constants can be read only from the working tree, so a different repo would mix two repos' facts into a
well-formed wrong answer. When the argument differs, or `CLAUDE.md` holds no board constants, stop and
name `/phil:board-setup`, to be run in the target repo's checkout. Pass `-R <owner/repo>` on every `gh
issue` call, per `phil:issue-board`: an inferred remote reads the wrong repo's issues successfully.

`--next N` sets how many queued cards to print in the standing check. Default 5.

`--all` renders the orientation read instead: every open card as a number, a title and a composed
description of 100 words or fewer. It drops nothing and has no total ceiling — the two modes bound
themselves differently, and the skill says why.

**This command reports and never writes. Send only `query` documents through `gh api graphql`, never
`mutation`.** The grant accepts a mutation document and no tool boundary refuses one: with no `Write` or
`Edit`, no file can be touched, but the forge write rests on this prose and the skill's never-do list.

Status is a project field, not a label: `gh issue list --json` returns no Status and no flag adds one, so
the sections need the GraphQL project-items query. `gh project item-list` is refused: it served a stale
title on 2026-08-12 and can under-report, invisibly inside a bounded read. `gh issue list` is the
reconciliation call: the project-items query returns only issues somebody added to the project, so without
it an open issue nobody added is omitted in silence — a completeness claim the skill forbids, reached
structurally rather than through a dropped page.

Report every outcome the skill's `## Decision outcomes` requires — the terminal one, `READ-ONLY`, and each
report line that fires. Each report line names its resolver where the skill gives one, with its count —
for example *"1 card in Done while open; `phil:groom-issues` reports it against the board standard"*. Name
it; do not run it, and do not offer to.

**Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`; it governs everything this command composes** — in the
standing check, the sentence naming empty sections, the withheld count, the clause saying where the order
came from, and the drift, uncolumned, off-board and inflation lines; in `--all`, every description — which
also may not carry a file path, a bracketed identifier or a bare handle. Card numbers are permitted;
spelling one out in longhand to dodge the vocabulary rule is the failure the permission exists to prevent.
The skill states the boundary and carries the citation. Card titles are quoted verbatim: they are the
filer's words, and judging them would be the taste-policing this family refuses.
