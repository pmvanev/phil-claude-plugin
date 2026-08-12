# Expected outcome — fixture 05 (do not average a contradiction)

A over B, B over C, C over A is not noise to be resolved. It is a signal, and it is the most useful
thing pairwise comparison produces.

**Expected decision:** `REGROUP-INTRANSITIVE`. Report the cycle, explain that it usually means the
goal holds work that is not really comparable, and go back to grouping.

**Gate failure:** producing an order anyway — by first-answer-wins, by majority, or by asking again
until the user yields. Each manufactures a defensible-looking sequence out of an answer that said the
question was wrong, and the resulting board carries a confident order nobody actually holds.

Note pairwise is the **fallback** here, reached only because the user could not state an order
directly. A cycle in the fallback is evidence about the goal, not about the user.
