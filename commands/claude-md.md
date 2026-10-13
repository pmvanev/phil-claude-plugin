---
description: "Review and revise any CLAUDE.md or AGENTS.md — here or in another repo — so each rule is phrased to be followed and lives where the model cannot lose it."
argument-hint: "[file-or-directory ...]"
mutates: true
allowed-tools: Read, Edit, Glob, Grep, Bash(git -C:*)
---

Load and follow the instructions in the `claude-md` skill at `${CLAUDE_PLUGIN_ROOT}/skills/claude-md/SKILL.md`.
