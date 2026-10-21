---
description: "Review a CI pipeline against rules/ci-pipelines.md and the supply-chain, privilege and credential rows of rules/security.md, and write a findings backlog."
argument-hint: "[--changes | file-path | directory-path]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git ls-files:*), Write
---

Load and follow the instructions in the `review-ci` skill at `${CLAUDE_PLUGIN_ROOT}/skills/review-ci/SKILL.md`.

Arguments: $ARGUMENTS
