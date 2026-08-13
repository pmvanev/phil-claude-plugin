---
description: "Read a whole issue board and report what is wrong with it — bodies that state no purpose or no way to tell when they are done, links that will 404, accumulated labels, plus the defects that live between issues: duplicates, oversized cards, work overcome by events. Reports only; changes nothing."
argument-hint: "[<owner/repo> or <group/project>]"
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(glab issue list:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
scan it describes.

This command is **read-only**, and enforced rather than declared. It has no `Write` or `Edit`, and
its `Bash` is scoped to `gh issue list` and `glab issue list` — not `gh api`, which would permit
`--method POST` and hand back the mutation the scoping exists to remove. Fixing what the report finds
is a later slice.
