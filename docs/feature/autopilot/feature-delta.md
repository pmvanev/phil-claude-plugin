# Feature Delta — autopilot (`/phil:autopilot`)

> Single narrative file for the feature. DISCUSS findings live here as
> `## Wave: DISCUSS / [REF|WHY|HOW]` sections. Machine artifacts: `slices/slice-NN-*.md`.
> SSOT updates: `docs/product/jobs.yaml` (new job), `docs/product/journeys/autopilot.yaml` (new
> journey), `docs/product/personas/rowan-skeptical-delegator.yaml` (facet added).
> Board: issue 76, In Progress.
> Build path: DISCUSS only — the deliverable is prose (CLAUDE.md, edd-loop DDD8).

---

## Wave: DISCUSS / [REF] Source

Issue 76 asks for a command that carries one card through every remaining step of its repo's build
path and stops only for a blocker that needs the developer. Driving a card today needs the developer at
every gate, and most answers are the agent's own recommendation, accepted unchanged.

Measured on 2026-11-05 over this repo's session transcripts, 2026-10-13 to 2026-11-05 — 18 sessions,
75 answered questions:

- **70 questions carried a recommended option; the developer took it unchanged 64 times (91%).**
- **Four of the six overrides were one call**: file a new card or extend the current one. The
  developer extended it each time, and a saved preference already records that rule ("No follow-up
  cards"). A recorded rule would have answered all four.
- **The other two turned on the developer's own material**: which writing samples a voice profile
  learns from, and whether private slips stay quoted in a public repo. No rule could have answered
  either.

Three facts, read the same day from the repos on this machine, shape the design:

- **No repo marks its build path with a fixed heading.** This repo writes it under "Build path for
  this plugin", beatrix under "Workflow", modive and harebrain under "Development paradigm".
  `/phil:start`'s route rule reads that prose.
- **Test sign-in differs in every repo that runs a product.** modive declares a test tenant created
  through the Cognito admin API; submission-tracker has none and renders markup instead; beatrix says
  "The agent types no credential". *Corrected 2026-11-06:* beatrix's line governs only the
  operator-assisted extension browser. beatrix keeps dev test accounts, and both beatrix and modive
  serve their web UI locally over recorded fixtures with no sign-in, through a documented dogfood
  command.
- **Claude Code asks before an outward or hard-to-reverse action** "unless durably authorized or
  explicitly told to proceed without asking". This repo's path ends in a push, a pull request and a
  merge on a green pipeline.

## Wave: DISCUSS / [REF] Persona & Job

- **Persona:** `rowan-skeptical-delegator`, with a hands-off facet. Rowan delegates work to agents and
  wants it checked before trusting it; here Rowan delegates a whole card and reviews the decisions
  afterwards, from the card.
- **JTBD one-liner:** *When I hand a card to the agent in a repo that records how its work gets built,
  I want it carried through every step without me at each gate — stopped only where my answer would
  change the outcome, and every call it made recorded on the card — so my attention goes to the
  decisions that need me.*
- **Job ID:** `carry-a-card-hands-off` (new).

## Wave: DISCUSS / [REF] Feature type & framing

- **Feature type:** developer tool, user-facing — the developer invokes `/phil:autopilot` and reads
  the card and the report it leaves.
- **New command** in a brownfield plugin: `commands/autopilot.md` and `skills/autopilot/`. It composes
  `/phil:start` at the front and the routes the build path names in the middle, and ends through
  `/phil:handoff`, leaving `/phil:done` to the developer.
- **Research depth:** lightweight — happy path plus the error paths in the journey. JTBD on. The
  developer answered D1–D4; the session settled the routine settings without an ask.

## Wave: DISCUSS / [REF] Locked decisions

The developer answered D1–D4 on 2026-11-05. The rest follow from those answers, the card and the
plugin's existing rules.

- **[D1] Three kinds of question stop the run.** *(Developer's answer.)* The run stops for:
  - an outward or irreversible write the build path does not name;
  - an input only the developer holds — their own material, an account, a secret, or a call the card
    reserves for them;
  - a check that still fails once the run has spent the fix attempts the skill allows.

  Recorded rules answer every other question: the repo's `CLAUDE.md` and `AGENTS.md`, and the
  developer's saved preferences. Where none does, the run takes its own recommendation and records it
  (D6). The cost the developer accepted: a call of taste that no rule covers goes through, recorded on
  the card for the developer to overturn.

- **[D2] The build path is read from the repo's prose.** *(Developer's answer; the recommendation was a
  fixed heading.)* The run reads the root's `CLAUDE.md` and `AGENTS.md` for the steps the repo runs for
  the card's kind of work, as `/phil:start`'s route rule 1 does. Nothing can check that reading, so the
  run shows it: before the first step it prints the steps in order, each beside the line it came from,
  and records the same list on the card. A declared path beats detection. With none declared, the run
  falls back to the nWave waves in an nWave repo, and to `phil:edd` or `phil:work` elsewhere, by
  `/phil:start`'s route rules 2 and 3, and says it fell back.

- **[D3] The run works out for itself how to dogfood a running product.** *(Developer's answer,
  2026-11-06; it replaces the 2026-11-05 answer, under which only a declared sign-in source let the run
  sign in.)* Where the work changes a running product, the run reads the repo for how it is dogfooded —
  `CLAUDE.md`, `AGENTS.md`, test-account documentation, dogfood guides and scripts — and follows the
  repo's own instructions. It takes the first way that works:
  1. the repo's test accounts and dogfood instructions;
  2. the product run locally, the way the repo's own dogfood guides run it;
  3. any other way the run can find.

  Where none works, the check is a blocker of D1's second kind: the blocker comment suggests
  documenting an automatic way forward, so the next run is not stopped the same way, and the run hands
  off. Work that changes no running product needs no check. The skill's prose does all of this; no
  hook and no script (the developer: "I don't know that we need hooks or crazy custom code"). The run
  signs in only with a credential the repo documents or provisions for testing, never invents one, and
  writes none onto the card.

- **[D4] Starting the run authorizes every write the build path names, except done (D13).**
  *(Developer's answer.)* That covers commits, the push, the pull request and the merge on a green
  pipeline. The yes is implied, so the run records it: its first comment on the card lists the writes
  the path authorizes. A write the path does not name is a blocker (D1). A recorded rule still binds the
  run — here, a merge needs a passing pipeline, and a red main stops the line.

- **[D5] Autopilot composes the commands that already own each step.** `/phil:start` claims the card
  and cuts the worktree; each step of the path launches the command or skill that owns it;
  `/phil:handoff` puts the run down (D13). A card already underway resumes at the first step neither
  the disk nor a step comment marks done, reading the snapshot for context (refined at slices 02–03).

- **[D6] Every taken recommendation is recorded on the card.** One comment per step of the path lists
  that step's decisions: the question, the option taken and the reason. This is a board surface that
  composes prose, so the skill names `rules/writing.md` and ships a fixture that fails without the
  citation (CLAUDE.md, "Board surfaces that compose prose").

- **[D7] The card stays current at every step boundary** — `wave:` label, generated block and Status —
  as `phil:nwave-issue-board` prescribes.

- **[D8] A blocker stops the run in two writes.** The run describes the blocker on the card, then runs
  `/phil:handoff`, so the next session resumes from the snapshot. It ends with a named outcome.

- **[D9] The developer's saved preferences are recorded rules.** Discovered work goes on the current
  card's checklist; filing a new card is a write the path does not name, so it is a blocker (D1). This
  rule alone would have answered four of the six measured overrides.

- **[D10] Every slice ships GitHub and GitLab together.** *(Developer's answer, 2026-11-05.)* Each slice
  takes both forges' mechanics from `phil:issue-board` and `/phil:start`'s GitLab reference. CLAUDE.md
  changed the same day: a surface never ships covering one forge. The separate GitLab slice is gone.

- **[D11] `commands/autopilot.md` declares `mutates: true`** — it writes to the forge and git
  (`scripts/check-readonly-commands.py`).

- **[D12] The skill's own prompt answers a launched route's questions; no hook.** *(Developer's call,
  2026-11-05, after the spike in `spike-d12/README.md`.)* The skill carries the developer's standing
  prompt, quoted below. A route's question takes the recommendation, recorded on the card as the run's
  (D6), unless it is one of D1's kinds. The instruction alone did this in a headless session and in an
  interactive one with the question tool present (spike rows 2 and 9). A run that loses the instruction
  leaves the question waiting for the developer, which costs time but makes no false record. The spike
  also showed that a `PreToolUse` hook that denies the ask works, and keeps it on file in case runs show
  the instruction failing. A hook that pre-fills `answers` must never ship: it reads as "User answered".

  The developer's standing prompt, verbatim:

  > proceed as independently as possible (through each wave if using nwave). keep the issue updated as
  > you go. only stop if a blocker absolutely requires me, in which case do a phil:handoff after
  > describing the blocker. clean up worktrees and branches as we finish with them. go with our
  > recommendations to questions/options that arise unless you feel I really need to weight in. use
  > chrome tools and known test credentials where possible to do your own walks/tests/checks.

  Its "clean up worktrees and branches as we finish with them" predates D13. Under D13 the cleanup
  is `/phil:done`'s, run by the developer after inspecting.

- **[D13] Done is the developer's.** *(Developer's answer, 2026-11-05.)* The developer inspects and
  approves the work before anything calls it done, so autopilot never runs `/phil:done` and never closes
  the card, even where the path names that step: it prints the step as the developer's and authorizes
  no close. When the run believes the work is finished, it runs `/phil:handoff` and ends, naming
  `/phil:done` for the developer to run after inspecting. A blocker ends the same way (D8).

## Wave: DISCUSS / [REF] User stories

### Story 1 — See the path the run read *(slice 01)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want the run to show the steps it read from my repo, each beside its source line,
before it does anything, so I can catch a misreading of prose no check can verify.

### Elevator Pitch
Before: nothing says which build path an agent will follow; it follows the nWave waves because the directories exist, or whatever it remembers.
After: run `/phil:autopilot 76` → sees `PATH: 1 nw-discuss (done) — CLAUDE.md, Build path for this plugin: "Run nw-discuss before authoring…" · 2 author after plugin-dev · … · 7 merge once its pipeline passes — CLAUDE.md, CI workflow`, then `AUTHORIZED: commit (step 5), push (step 6), pull request (step 6), merge once its pipeline passes (step 7)`.
Decision enabled: I let the run go on, or stop it because it read my path wrong.

**Acceptance criteria**
- AC1.1 — Given a repo whose `CLAUDE.md` declares a build path and which holds `.nwave/` and
  `docs/feature/`, then the run prints the declared path, not the nWave waves.
- AC1.2 — Given a repo with no declared path, then the run says it fell back and names the fallback
  and the rule that chose it.
- AC1.3 — Given any path, then each step is printed beside the line it came from, quoted in its own
  words.
- AC1.4 — Given any path, then the run lists the writes the path authorizes before the first step,
  and never a close (D13).
- AC1.5 — Given a GitLab forge line, then the run claims, prints and records as on GitHub (D10).

### Story 2 — Take the recommendation and record it *(slice 02)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want each question the path raises answered with the run's own recommendation, unless
a recorded rule answers it, and every answer recorded on the card, so the card holds every call made
for me to review.

### Elevator Pitch
Before: each wave ends on a question, and I answer 91% of them by taking the recommendation unchanged.
After: run `/phil:autopilot 76` → sees, on the card after each step, `DECISIONS (nw-discuss): Which questions stop the run? — took "Only three kinds": a recorded rule… · …`.
Decision enabled: I overturn a recorded call on the card, or let the run carry on.

**Acceptance criteria**
- AC2.1 — Given a question a recorded rule answers, then the run answers it by that rule and names the
  rule on the card.
- AC2.2 — Given a question no rule answers and that is none of D1's kinds, then the run takes its
  recommendation and records the question, the option and the reason on the card.
- AC2.3 — Given a question of one of D1's kinds, then the run stops (Story 3).
- AC2.4 — Given `skills/autopilot/SKILL.md` without its `rules/writing.md` citation, then a test fails.

### Story 3 — Stop on a blocker, leave it resumable *(slice 03)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want a blocker described on the card and the session put down with a snapshot, so I
answer it when I'm back and the next run picks up where this one stopped.

### Elevator Pitch
Before: a run that hits a question waits in a terminal nobody is watching, and its reasoning dies with the session.
After: run `/phil:autopilot 76` → sees `BLOCKED: no test account and no local way to run the page — described on the card, with a suggestion to document one; snapshot written; next: /phil:autopilot 76`.
Decision enabled: I clear the blocker, then restart the run from where it stopped.

**Acceptance criteria**
- AC3.1 — Given a blocker, then the run writes a card comment naming it and its kind, runs
  `/phil:handoff`, and ends with the blocked outcome.
- AC3.2 — Given a card stopped on a blocker, then the next run resumes at the step that stopped, not
  at the first.
- AC3.3 — Given a write the path does not name, including filing a new card, then the run stops
  before making it.

### Story 4 — Land the work and hand it back for inspection *(slice 04)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want the run to push, open the pull request and merge once the pipeline passes,
keeping the card current at each step, then put the session down for me to inspect, so the work lands
without me and nothing calls it done until I have looked.

### Elevator Pitch
Before: the work is done, and I still push, open, wait and merge by hand.
After: run `/phil:autopilot 76` → sees `LANDED: pull request 112 merged on a green pipeline — 7 steps, 14 decisions recorded, 0 stops; snapshot written; next: inspect, then /phil:done 76`.
Decision enabled: I inspect the work and the recorded decisions, then call it done or send it back.

**Acceptance criteria**
- AC4.1 — Given a path naming push, pull request and merge, then the run makes each write without an
  ask, after recording the authorization on the card (D4).
- AC4.2 — Given a red pipeline, then the run never merges; a failure it cannot fix within its attempts
  is a blocker.
- AC4.3 — Given each step boundary, then the card's `wave:` label, generated block and Status match the
  step (D7).
- AC4.4 — Given the run believes the work is finished, then it runs `/phil:handoff`, names
  `/phil:done` for the developer, and never runs `/phil:done` or closes the card itself (D13).

### Story 5 — Dogfood the running product without me *(slice 05)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want the run to work out from the repo how to check a change to a running product in
the browser, and check it, so a product change is checked without me, and a repo that leaves the run
no way gets a suggestion for one.

### Elevator Pitch
Before: an in-browser check waits for me to sign in, or nobody walks the page at all.
After: run `/phil:autopilot 58` in modive → sees on the card's step comment `walked 3 pages in the browser as the repo's test account (from its dogfood guide), 0 failures`.
Decision enabled: I trust the check, or open the evidence it left.

**Acceptance criteria**
- AC5.1 — Given work that changes a running product and a repo that documents test accounts or
  dogfood steps, then the run follows them, checks the change in the browser, and records the evidence
  on the card, naming where the sign-in came from and never the secret.
- AC5.2 — Given no test account the run can use, then it runs the product locally as the repo's own
  dogfood guides do and checks it there; given work that changes no running product, then no check
  runs.
- AC5.3 — Given no way the run can find to check the change, then the check is a blocker whose
  comment suggests documenting an automatic way forward, and the run hands off.
- AC5.4 — Given any run, then it signs in only with a credential the repo documents or provisions for
  testing, never invents one, and writes none onto the card.

GitLab is no story of its own: every story above ships on both forges (D10), and each slice's
acceptance criteria hold on GitLab with a merge request in place of a pull request and a note in place
of a comment.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| Stops only where needed | 0 stops outside D1's three kinds | fixture per kind; dogfood transcript |
| Nothing unseen | every taken recommendation is on the card | dogfood: card comments against the transcript's asks |
| Few calls overturned | ≤ 6 in 70 recorded calls overturned — today's override rate | developer's review of the card after dogfood |
| Declared path wins | 0 runs that follow nWave detection over a declared path | fixture (AC1.1) |
| No guessed credential | 0 credentials invented, taken from outside what the repo provides for testing, or written onto the card | fixture (AC5.4) |
| No unnamed write | 0 writes the path does not name | fixture (AC3.3) |
| Hands-off | a card on this repo runs from `/phil:autopilot` to a merged change and a handoff with no question that is not a blocker | dogfood transcript |
| Done is yours | 0 runs of `/phil:done`, and 0 cards closed, by autopilot | fixture (AC4.4) |
| Both forges | 0 runs that stop because the forge is GitLab | fixture (AC1.5) |
| Applied, not cited | removing the `rules/writing.md` citation fails a test | pytest, watched red first |

## Wave: DISCUSS / [REF] Out of scope

- Choosing which card to carry. `phil:board-snapshot` and `phil:rank-issues` own the order.
- Carrying several cards at once, or one card across machines.
- Changing the routes the path launches, beyond what D12's mechanism needs to answer their questions.
- A fixed build-path heading or declaration line (D2 chose prose).

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:autopilot <card>`.
- **Driven ports:** `/phil:start`, `/phil:handoff`, `/phil:resume`; the routes the path names; `gh`
  and `glab` (comments or notes, labels, Status, pull or merge requests, pipeline status); `git`;
  Chrome DevTools or Playwright for in-browser checks; the repo's `CLAUDE.md` and `AGENTS.md`; the
  developer's saved preferences.
- **Prerequisites:** `/phil:start` and `/phil:handoff` (both shipped, both forges); D12's spike before
  slice 02.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

Slice 01 is the skeleton: `/phil:autopilot` claims the card through `/phil:start`, reads the path,
prints it with its sources and its authorized writes, records both on the card, and stops before the
first step. Slices 02–05 add the steps behind it.

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** Five stories across five slices, each on both forges; one new command and
skill; no change to an existing command's behaviour. The largest risk, D12, gets a spike before slice
02.

## Wave: DISCUSS / [REF] Definition of Done

1. `commands/autopilot.md` and `skills/autopilot/SKILL.md` exist, authored after reading
   `plugin-dev:command-development` and `plugin-dev:skill-development`.
2. Every story traces to `carry-a-card-hands-off`.
3. Every story has an Elevator Pitch with a real entry point and observable output.
4. Fixtures pin issue 76's five behaviours: a taken recommendation is recorded on the card (AC2.2); a
   decision the developer must make stops the run (AC2.3); a blocker yields a card comment and a
   snapshot (AC3.1); a declared build path wins over nWave directories (AC1.1); a change to a running
   product is checked in the browser by the first way that works, and blocks only when none does
   (AC5.1–AC5.3).
5. Every new citation and gate has a test, watched red first.
6. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
7. `/phil:harden-instructions` over the command, the skill and its references; `phil:eos` over this
   file, its slice briefs and the SSOT entries; `plugin-dev:skill-reviewer` and
   `plugin-dev:plugin-validator` over the command and skill — then the tests again.
8. ~~Dogfood runs on this board and on modive.~~ Dropped 2026-11-06 by the developer: "we don't need
   dogfood runs".
9. The plugin version is bumped.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | `carry-a-card-hands-off` in `jobs.yaml`; all 5 stories carry it |
| 2 | Persona defined | ✅ | `personas/rowan-skeptical-delegator.yaml`, hands-off facet |
| 3 | Journey mapped | ✅ | `journeys/autopilot.yaml`, with error paths |
| 4 | Elevator pitches | ✅ | all 5 stories, `/phil:autopilot` entry point, observable output |
| 5 | ACs testable | ✅ | Given-then, fixture- or pytest-checkable |
| 6 | Slices ≤1 day with a learning hypothesis | ✅ | `slices/slice-01` … `slice-05` |
| 7 | Walking skeleton | ✅ | slice 01 |
| 8 | Outcome KPIs with targets | ✅ | table above |
| 9 | Scope right-sized | ✅ | Scope Assessment above |

Requirements completeness: each of issue 76's seven *What it does* items, two *Done when* items and
four open questions maps to a decision and an AC.

## Wave: DISCUSS / [REF] Changed Assumptions

DISCOVER and DIVERGE never ran; the changed assumptions are issue 76's own, as written.

- Open question 2: "A heading or a line can be checked; prose cannot."

  **New:** the path is read from prose (D2). **Why:** the developer chose prose over a fixed heading,
  so no repo has to change. The run prints its reading beside the source lines, so a misreading is
  visible even though it cannot be checked.

- What it does, item 3: "It asks only where the developer's judgement would change the outcome."

  **New:** three kinds of question stop the run (D1). **Why:** "would change the outcome" cannot be
  judged before the answer exists; the three kinds can. With D9's saved preferences, they account for
  all six measured overrides: the preferences answer four, and the developer's own material stops the
  other two.

- What it does, item 6: "Cleans up each worktree and branch once its work merges, through `/phil:done`
  (#75)."

  **New:** autopilot never runs `/phil:done` (D13). **Why:** the developer inspects and approves the
  work before anything calls it done; the run ends with a handoff that names `/phil:done` for them.

## Wave: DISCUSS / [REF] Decisions summary (for authoring)

- **Key decisions:** D1 three kinds of blocker · D2 path read from prose, shown beside its sources ·
  D3 the run works out how to dogfood a running product · D4 starting authorizes the path's writes, recorded on the card · D5
  compose the commands that own each step · D6 each decision recorded on the card · D7 card current at
  each boundary · D8 blocker: comment, then handoff · D9 saved preferences are rules · D10 both forges
  in every slice · D11 `mutates: true` · D12 answering a route's questions, settled by spike · D13
  done is the developer's.
- **Requirements summary:** `/phil:autopilot` claims a card, reads the repo's build path and shows it,
  runs each step through the command that owns it, answers each question by rule or by its own
  recommendation and records the answer on the card, stops for three kinds of question, lands the
  work, and hands it back through `/phil:handoff` for the developer to inspect and call done.
- **Constraints:** never a write the path does not name; never merge red; never invent a credential or
  write one onto the card; never an unrecorded decision; never follow detection over a declared path.
- **Settled at slice 01 authoring (2026-11-05)**, after `plugin-dev:skill-reviewer` and
  `plugin-dev:plugin-validator`:
  - The nWave fallback needs a `wave:` label, as `/phil:start`'s route rule 2 and
    `phil:nwave-issue-board` say. An unlabelled card falls to rule 3 (fixture 10).
  - A step has run where the repo holds its output for the card: for `nw-discuss`, a feature delta
    whose `Board:` line names the card. The path marks it `done` and names the next step, which gives
    slice 03 its resume point.
  - The path comment starts with the fixed line `**Autopilot · build path**`. A rerun compares only the
    quoted lines, the `done` marks and the authorized step numbers, because the labels the run composes
    differ run to run (fixture 04).
  - Wherever `/phil:start`'s text ends the run `UNDERWAY` or names `/phil:resume`, DESCRIBE or ROUTE as
    next, autopilot goes on to PATH. A card underway with no worktree here cuts nothing and says so
    (fixture 11).
  - Loaded from a question rather than the command, the skill prints the path and writes nothing.
  - This repo's own path names no `/phil:done`. Raised with the developer, it led to D13: autopilot
    never calls a card done, whatever the path names.
  - The first cut covered GitHub only. The developer answered that every surface ships both forges, so
    slice 01 ships GitLab too, through `/phil:start`'s GitLab reference and `glab issue note` (D10), and
    CLAUDE.md changed the same day.
- **Settled at slices 02 and 03 authoring (2026-11-05)**:
  - Slices 02 and 03 ship together. The developer's standing prompt, carried verbatim (D12), names
    the handoff on a blocker, and a skill that kept only half of it would mislead.
  - A plain run carries the card. `--plan` keeps slice 01's behaviour: print and record the path, run
    nothing.
  - The run stopped before the first landing step until slice 04 (superseded below). Steps run under the session's own permissions; the command's
    grant holds only autopilot's own calls, as `/phil:start`'s inline route does.
  - A question is decided by a recorded rule, then D1's three kinds, then the recommendation. The run
    never calls the question tool, and never writes that the developer answered.
  - A check is a circuit breaker, `k = 2`: two fixes that leave it failing make a blocker.
  - A step comment marks its step done, and the next run starts at the first step neither the disk nor
    a comment marks done. A blocker stands until a later comment, or words after the card in the
    argument, answer it.
  - D9 refined: the run cannot edit the card's body, so work it finds beyond the card goes in the step
    comment under `- Found:`, for the developer to place.
  - D13 holds: a run that reaches the path's end, or only `(yours)` steps, hands off and names
    `/phil:done` for the developer.
  - The skill's run and record detail moved to `references/run.md` and `references/record.md`,
    keeping the body under 2,000 words.
  - **D1 widened, after `plugin-dev:skill-reviewer`:** an approval a launched route reserves for the
    developer, such as `phil:edd`'s verdicts and `phil:work`'s approve-or-reject, counts as an input
    only the developer holds, and so does a permission the session denies. Otherwise a fallback run
    would adjudicate its own evidence (fixture 25).
  - Every run that reaches RUN prints its report, then hands off as its last act, since
    `/phil:handoff`'s recorded exchange ends the turn.
  - Agents named by a path, such as this repo's review passes, launch through the Agent tool.
  - A step that mixes work and landing does the work, commits it, and leaves the landing; its step
    comment reads `— work done, landing left`, and a later run lands it.
  - The AUTHORIZED line lists only the writes that leave the machine. Commits in the card's worktree
    belong to the work.
  - A step comment quotes its source line, and marks its step done only while the path gives that step
    the same line. The path comment's comparison ignores `done` marks, because progress lives in the
    step comments.
- **Settled at slice 04 authoring (2026-11-05)**, from `gh` 2.97.0's and `glab` 1.112.0's help, and
  both plugin-dev reviews. The landing lives in `references/land.md`.
  - D7 refined against D13: after each wave, `phil:nwave-issue-board` moves the label and the block
    only, never the column, and the run reads the Status back. Otherwise the fold after the last wave
    sets Done, and this board's Auto-close closes the card (fixture 31).
  - `glab mr merge` sets auto-merge by default, so the run always passes `--auto-merge=false`.
  - A pipeline judges a commit only where its commit is the request's head and local `HEAD`. GitLab's
    `head_pipeline` lags a push.
  - Before merging, the run reads the default branch's head (red blocks, fixture 34) and the request's
    closing references, commits, title and body (a reference that would close the card blocks,
    fixture 32).
  - The wait is bounded: `timeout: 600000` per call, absent after 10 minutes, stuck after 60.
  - The default branch is judged on the merge commit itself, never the request's pipeline. A default
    branch that runs no pipeline lands on the request's green.
  - Landing is autopilot's own call, in five moves: push, open the request (or reuse the open one),
    wait for its pipeline, merge on green, watch the default branch. It lands only the writes the path
    names, so a fallback path lands nothing.
  - Green is read from the forge — GitHub's `statusCheckRollup`, GitLab's `head_pipeline.status` —
    never from a wait command's exit code. The merge names the head commit the run judged
    (`--match-head-commit`, `--sha`).
  - A request with no pipeline is a blocker, because "merge once its pipeline passes" cannot be met. A
    red pipeline is a check, circuit breaker `k = 2`. A red default branch after the merge is a
    blocker, citing the repo's stop-the-line rule where it has one.
  - No `--force`, `--admin` or `--auto`, and no `--delete-branch` or `--remove-source-branch`. The first
    three skip or hand off the check the merge waits for; the last two take `/phil:done`'s cleanup.
  - D7 runs through its owner: after each nWave wave, the run launches `phil:nwave-issue-board` to move
    the `wave:` label and regenerate the block. The Status stays In Progress.
  - `LANDED` reports a merge read back merged with the default branch read green.
