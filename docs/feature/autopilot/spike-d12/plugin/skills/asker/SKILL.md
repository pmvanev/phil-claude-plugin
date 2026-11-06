---
name: asker
description: Throwaway probe skill. Use only when the spikeap auto commands launch it.
---

# Asker

1. Call the AskUserQuestion tool with exactly one question: "Which colour should the widget be?",
   header "Colour", multiSelect false, and two options:
   - label "Blue (Recommended)", description "Matches the existing palette."
   - label "Red", description "Stands out, but clashes with the palette."
2. Write the label of the option that was chosen, and nothing else, to the file `answer.txt` in the
   current working directory.
3. Print one line: `ANSWER: <the chosen label>` and, on a second line, `HOW: <how the answer was
   decided — by the user, by a hook, or by you>`.
