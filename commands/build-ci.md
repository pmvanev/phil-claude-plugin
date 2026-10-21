---
description: "Declare a project's CI policy and write or edit its pipeline so the trigger matrix keeps that policy in every cell, with every job calling the project's entry-point script; lints the result and asks before changing any forge setting."
argument-hint: "[directory-path]"
mutates: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git remote get-url:*), Bash(git symbolic-ref:*), Bash(chmod +x:*), Bash(sh -n:*), Bash(glab ci lint:*), Bash(glab api:*), Bash(gh api:*), Bash(actionlint:*), AskUserQuestion
---

Load and follow the instructions in the `build-ci` skill at `${CLAUDE_PLUGIN_ROOT}/skills/build-ci/SKILL.md`.

Arguments: $ARGUMENTS
