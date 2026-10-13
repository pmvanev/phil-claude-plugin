---
description: "Renamed to /phil:harden-instructions. This alias still revises CLAUDE.md and AGENTS.md files as before, and goes away in a later release."
argument-hint: "[file-or-directory ...]"
mutates: true
allowed-tools: Read, Edit, Glob, Grep, Bash(git -C:*)
---

Start the reply with one line: `/phil:claude-md` is now `/phil:harden-instructions`, and this alias will be removed in a later release.

Then load and follow the instructions in the `harden-instructions` skill at `${CLAUDE_PLUGIN_ROOT}/skills/harden-instructions/SKILL.md`.

With `$ARGUMENTS` empty, keep the old behaviour: Glob the current directory for `**/CLAUDE.md`, `**/CLAUDE.local.md` and `**/AGENTS.md`, drop matches the skill's Directory Path step 2 drops, and pass the rest to the skill as file paths. Skills, agents, commands and rules are left to `/phil:harden-instructions`.
