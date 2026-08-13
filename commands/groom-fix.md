---
description: "Apply the mechanical fixes /phil:groom-issues reported — relative links that 404, accumulated single-valued labels, one-sided chains, missing cross-references — inside a scope you pick, each change reported with the reason it needed no judgement. Never touches a defect that needs a decision."
argument-hint: "[<owner/repo> or <group/project>]"
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(glab issue list:*), Bash(glab issue view:*), Bash(glab issue update:*), Bash(git ls-tree:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
apply loop in *Applying the mechanical column*.

Re-scan first. This command never inherits a report from another session — the scan is one call, and a
fix computed against remembered text is the failure the separation exists to prevent.

**This command writes, and its scoping is the boundary.** `Bash` is scoped to issue read and edit verbs
plus `git ls-tree` for confirming a link target is pushed. It grants no `gh api` (which permits
`--method POST` on anything), no `gh project` (status and position are `phil:rank-issues`), no
`gh issue close`, no `gh issue create`, no bare `Bash`. Changing the *set* of cards belongs to
`/phil:groom-set` and is not reachable from here.

**It never writes before you have picked a scope**, and never touches a defect the report classified as
needing a decision. Both are in the skill; neither is negotiable here.
