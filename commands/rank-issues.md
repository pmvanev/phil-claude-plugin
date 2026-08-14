---
description: "Turn an unsorted board into a queue: elicit the goals your issues serve, order the goals by milestone due date, then order the issues inside each goal by board position — recording why each goal ranks where it does, and writing any dependency it uncovers as a real forge link rather than burying it in the order. In an nWave repo the ranked unit is the feature card, so a board still carrying slice cards is consolidated before it is ranked."
argument-hint: "[<owner/repo> or <group/project>]"
mutates: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Skill
---

Load the `rank-issues` skill at `${CLAUDE_PLUGIN_ROOT}/skills/rank-issues/SKILL.md` and run the
session it describes. Ask through every step before writing anything: a half-ranked board is worse
than an unranked one.
