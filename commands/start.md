---
description: "Pick a card up: resolve a number, title or description to one open card, refuse a closed card and ask before a card in Done or someone else's, describe what it asks and how anyone will know it is done, and recommend one route with its reason, launched only on a yes. Writes nothing before the launch. For a card already underway, use /phil:resume."
argument-hint: "<issue number, URL, title or description>"
mutates: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(git rev-parse:*), Bash(gh api graphql:*)
---

Load the `start` skill at `${CLAUDE_PLUGIN_ROOT}/skills/start/SKILL.md` and run its RESOLVE, CHECK,
DESCRIBE, ROUTE and REPORT steps for the card `$ARGUMENTS` names. With no argument, ask which card to
start; never infer it from the branch.

Read the repo and the board constants from the working tree's `CLAUDE.md`. With no forge line, name
`/phil:board-setup` and report `CANNOT-RUN`. Pass the owner and repo as variables to `gh api graphql`,
which takes no `-R`.

**Write nothing before the launch.** Send only `query` documents through `gh api graphql`; run `git`
only for `rev-parse --show-toplevel`. No tool boundary backs these limits. A launched route, inline
included, writes under its own rules.

Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md` before composing the description and the report, as the
skill directs, and leave every quoted line of the card or of `CLAUDE.md` in its own words.

Launch the recommended route only on the developer's yes. Print the outcome tokens before the launch —
exactly one terminal outcome, `LAUNCHED`, `NOT-LAUNCHED`, `STOPPED`, `NO-MATCH`, `REFUSED-CLOSED` or
`CANNOT-RUN`, with each report line that fires, and `WROTE-NOTHING` on every run.
