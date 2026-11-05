---
description: "Make a committed draft read as its author's: strip the AI tells, reword it toward a voice profile built from documents the author wrote, and add exactly the slips asked for, each reported by line."
argument-hint: "<file> [--profile <name>] [--slips N] [--misspellings] | --build-profile <name> <sample paths…>"
mutates: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git ls-files:*), Bash(git status:*), Bash(python3:*)
---

Load and follow the instructions in the `humanize-technical-prose` skill at `${CLAUDE_PLUGIN_ROOT}/skills/humanize-technical-prose/SKILL.md`.
