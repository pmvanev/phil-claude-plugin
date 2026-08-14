---
description: "Fill in a card that says too little — asks what the issue is for and how you will know it is done, then writes your answers into the body. It composes nothing: every word is yours, and a question you decline stays unanswered rather than guessed."
argument-hint: "<issue-number> [<owner/repo> or <group/project>]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(glab issue list:*), Bash(glab issue view:*), Bash(glab issue update:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
loop in *Eliciting the semantic content*.

Re-read the issue immediately before writing. This command inherits no report from another session,
and the body it is about to replace is prose a human wrote — the rule matters more here than
anywhere else in the family.

**This command is a scribe, and the distinction is the whole design.** `/phil:groom-fix` refuses to
draft a purpose or invent acceptance criteria, and that refusal is correct and is not relaxed here.
What this adds is not permission to compose — it is somewhere for the answer to come from. Every word
written traces to something the user said. Nothing is inferred from the title, the labels, a sibling
card, or the repository.

**One card per invocation.** No batch, no apply-to-all, no "same again for the other four". The
content differs every time, so there is nothing for a bulk offer to scale over, and a bulk offer here
would collect one answer and write it as though it were several.

**Its scoping is the boundary.** `Bash` is scoped to issue read and edit verbs. It grants no
`gh issue create`, no `gh issue close`, no `gh issue comment`, no `gh api` (which permits
`--method POST` on anything), no `gh project`, and no bare `Bash`. It changes what a card *says*,
never which cards exist or where they sit.
