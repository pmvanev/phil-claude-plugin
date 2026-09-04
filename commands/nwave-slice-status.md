---
description: "Show a read-only table of an nWave slice's steps — what each does, which are done, which one you're on, which are next. On request, also folds a feature-level state over every slice, or a story-level state over every feature in a story, for a caller placing the card in a board column."
argument-hint: "[feature-id] [slice-number] [--feature-state] [--story-state <slug>]"
mutates: false
allowed-tools: Read, Grep, Glob, Bash(git log:*), Bash(ls:*)
---

Load and follow the instructions in the `nwave-slice-status` skill at `${CLAUDE_PLUGIN_ROOT}/skills/nwave-slice-status/SKILL.md`.
