---
description: "Measure a Lambda web app's cold path from the function's own logs — cold starts after a failed INIT and suppressed inits counted apart — name the layer to look inside, and drill one level into it from the function's own timing line, citing the command behind every number. Reads AWS; never deploys, invokes or reconfigures the function."
argument-hint: "[function-name] [--profile <name>] [--region <region>]"
mutates: true
allowed-tools: Read, Grep, Glob, AskUserQuestion, Bash(aws lambda list-functions:*), Bash(aws lambda get-function-configuration:*), Bash(aws logs filter-log-events:*), Bash(python3:*)
---

Load and follow the instructions in the `lambda-web-app-speed` skill at `${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/SKILL.md`.

Arguments: $ARGUMENTS
