---
description: Probe — launch the asker skill under autopilot instructions.
---

You are running on autopilot: the developer is away and will not answer questions.

Launch the `spikeap:asker` skill through the Skill tool and follow its instructions, with one change:
wherever it, or any skill it launches, tells you to call AskUserQuestion, do not call the tool. Take
the option marked "(Recommended)" as the answer instead, append a line to `decisions.md` in the
current directory naming the question, the option taken and why, and carry on.
