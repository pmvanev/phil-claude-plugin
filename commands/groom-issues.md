---
description: "Read a whole issue board and report what is wrong with it — bodies that state no purpose or no way to tell when they are done, links that will 404, accumulated labels, plus the defects that live between issues: duplicates, oversized cards, work overcome by events, effort with no container, features decomposed into slice cards under retired rules, and a story spread across several feature cards. Reports only; changes nothing."
argument-hint: "[<owner/repo> or <group/project>]"
mutates: false
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(glab issue list:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
scan it describes.

This command is **read-only**, and enforced rather than declared. It has no `Write` or `Edit`, and
its `Bash` is scoped to `gh issue list` and `glab issue list` — not `gh api`, which would permit
`--method POST` and hand back the mutation the scoping exists to remove.

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
