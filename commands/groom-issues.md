---
description: "Read a whole issue board and report what is wrong with it — bodies that state no purpose or no way to tell when they are done, links that will 404, accumulated labels, plus the defects that live between issues: duplicates, oversized cards, work overcome by events, effort with no container, features decomposed into slice cards under retired rules, and a story spread across several feature cards. Reports only; changes nothing."
argument-hint: "[<owner/repo> or <group/project>]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(gh api graphql:*), Bash(glab issue list:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
scan it describes.

This command **reports and never writes**. It declares `mutates: true` while writing nothing, and the
declaration is honest rather than defensive: `Bash(gh api graphql:*)` accepts a mutation document, so the
grant *permits* a write that this command must never make. `mutates: false` beside that grant would be a
false claim about the tool list, which is the one thing that declaration is for.

**The guarantee is now half enforced and half promised, and which half is which matters.** No `Write`
and no `Edit`, so no file can be touched — mechanical, checkable, unchanged. The forge half is prose: this
paragraph, and the never-do list in the skill. **Send only `query` documents through `gh api graphql`,
never `mutation`.**

**Why the grant exists.** The decomposed-feature check ranks a real parent/child edge as its strongest
evidence — sufficient on its own to offer an irreversible consolidation. `parent` and `subIssues` are
GraphQL-only; `gh issue list --json` exposes neither and no flag adds one. Without this call the check
reported **clean** on every board whose slice cards were properly parented, which is exactly the
population it was written for. That was issue #30.

**Two alternatives were rejected, and neither was overlooked.** A read-only helper script cannot restore
the enforcement: no grant names one script, only its interpreter, and an interpreter cannot honestly join
`READ_ONLY_VERBS` in `scripts/check-readonly-commands.py`, whose header says an entry there promises the
verb has no writing mode. Leaving the edge unread was the honest status quo and left the check inert
where it matters. The precedent for the trade taken instead is `commands/resume.md`, which has declared
`mutates: true` while writing nothing since 2026-08-17.

Read the edges in **one** call for the whole board, not one per issue.

End the report by naming the command that acts on each column, with its count:

- *"3 mechanical findings; `/phil:groom-fix` applies them inside a scope you pick"*
- *"2 set-level candidates; `/phil:groom-set` resolves them, asking before each"*
- *"4 semantic findings; `/phil:groom-ask` fills a card in from your answers, one at a time"*

Name them; do not run either, and do not offer to. Naming a command with a count is a handover; running
it is the consent step that command owns, taken by the one session that has not asked.

**This command applies no prose standard to anything reaching a board, and that is correct rather than
an omission.** It does compose: the whole report, every finding sentence with its quoted evidence, the
handover lines, the checks-that-passed prose. But that output is **terminal-only** — it lands on no
card, nobody inherits it, and the next run regenerates it. It is outside the board surfaces this
standard governs.

Every sentence it *evaluates* was written by a human, and judging those is the taste-policing the
skill's standard refuses — see *Judging prose is taste; composing it is not*. `rules/writing.md` reaches
the commands in this family that **write to a card** (`groom-ask`, `groom-set`), never the one that
reads.

Stated in as many words because a surface with no citation is otherwise indistinguishable from one
that forgot.
