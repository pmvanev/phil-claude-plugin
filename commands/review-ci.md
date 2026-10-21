---
description: "Review a CI pipeline against rules/ci-pipelines.md, the pipeline rows of rules/security.md and the project's declared CI policy, with a jobs-by-source trigger matrix, and write a findings backlog."
argument-hint: "[--changes | file-path | directory-path]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash(git diff:*), Bash(git ls-files:*), Write
---

Load and follow the instructions in the `review-ci` skill at `${CLAUDE_PLUGIN_ROOT}/skills/review-ci/SKILL.md`.

Arguments: $ARGUMENTS
