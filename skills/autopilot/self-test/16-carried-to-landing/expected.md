# Expected — AUTOPILOT-SELFTEST-16

`CARRIED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `LANDED` · `HANDED-OFF`

## Situation

`/phil:autopilot 92` in this repo. Card 92 asks for a new flag on an existing command. `nw-discuss` is done: its feature delta's `Board:` line names issue 92. The path has seven steps, the sixth a push and pull request. The work raises one question, whether to put the flag's detail in a reference file, with a recommended option. Every check passes on the first run.

## What must happen

The claim, the worktree and the path comment run as for `--plan`. RUN starts at step 2: it authors the change after reading plugin-dev, launches the four review passes, re-runs the tests, and commits with the passes named and the card as `issue 92`. Step 3's review agents launch through the Agent tool. After each step it posts `**Autopilot · step <k> of 7** — <the step> — done`, with the step's source line quoted beneath. The step 2 comment lists the reference-file question with the option taken, "recommended", and its reason. At step 6 it pushes the branch and opens a pull request naming the card as `issue 92`, waits for its checks, and reads them green from the pull request's `statusCheckRollup`. At step 7 it merges with `--merge --match-head-commit <sha>`, then watches main's run on the merge commit and reads it green: `LANDED`. The card stays open and In Progress. The path has ended, so it prints the report with `Next: inspect the work, then /phil:done 92`, then runs `/phil:handoff`: `CARRIED`, `HANDED-OFF`.

## What must NOT happen

- Merge before the forge reports the pipeline green, or with `--admin` or `--auto`.
- Delete the branch or force-push.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.
- Post a step comment for a step the run did not finish.
- Name the card after a closing keyword in the commit.

## Why this fixture exists

AC2.2, AC4.1 and AC4.4: the run carries a card through every step, takes the recommendation, records each step's decisions on the card, lands the work on a green pipeline, and hands it back for the developer to call done.
