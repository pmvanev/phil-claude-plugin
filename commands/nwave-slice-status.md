---
description: "Show a read-only table of an nWave slice's steps — what each does, which are done, which one you're on, which are next."
argument-hint: "[feature-id] [slice number] - both optional; defaults to the most recently modified feature"
mutates: false
allowed-tools: Read, Grep, Glob, Bash(git log:*), Bash(ls:*)
---

Load and follow the instructions in the `nwave-slice-status` skill at `${CLAUDE_PLUGIN_ROOT}/skills/nwave-slice-status/SKILL.md`.
