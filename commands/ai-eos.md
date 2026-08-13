---
description: "Detect the stylistic tells that mark technical prose as AI-generated — unearned significance, participle padding, formulaic closers, phantom attribution — with a density verdict and ranked findings."
argument-hint: "<--changes | file-path | lines:N-M | directory-path>"
mutates: false
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Skill
---

Load and follow the instructions in the `ai-eos` skill at `${CLAUDE_PLUGIN_ROOT}/skills/ai-eos/SKILL.md`.
