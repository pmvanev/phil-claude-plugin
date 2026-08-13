---
description: "Read a whole issue board and report what is wrong with it — bodies that state no purpose or no way to tell when they are done, links that will 404, accumulated labels, plus the defects that live between issues: duplicates, oversized cards, work overcome by events. Reports only; changes nothing."
argument-hint: "[<owner/repo> or <group/project>]"
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(glab issue list:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
scan it describes.

This command is **read-only**, and enforced rather than declared. It has no `Write` or `Edit`, and
its `Bash` is scoped to `gh issue list` and `glab issue list` — not `gh api`, which would permit
`--method POST` and hand back the mutation the scoping exists to remove.

End the report by naming `/phil:groom-fix` as the command that applies the mechanical column, and its
count — *"3 mechanical findings; `/phil:groom-fix` applies them inside a scope you pick"*. Name it; do
not run it, and do not offer to. The set-level candidates belong to slice 03 and have no command yet.
