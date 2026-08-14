---
description: "Fill in a card that says too little — presents the card, asks only for what the scan reported missing, offers a suggestion or two, and writes what you sanction. Every field says where its words came from, and a question you decline stays unanswered rather than guessed."
argument-hint: "<issue-number> [<owner/repo> or <group/project>]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(glab issue list:*), Bash(glab issue view:*), Bash(glab issue update:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
loop in *Eliciting the semantic content*.

Re-read the issue immediately before writing. This command inherits no report from another session,
and the body it is about to replace is prose a human wrote — the rule matters more here than
anywhere else in the family.

**This command is an editor, and the distinction is the whole design.** `/phil:groom-fix` refuses to
draft a purpose or invent acceptance criteria, and that refusal is correct and is not relaxed there —
it never asks, so it may never draft. This command asks, so it may.

**What it may never do is put a word on a card the user has not sanctioned.** Present the card, ask only
for what the scan reported missing, offer a suggestion or two marked as yours, and write the result —
with a provenance label on every field you write, from exactly this set: `you wrote` ·
`you accepted my suggestion` · `you edited my suggestion` · `I rephrased your answer`. **An unlabelled
field is the defect**, however well the body reads.

**An accept must name the suggestion or restate its text.** A bare affirmation — "ok", "sure", "yep",
"that works" — is never an accept, even when only one suggestion is on the table. Ask once more, naming
what is still needed; after a second unanswered ask, treat it as a decline and say so.

**One card per invocation.** No batch, no apply-to-all, no "same again for the other four". The
content differs every time, so there is nothing for a bulk offer to scale over, and a bulk offer here
would collect one answer and write it as though it were several.

**Its scoping is the boundary.** `Bash` is scoped to issue read and edit verbs. It grants no
`gh issue create`, no `gh issue close`, no `gh issue comment`, no `gh api` (which permits
`--method POST` on anything), no `gh project`, and no bare `Bash`. It changes what a card *says*,
never which cards exist or where they sit.
