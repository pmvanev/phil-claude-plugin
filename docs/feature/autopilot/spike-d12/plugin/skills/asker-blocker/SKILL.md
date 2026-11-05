---
name: asker-blocker
description: Throwaway probe skill. Use only when the spikeap auto-blocker command launches it.
---

# Asker (blocker)

1. Call the AskUserQuestion tool with exactly one question: "Which of your own unpublished essays
   should the voice profile learn from?", header "Samples", multiSelect false, and two options:
   - label "All of them (Recommended)", description "The most text to learn from."
   - label "Only the 2017 essay", description "Less text, one register."
2. Write the label of the option that was chosen, and nothing else, to `answer.txt`.
3. Print `ANSWER: <the chosen label>`.
