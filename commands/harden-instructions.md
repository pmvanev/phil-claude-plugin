---
description: "Harden any instruction file — CLAUDE.md, AGENTS.md, a skill, agent, command or rule, here or in another repo — so each rule lives where the model cannot lose it and what stays in prose is phrased to be recalled."
argument-hint: "[file-or-directory ...]"
mutates: true
allowed-tools: Read, Edit, Glob, Grep, Bash(git -C:*)
---

Load and follow the instructions in the `harden-instructions` skill at `${CLAUDE_PLUGIN_ROOT}/skills/harden-instructions/SKILL.md`.
