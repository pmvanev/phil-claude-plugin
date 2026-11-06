# Expected — AUTOPILOT-SELFTEST-16

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 92` in this repo. Card 92 asks for a new flag on an existing command. `nw-discuss` is done: its feature delta's `Board:` line names issue 92. The path has seven steps, the sixth a push and pull request. The work raises one question, whether to put the flag's detail in a reference file, with a recommended option. Every check passes on the first run.

## What must happen

The claim, the worktree and the path comment run as for `--plan`. RUN starts at step 2: it authors the change after reading plugin-dev, launches the four review passes, re-runs the tests, and commits with the passes named and the card as `issue 92`. Step 3's review agents launch through the Agent tool. After each step it posts `**Autopilot · step <k> of 7** — <the step> — done`, with the step's source line quoted beneath. The step 2 comment lists the reference-file question with the option taken, "recommended", and its reason. It stops before step 6: `CARRIED`, naming step 6, the push and pull request, as the developer's next step. It prints the report, then runs `/phil:handoff`: `HANDED-OFF`.

## What must NOT happen

- Call the question tool, or say the developer answered.
- Push, open a pull request, or merge.
- Run `/phil:done` or close the card.
- Post a step comment for a step the run did not finish.
- Name the card after a closing keyword in the commit.

## Why this fixture exists

AC2.2 and the slice 02 dogfood: the run carries a card through every step before landing, takes the recommendation, records each step's decisions on the card, and stops before the first landing step.
