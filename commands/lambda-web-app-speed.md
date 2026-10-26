---
description: "Measure a Lambda web app's cold path from the function's own logs — cold starts after a failed INIT and suppressed inits counted apart — name the layer to look inside, drill one level into it from the function's own timing line, rank the fixes by the time each saves, stopping at the project's target, price keeping it warm, and split one page load's first byte, citing the command behind every number. Reads AWS and never deploys or reconfigures the function; it invokes it only by loading the one page the person names and agrees to."
argument-hint: "[function-name] [--url <page>] [--profile <name>] [--region <region>]"
mutates: true
allowed-tools: Read, Grep, Glob, AskUserQuestion, Bash(aws lambda list-functions:*), Bash(aws lambda get-function-configuration:*), Bash(aws logs filter-log-events:*), Bash(python3:*)
---

Load and follow the instructions in the `lambda-web-app-speed` skill at `${CLAUDE_PLUGIN_ROOT}/skills/lambda-web-app-speed/SKILL.md`.

Arguments: $ARGUMENTS
