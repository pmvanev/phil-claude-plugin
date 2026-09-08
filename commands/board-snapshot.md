---
description: "Say where the issue board stands right now, in 200 words or fewer: what is blocked and what each waits on, what is in flight, and the next few in the board's own order. Reports drift and never fixes it; consumes the board's order and never computes one. For what is WRONG with the cards use /phil:groom-issues instead."
argument-hint: "[<owner/repo>] [--all] [--next N]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(gh api graphql:*), Bash(gh issue view:*)
---

Load the `board-snapshot` skill at `${CLAUDE_PLUGIN_ROOT}/skills/board-snapshot/SKILL.md` and render the
standing check it describes.

Read the board constants — project id, project number, Status field — from the target repo's `CLAUDE.md`
before making any call. Do not probe for them; `/phil:board-setup` owns writing them, and a snapshot that
re-derived them would be a second authority over a fact the repo already records.

`--next N` sets how many queued cards to print in the standing check. Default 5.

`--all` renders the orientation read instead: every open card as a number, a title and a composed
description of 100 words or fewer. It drops nothing and has no total ceiling — the two modes bound
themselves differently, and the skill says why.

**This command reports and never writes.** It declares `mutates: true` while writing nothing, and the
declaration is honest rather than defensive: `Bash(gh api graphql:*)` accepts a mutation document, so the
grant *permits* a write this command must never make. `mutates: false` beside that grant would be a false
claim about the tool list, which is the one thing the declaration is for. The precedent is
`commands/resume.md`, which has declared `true` while writing nothing since 2026-08-17.

**The guarantee is half enforced and half promised, and which half is which matters.** No `Write` and no
`Edit`, so no file can be touched — mechanical, checkable. The forge half is prose: this paragraph and the
skill's never-do list. **Send only `query` documents through `gh api graphql`, never `mutation`.**

**Why the grant exists.** Status is a project field, not a label. `gh issue list --json` returns no Status
and no flag adds one, so the three sections cannot be populated without the project-items query, which is
GraphQL-only. `gh project item-list` is refused for the same reason `CLAUDE.md` refuses it everywhere: it
served a stale title on 2026-08-12 and can under-report, and under-reporting inside a bounded read is
invisible by construction.

**Send the query with GraphQL variables.** Interpolating a `fieldValueByName(name: "Status")` selection
into a single-quoted `-f query='…'` fails to parse; `-F query=@file` would work and is unavailable,
because writing a temp file is outside this grant and `CLAUDE.md` forbids a path inside a `Bash(...)`
grant. Measured 2026-09-08.

Report the outcome by name, per the skill's `## Decision outcomes`. End by naming the command that acts
on anything reported, with its count — for example *"1 card in Done while open; `/phil:groom-issues`
reports it against the board standard"*. Name it; do not run it, and do not offer to.

**`rules/writing.md` governs everything this command composes** — in the standing check, the sentence
naming empty sections, the withheld count, the clause saying where the order came from, and the drift,
uncolumned and inflation lines; in `--all`, every description. The skill states the boundary and carries the citation. Card titles are quoted
verbatim, because they are the filer's words and judging them would be the taste-policing this family
refuses.

*An earlier draft of this paragraph said the command applied no prose standard, on the grounds that
composed descriptions arrive in a later slice. That was false about this slice and it silently reversed a
locked decision. Corrected 2026-09-08.*
