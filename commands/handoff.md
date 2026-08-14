---
description: "Put this session down: record what a fresh session cannot derive — the decisions reached, the approaches ruled out, the work stack you were diverted through, and the intended next action — stamped with a tree fingerprint so the next session can tell whether it is still current. Refreshes the feature card's projection so a teammate can read it too. Writes nothing if the session advanced nothing."
argument-hint: "[\"<what you were doing>\"]"
mutates: true
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Skill
---

Load the `session-handoff` skill at `${CLAUDE_PLUGIN_ROOT}/skills/session-handoff/SKILL.md`. Follow the CAPTURE path; the
snapshot format, the deriving rules, the decision outcomes, and the never-do list govern both paths.

**The local snapshot is written before the card's projection is refreshed, and nothing is ever read back
from the card.** A forge failure leaves the snapshot standing and is reported as
`PROJECTION-UNREFRESHED`; it is not a failed capture. Where the work has a card and neither `PROJECTED`
nor `PROJECTION-UNREFRESHED` is reported, the run skipped the card silently — the snapshot is written
either way, so nothing else would show it.
