---
description: "Resolve the defects that live between issues — duplicates, oversized cards, work overcome by events, effort with no container, a feature decomposed into slice cards under retired rules, a story spread across feature cards — one candidate at a time, each surfaced with its evidence and applied only on your answer. Merges, splits, closes and consolidations are irreversible, so none of them happens without a question. Where a resolution needs a call this command does not hold — a reopen, a Status write, a rollup read — it hands the call over and stops."
argument-hint: "[<owner/repo> or <group/project>]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(gh issue create:*), Bash(gh issue close:*), Bash(gh issue comment:*), Bash(gh project item-add:*), Bash(glab issue list:*), Bash(glab issue view:*), Bash(glab issue update:*), Bash(glab issue create:*), Bash(glab issue close:*), Bash(glab issue note:*), Bash(git log:*), Bash(git ls-tree:*), AskUserQuestion, Skill
---

Load the `groom-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/groom-issues/SKILL.md` and run the
loop in *Resolving the set-level candidates*.

Re-scan first, and re-derive between candidates. Like `/phil:groom-fix` this command inherits no
report from another session — but it carries a second obligation that command does not: **its own
applies change the set it is reading.** A merge closes a card that a later candidate may name, and a
split creates numbers no earlier scan could have seen. Candidates are resolved one at a time against
a fresh read, never against the list the run started with.

**This command changes which cards exist, and its scoping is the boundary.** `Bash` is scoped to
issue read, edit, create, close and comment verbs, plus `gh project item-add` so a card this command
creates lands on the board, plus read-only `git log` / `git ls-tree` for the evidence that work landed
another way. It grants no `gh api` (which permits `--method POST` on anything), no `gh project
item-edit` — Status and position are not this command's to set — and no bare `Bash`.

**Creating a milestone is deliberately out of reach.** `gh` has no milestone-create verb, and the
`gh api` call that would do it is not granted. This command joins a card to a container that already
exists; where the right container does not exist yet, it proposes one, hands you the exact call, and
stops. A goal invented inside a grooming run is a goal nobody agreed to.

**Every one of them asks, every time.** Merge, split, close, group and the two consolidations are the
candidate classes, and no population size, no obviousness, and no run of prior approvals converts any of them
into a default. That is the whole discipline of this command.

**The comments it leaves are composed against `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`.** A merge,
split or closing comment is the permanent record of an irreversible act, read months later by someone
reconstructing why a card went away — so it states the reason in one pass. Facts first, active voice,
the emphatic word last; concision is one of the standard's eleven principles of composition, never a licence to drop a
reason to save words.

This governs what this command composes and licenses nothing about prose a human wrote — see the skill's
*Judging prose is taste; composing it is not*.
