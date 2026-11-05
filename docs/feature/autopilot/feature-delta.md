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
  "The agent types no credential".
- **Claude Code asks before an outward or hard-to-reverse action** "unless durably authorized or
  explicitly told to proceed without asking". This repo's path ends in a push, a pull request, a
  merge on a green pipeline and `/phil:done`.

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
  `/phil:start` at the front, the routes the build path names in the middle, and `/phil:done` at the
  end; it stops through `/phil:handoff`.
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

- **[D3] Test sign-in comes from a source the repo declares.** *(Developer's answer.)* The repo names
  where test sign-in comes from, never the secret. A declaration that a person signs in, as beatrix's
  does, makes that check a blocker of D1's second kind. A missing declaration is a blocker only when
  the work needs the running product. The run never searches for a credential and never invents one.

- **[D4] Starting the run authorizes every write the build path names.** *(Developer's answer.)* That
  covers commits, the push, the pull request, the merge on a green pipeline and `/phil:done`'s close
  and cleanup. The yes is implied, so the run records it: its first comment on the card lists the writes
  the path authorizes. A write the path does not name is a blocker (D1). A recorded rule still binds the
  run — here, a merge needs a passing pipeline, and a red main stops the line.

- **[D5] Autopilot composes the commands that already own each step.** `/phil:start` claims the card
  and cuts the worktree; each step of the path launches the command or skill that owns it; `/phil:done`
  closes the card. A card already underway resumes from its snapshot, as `/phil:resume` reads it, and
  continues at the next step.

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

- **[D10] GitHub and GitLab.** Slices 01–05 cover GitHub; slice 06 adds GitLab, taking the mechanics
  from `phil:issue-board`. Until slice 06 lands, the command says it covers GitHub only and stops on
  GitLab with a named outcome (CLAUDE.md, decided 2026-11-03).

- **[D11] `commands/autopilot.md` declares `mutates: true`** — it writes to the forge and git
  (`scripts/check-readonly-commands.py`).

- **[D12] Open for slice 02: how the run answers a launched route's questions.** Every route the path
  names asks through the question tool. A pre-slice spike settles how the run answers those asks itself
  and stops on a blocker. One fact bears on it: the decision-request `PreToolUse` hook already receives
  every ask's question and options before the call runs.

## Wave: DISCUSS / [REF] User stories

### Story 1 — See the path the run read *(slice 01)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want the run to show the steps it read from my repo, each beside its source line,
before it does anything, so I can catch a misreading of prose no check can verify.

### Elevator Pitch
Before: nothing says which build path an agent will follow; it follows the nWave waves because the directories exist, or whatever it remembers.
After: run `/phil:autopilot 76` → sees `PATH (CLAUDE.md, "Build path for this plugin"): 1 nw-discuss — "Run nw-discuss before authoring…" · 2 author after plugin-dev · … · 9 /phil:done`, then `AUTHORIZED: push, pull request, merge on green, close`.
Decision enabled: I let the run go on, or stop it because it read my path wrong.

**Acceptance criteria**
- AC1.1 — Given a repo whose `CLAUDE.md` declares a build path and which holds `.nwave/` and
  `docs/feature/`, then the run prints the declared path, not the nWave waves.
- AC1.2 — Given a repo with no declared path, then the run says it fell back and names the fallback
  and the rule that chose it.
- AC1.3 — Given any path, then each step is printed beside the line it came from, quoted in its own
  words.
- AC1.4 — Given any path, then the run lists the writes the path authorizes before the first step.

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
After: run `/phil:autopilot 76` → sees `BLOCKED: the in-browser check needs a person to sign in (CLAUDE.md: "The agent types no credential") — described on the card; snapshot written; next: /phil:autopilot 76`.
Decision enabled: I clear the blocker, then restart the run from where it stopped.

**Acceptance criteria**
- AC3.1 — Given a blocker, then the run writes a card comment naming it and its kind, runs
  `/phil:handoff`, and ends with the blocked outcome.
- AC3.2 — Given a card stopped on a blocker, then the next run resumes at the step that stopped, not
  at the first.
- AC3.3 — Given a write the path does not name, including filing a new card, then the run stops
  before making it.

### Story 4 — Land the work *(slice 04)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want the run to push, open the pull request, merge once the pipeline passes and close
the card through `/phil:done`, keeping the card current at each step, so a card finishes without me
when nothing needs me.

### Elevator Pitch
Before: the work is done, and I still push, open, wait, merge, and close by hand.
After: run `/phil:autopilot 76` → sees `LANDED: pull request 112 merged on a green pipeline; card closed by /phil:done — 9 steps, 14 decisions recorded, 0 stops`.
Decision enabled: I read the recorded decisions and overturn any I disagree with.

**Acceptance criteria**
- AC4.1 — Given a path naming push, pull request and merge, then the run makes each write without an
  ask, after recording the authorization on the card (D4).
- AC4.2 — Given a red pipeline, then the run never merges; a failure it cannot fix within its attempts
  is a blocker.
- AC4.3 — Given each step boundary, then the card's `wave:` label, generated block and Status match the
  step (D7).

### Story 5 — Check the running product with declared sign-in *(slice 05)*
`job_id: carry-a-card-hands-off`

As **Rowan**, I want the run to check a change to a running product in the browser, signing in as the
repo declares, so a product change is verified without me unless only I can sign in.

### Elevator Pitch
Before: an in-browser check waits for me to sign in, or an agent goes looking for a password.
After: run `/phil:autopilot 58` in modive → sees `CHECKED in the browser as the test-tenant user (CLAUDE.md: "Test users live in a dedicated test tenant…") — 3 pages, 0 failures`.
Decision enabled: I trust the check, or open the evidence it left.

**Acceptance criteria**
- AC5.1 — Given work that changes a running product and a declared sign-in source, then the run checks
  it in the browser using that source and records the evidence.
- AC5.2 — Given work that needs the running product and no declaration, then the run stops on a
  blocker; given work that does not, then no declaration is needed.
- AC5.3 — Given a declaration that a person signs in, then that check is a blocker.
- AC5.4 — Given any run, then it never searches for a credential or invents one.

### Story 6 — Carry a card on GitLab *(slice 06)*
`job_id: carry-a-card-hands-off`

As **Rowan** on a GitLab repo, I want the same run, so the forge is no reason to drive a card by hand.

### Elevator Pitch
Before: on modive, `/phil:autopilot 58` stops at once, because the command covers GitHub only.
After: run `/phil:autopilot 58` in modive → sees the same PATH, DECISIONS and LANDED lines, the merge request in place of the pull request.
Decision enabled: I hand a GitLab card over as I would a GitHub one.

**Acceptance criteria**
- AC6.1 — Given a GitLab forge line, then no run stops because the forge is GitLab.
- AC6.2 — Given any GitLab call, then it follows `phil:issue-board`'s GitLab mechanics, as
  `/phil:start`'s and `/phil:done`'s GitLab references do.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measurement |
|---|---|---|
| Stops only where needed | 0 stops outside D1's three kinds | fixture per kind; dogfood transcript |
| Nothing unseen | every taken recommendation is on the card | dogfood: card comments against the transcript's asks |
| Few calls overturned | ≤ 6 in 70 recorded calls overturned — today's override rate | developer's review of the card after dogfood |
| Declared path wins | 0 runs that follow nWave detection over a declared path | fixture (AC1.1) |
| No guessed credential | 0 credentials searched for or invented | fixture (AC5.4) |
| No unnamed write | 0 writes the path does not name | fixture (AC3.3) |
| Hands-off | a card on this repo runs from `/phil:autopilot` to `/phil:done` with no question that is not a blocker | dogfood transcript |
| Applied, not cited | removing the `rules/writing.md` citation fails a test | pytest, watched red first |

## Wave: DISCUSS / [REF] Out of scope

- Choosing which card to carry. `phil:board-snapshot` and `phil:rank-issues` own the order.
- Carrying several cards at once, or one card across machines.
- Changing the routes the path launches, beyond what D12's mechanism needs to answer their questions.
- A fixed build-path heading or declaration line (D2 chose prose).

## Wave: DISCUSS / [REF] Driving ports & prerequisites

- **Driving port:** `/phil:autopilot <card>`.
- **Driven ports:** `/phil:start`, `/phil:done`, `/phil:handoff`, `/phil:resume`; the routes the path
  names; `gh` (comments, labels, Status, pull requests, pipeline status); `git`; Chrome DevTools or
  Playwright for in-browser checks; the repo's `CLAUDE.md` and `AGENTS.md`; the developer's saved
  preferences.
- **Prerequisites:** `/phil:start` and `/phil:done` (both shipped); D12's spike before slice 02.

## Wave: DISCUSS / [REF] Walking-skeleton strategy

Slice 01 is the skeleton: `/phil:autopilot` claims the card through `/phil:start`, reads the path,
prints it with its sources and its authorized writes, records both on the card, and stops before the
first step. Slices 02–05 add the steps behind it.

## Wave: DISCUSS / [REF] Scope Assessment

**PASS (right-sized).** Six stories across six slices; one new command and skill; no change to an
existing command's behaviour. The largest risk, D12, gets a spike before slice 02.

## Wave: DISCUSS / [REF] Definition of Done

1. `commands/autopilot.md` and `skills/autopilot/SKILL.md` exist, authored after reading
   `plugin-dev:command-development` and `plugin-dev:skill-development`.
2. Every story traces to `carry-a-card-hands-off`.
3. Every story has an Elevator Pitch with a real entry point and observable output.
4. Fixtures pin issue 76's five behaviours: a taken recommendation is recorded on the card (AC2.2); a
   decision the developer must make stops the run (AC2.3); a blocker yields a card comment and a
   snapshot (AC3.1); a declared build path wins over nWave directories (AC1.1); a missing credential
   declaration blocks only when the work needs the running product (AC5.2).
5. Every new citation and gate has a test, watched red first.
6. `python3 -m pytest -q` and `scripts/check-invariants.py` pass.
7. `/phil:harden-instructions` over the command, the skill and its references; `phil:eos` over this
   file, its slice briefs and the SSOT entries; `plugin-dev:skill-reviewer` and
   `plugin-dev:plugin-validator` over the command and skill — then the tests again.
8. Dogfood: `/phil:autopilot` carries the next card on this board to `/phil:done`, naming the plugin
   version it ran against.
9. The plugin version is bumped.

## Wave: DISCUSS / [REF] Definition of Ready — validation

| # | DoR item | Status | Evidence |
|---|---|---|---|
| 1 | Job traceable | ✅ | `carry-a-card-hands-off` in `jobs.yaml`; all 6 stories carry it |
| 2 | Persona defined | ✅ | `personas/rowan-skeptical-delegator.yaml`, hands-off facet |
| 3 | Journey mapped | ✅ | `journeys/autopilot.yaml`, with error paths |
| 4 | Elevator pitches | ✅ | all 6 stories, `/phil:autopilot` entry point, observable output |
| 5 | ACs testable | ✅ | Given-then, fixture- or pytest-checkable |
| 6 | Slices ≤1 day with a learning hypothesis | ✅ | `slices/slice-01` … `slice-06` |
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

## Wave: DISCUSS / [REF] Decisions summary (for authoring)

- **Key decisions:** D1 three kinds of blocker · D2 path read from prose, shown beside its sources ·
  D3 declared sign-in source · D4 starting authorizes the path's writes, recorded on the card · D5
  compose the commands that own each step · D6 each decision recorded on the card · D7 card current at
  each boundary · D8 blocker: comment, then handoff · D9 saved preferences are rules · D10 GitHub, then
  GitLab · D11 `mutates: true` · D12 answering a route's questions, settled by spike.
- **Requirements summary:** `/phil:autopilot` claims a card, reads the repo's build path and shows it,
  runs each step through the command that owns it, answers each question by rule or by its own
  recommendation and records the answer on the card, stops for three kinds of question, and lands the
  work through `/phil:done`.
- **Constraints:** never a write the path does not name; never merge red; never search for or invent a
  credential; never an unrecorded decision; never follow detection over a declared path.
