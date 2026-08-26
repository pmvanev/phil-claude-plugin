<!-- decision-request-emission:v1 -->

<!-- context -->

Review verified against the files — it's substantially correct, and my first grep missed the duplication only because of line wrapping. Confirmed defects in what I shipped:

| # | Finding | Status |
|---|---|---|
| 1 | Ceiling says "count the framing", remedy says "cut options" — cutting options changes a count they don't enter. And a third line treats the ask as framing **+ option labels** | **Confirmed** — three-way inconsistency |
| 2 | "Detail sits below" is unimplementable against the emission order the same file mandates | **Confirmed** |
| 3 | "In force deterministically" overclaims — delivery is deterministic, compliance isn't, and my own test docstrings say so | **Confirmed** |
| 5 | Header claims it's "referenced by the skills that hold `AskUserQuestion`" — it's 1 of 6. The exact defect I fixed in the sibling fragment hours earlier | **Confirmed** |
| 6 | "Ask once more, naming what is still needed" is byte-identical in both files, and the fragment omits the two-ask cap — so it licenses the nagging loop `groom-issues` forbids | **Confirmed** |
| 8 | Prose permits naming a command the reader is about to run; my own regex matches `/phil:` on sight | **Confirmed** — prose and oracle contradict |

Holding edits until the validator finishes, so it isn't reading files I'm changing underneath it. One of these needs your call rather than my judgement.

<!-- /context -->

<!-- interrupted -->

I got something wrong that needs your decision.

<!-- /interrupted -->

<!-- decision -->

I wrote that the extra detail behind a question "sits below" it. That cannot work: the question box takes over the screen and waits for your answer, so anything placed after it does not reach you until you have already decided — and anything placed before it sits between the question and its options, which is the wall of text we are trying to kill. When I actually asked you something earlier today, I put the background above the question and it read fine. So the rule I wrote and the one instance that worked disagree.

<!-- /decision -->

<!-- consequence -->

What turns on it: this decides where every future question puts its supporting material, and whether the word limit stays workable at all — a hard limit only works if there is somewhere for the overflow to go.

<!-- /consequence -->

<!-- call -->
