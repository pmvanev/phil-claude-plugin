---
description: "Declare a project's CI policy and write or edit its pipeline so the trigger matrix keeps that policy in every cell, with every job calling the project's entry-point script; lints the result, wires a red-main alert, names whoever started a failed pipeline, and asks before changing any forge setting. --speed measures the pipeline and ranks speed-ups on its critical path; --rework finds artifacts built twice."
argument-hint: "[--speed | --rework] [directory-path]"
mutates: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git remote get-url:*), Bash(git symbolic-ref:*), Bash(git rev-parse --verify:*), Bash(chmod +x:*), Bash(sh -n:*), Bash(shellcheck:*), Bash(uv pip compile:*), Bash(npm install --package-lock-only:*), Bash(glab ci lint:*), Bash(glab api:*), Bash(gh api:*), Bash(actionlint:*), Bash(python3:*), AskUserQuestion
---

Load and follow the instructions in the `build-ci` skill at `${CLAUDE_PLUGIN_ROOT}/skills/build-ci/SKILL.md`.

Arguments: $ARGUMENTS
