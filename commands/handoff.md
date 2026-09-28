---
description: "Put this session down: record what a fresh session cannot derive — the decisions reached, the approaches ruled out, the work stack you were diverted through, and the intended next action, plus the session's last three prompts and replies word for word — stamped with a tree fingerprint so the next session can tell whether it is still current. Refreshes the feature card's projection so a teammate can read it too. Reports back in about 300 words of plain English, saying so when it withheld any, while the snapshot itself is written whole and never clipped. Writes nothing if the session advanced nothing."
argument-hint: "[\"<what you were doing>\"]"
mutates: true
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Skill
---

Load the `session-handoff` skill at `${CLAUDE_PLUGIN_ROOT}/skills/session-handoff/SKILL.md`. Follow the CAPTURE path; the
snapshot format, the deriving rules, the decision outcomes, and the never-do list govern all three paths.

**The local snapshot is written before the card's projection is refreshed, and nothing is ever read back
from the card.** A forge failure leaves the snapshot standing and is reported as
`PROJECTION-UNREFRESHED`; it is not a failed capture. Where the work has a card and neither `PROJECTED`
nor `PROJECTION-UNREFRESHED` is reported, the run skipped the card silently — the snapshot is written
either way, so nothing else would show it.

**The report is bounded at 300 words; the snapshot is not.** The echo of what was recorded gives ground
first — clipped, it reports `REPORT-CLIPPED` and states how many decisions were withheld against the
whole recorded population. Nothing is ever left out of `.session-handoff.md` to shorten this output. The
ceiling, what may never give ground, and why `/phil:stack` is exempt are the skill's, under *The report
has a ceiling; the record never does*.

**The last three exchanges go in the snapshot word for word — this handoff's prompt and report the last
of them — and nowhere else.** Not onto the card, and not into the report beyond one line counting them.
**This session never types them.** A script copies them from the transcript Claude Code already keeps,
after the report is printed, so what the file holds is what was printed:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py head   --file <root>/.session-handoff.md
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py count
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py write  --file <root>/.session-handoff.md --expect-sha <h1> --body - <<'SESSION_HANDOFF_BODY'
<the header, the why, the next action and the stack>
SESSION_HANDOFF_BODY
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py record --file <root>/.session-handoff.md --expect-sha <h>
```

`head` prints `SHA <h1>` from the same read; `write` prints `WROTE <h>`, the hash `record` takes. **Never
the Write tool on the snapshot**: it refuses a file it has not Read whole, and reading it whole pulls the
previous session's replies into context.

Copying them by hand is what 0.97.0 did, and Anthropic's safety classifier refused it as duplicating
model outputs in 7 of 8 real handoffs. The skill owns the rules, under *The last exchanges*.
