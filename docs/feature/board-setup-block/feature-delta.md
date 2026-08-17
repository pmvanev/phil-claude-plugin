# Feature Delta — board-setup-block

Forge: #32 · Wave: DISCUSS ✓ (2026-08-14)
Density: lean + ask-intelligent (`~/.nwave/global-config.json`; the resolver script is absent from this
install, so the documented cascade default was applied rather than computed — stated rather than implied)

**Build path:** DISCUSS here, then authored with `plugin-dev` — not DESIGN/DISTILL/DELIVER. The
deliverable is a command plus prose, and this repo settled twice that skills are authored rather than
waved (`todo.md` 2026-06-17; edd-loop DDD8). Same path `groom-issues`, `session-handoff` and
`single-issue-per-feature` took.

**Route 3 per `CLAUDE.md` *Where a finding about a standard goes*.** The finding — that
`phil:issue-board`'s *Per-project setup* template has no author — changes neither a single skill's
assertion nor a repo convention. It is work, and it exceeds a paragraph.

---

## Wave: DISCUSS / [REF] Persona ID

**`robin-backlog-curator`** — extended, not replaced. Registered at
`docs/product/personas/robin-backlog-curator.yaml`, bootstrapped by `groom-issues` (2026-08-12).

Robin already *owns an issue board that other people — and a past self — also file into, and pays when a
card turns out to mean something other than what it said*. This feature is the same human one step
earlier: before a card can mean what it says, the board's own constants have to be known, and Robin is
the person who pays when they are not.

**A ninth persona was considered and rejected** ([D2] alternatives). The actor could be framed as an
*adopter* standing the plugin up on a new repo, which is the framing #32 leads with — "the point is the
next repo". But the adopter and the curator are the same human at t=0 and t=1, and minting a persona
whose only distinction is *when* they act creates two files that must be kept in agreement about one
person's goals. Robin's file gains a setup facet instead.

Robin's existing mental model already contains the load-bearing line: *"anything irreversible is mine to
decide, not the tool's."* This feature's central refusal — never infer a label family — is that line
applied one layer down, to a declaration rather than a card.

## Wave: DISCUSS / [REF] JTBD one-liner

When Robin points the plugin's board tooling at a repo whose forge instance nobody has operated before,
Robin wants everything discoverable to be discovered and everything undiscoverable to be asked — each
written down and labelled with which it was — so the instance's hazards are learned from a file rather
than from a call that reported success while doing the wrong thing.

Registered as a new validated job `know-a-boards-hazards-before-contact` in `docs/product/jobs.yaml`,
with a setup facet added to `keep-a-backlog-trustworthy`.

## Wave: DISCUSS / [REF] Locked decisions

- **[D1]** Feature type = **user-facing**. A developer-invocable slash command over one new skill, plus
  an addition to `phil:issue-board`'s template section. One surface, not six — narrower than
  `single-issue-per-feature`. (Session)
- **[D2]** **New job, existing persona.** `know-a-boards-hazards-before-contact` is a distinct outcome
  from `keep-a-backlog-trustworthy` — that job is about what a *card* means, this one is about whether
  the *instance* will do what the call says — but it is Robin's, and no new persona is minted. (User)
- **[D3]** **Driving port = a new `/phil:*` command.** Not a mode on `/phil:groom-issues`: grooming's
  own journey makes it a reporter that fixes only the mechanical, and giving the command that *detects*
  the missing declaration the power to *write* it collapses a separation the grooming feature spent four
  slices establishing. (User)
- **[D4]** **Delimited region for probed facts only.** Probed constants live inside generated,
  timestamped markers. Elicited decisions and human prose live **outside** the markers and are never
  written, moved or rewritten. A re-run refreshes only what is inside, and **reports** drift it detects
  outside without fixing it. This is `nwave-issue-board`'s generated-block discipline (C2) applied to a
  file that is mostly hand-written — the inverse of an issue description, where nothing human belongs.
  (User)
- **[D5]** **Three categories, not two.** #32's design point names *probeable facts* and *human
  decisions*. Probing the real board on 2026-08-14 found a third: **partially probeable**.
  `projectV2 { workflows { name enabled } }` returns `Auto-close issue: enabled` — so the hazard this
  repo learned by being bitten *is* discoverable — but introspection of `ProjectV2Workflow` shows it
  exposes `createdAt, enabled, fullDatabaseId, id, name, number, project, updatedAt` and **not** the
  configured trigger statuses. "A status→close workflow is on" is probed; "`Done` fires it" is not.
  Every such value is written as an **assumption, labelled as one**, with a confirm offer.
  (Session, evidenced 2026-08-14 — see *Evidence* below)
- **[D6]** **Never infer a declaration from the board's contents.** The labels in use may be shown as
  *evidence beside a question*; they may never be adopted as the answer. Inferring a label family makes
  the board's habits audit themselves, which `groom-issues` forbids in as many words, and would mint
  precisely the declaration rule 4 was supposed to read. (Card; inherited from `groom-issues` anxiety E)
- **[D7]** **Walking skeleton = yes**, WS strategy **C — real local resources**. Slice 01 probes the
  real board and writes a real region. A faked forge adapter answers a question nobody asked: the whole
  uncertainty is whether the *discoverable set is large enough to be worth a command*. (User)
- **[D8]** Research depth **comprehensive** — full journey, emotional arc, shared-artifact registry,
  error-path map. The value of this feature lives in its error paths (a stale option id, a declaration
  that disagrees with the labels in use), so specifying them without mapping them would specify the
  fixtures #32 demands with no failure mode behind them. (User)
- **[D9]** **Scope is the repo you are in.** The command writes one `CLAUDE.md` — the one in the working
  tree — and never a sibling checkout. Naming a target repo is `phil:issue-board`'s first rule for
  *forge* calls, and it stays that: the forge target is confirmed, the file target is not negotiable.
  (Session)
- **[D10]** **Both forges are in the feature; GitHub ships first.** `phil:issue-board` is deliberately
  forge-neutral, and a GitHub-only command leaves rule 4 dark on every GitLab repo — the exact defect
  #32 exists to close, half-closed. GitLab is slice 06, not an omission. Recorded here because "later
  slice" and "out of scope" are indistinguishable once a feature ships. (Session)
- **[D11]** **The command declares `mutates: true`.** It writes `CLAUDE.md` and holds `Write`/`Edit`.
  Per `CLAUDE.md`'s standing rule the declaration is a claim about the *grant*, not the intent; the
  intent — that it never writes to the forge, only reads it — is carried in the skill's prose.
  (Session)

## Wave: DISCUSS / [REF] Evidence — the probe, run against the real board

Run 2026-08-14 against user project 3, before any artifact was written. Two calls, both cheap:

```
gh api graphql -f query='{ user(login:"pmvanev"){ projectV2(number:3){
  workflows(first:20){ nodes { id name enabled } } } } }'
→ Auto-add sub-issues to project  enabled
  Auto-close issue                enabled
  Item added to project           enabled
  Item closed                     enabled
  Pull request linked to issue    enabled
  Pull request merged             enabled

gh api graphql -f query='{ __type(name:"ProjectV2Workflow"){ fields { name } } }'
→ createdAt · enabled · fullDatabaseId · id · name · number · project · updatedAt
```

Three findings, all load-bearing:

1. **`phil:issue-board` is right and incomplete.** Its claim that the workflows are "not visible in the
   project's field schema" is true — and the API exposes them elsewhere, which the skill does not say.
   A **route 1 fold-back** into `skills/issue-board/SKILL.md` with a fixture, per `CLAUDE.md`.
2. **`Item closed` is enabled on this board and this repo's `CLAUDE.md` never said so.** Closing an
   issue from the CLI sets Status=Done. Six weeks of hand-maintained hazards recorded only the forward
   direction. Written to `CLAUDE.md` on 2026-08-14 at the user's instruction — the sharpest available
   demonstration of the card's premise, produced by the probe on its first run.
3. **[D5]'s third category is real, not hypothetical.** The most dangerous constant in the template is
   exactly the one that comes back half-known.

## Wave: DISCUSS / [REF] Evidence — the authoring run, 2026-08-17

Three further findings, all from running the real probe while authoring slice 01. Each changed the
script rather than being noted after it:

1. **`repository.projectsV2` is EMPTY on this repo, and the board exists.** User project 3 is not
   linked to the repository, so the owner-level fallback is the path that actually runs — not a safety
   net. The probe records *how* the board was found, because that is itself a constant: a repo with no
   project link is a repo where `gh project item-add` is the only way a card ever reaches the board.
   Had the probe used only the repo-linked route, it would have reported *this repo has no board*.
2. **`projectV2.views` exposes `layout`**, so `TABLE_LAYOUT` / `BOARD_LAYOUT` is probed and *which view
   is the kanban* stops being remembered. `CLAUDE.md`'s hand-written "view 2 is the kanban (view 1 is
   the table)" is now reproducible. The layout is the fact; the friendly name a human gives a view is
   not — the views are literally titled "View 1" and "View 2".
3. **Every id the probe returned matches the hand-written block byte-for-byte** — project
   `PVT_kwHOANPp-M4Bf-px`, Status field `PVTSSF_lAHOANPp-M4Bf-pxzhaNnGs`, and all four option ids. The
   constants this repo learned by injury are exactly the constants one call returns, which is slice
   01's hypothesis confirmed against the thing itself rather than argued.

**A fourth finding arrived unbidden: GitHub's GraphQL API returned HTTP 503 mid-run**, repeatedly. The
script refused with exit 1 and wrote nothing, which is the designed behaviour exercised by accident
rather than by fixture. It also settled a design question in passing — the probe **refuses rather than
retries**, because a probe that quietly retries can mask a forge that is genuinely unwell, and the
caller is a human who can run the command again.

## Wave: DISCUSS / [REF] Scope assessment

**PASS — right-sized.** One oversized signal of five fires:

| Signal | Result |
|---|---|
| >10 user stories | ✗ — six |
| >3 bounded contexts or modules | ✗ — one command, one skill, one template section |
| Walking skeleton needs >5 integration points | ✗ — three: the git remote, the forge API, `CLAUDE.md` |
| Estimated effort >2 weeks | ✗ |
| Multiple independent outcomes that could ship separately | **✓** — GitHub and GitLab could ship apart |

The single firing signal is answered by [D10] and slice 06 rather than by a split: two forges of one
command is one outcome delivered twice, not two outcomes.

## Wave: DISCUSS / [REF] Story map — backbone

```
Point it at a repo  →  Discover what can be discovered  →  Ask what cannot  →  Write it down  →  Re-run it
      │                          │                              │                    │              │
  confirm the             tier · project · Status         label families      inside the       report what
  forge target            field · option ids ·            (evidence shown,    markers only     changed, and
  (never infer)           enabled workflows ·             never adopted)      (never outside)  "unchanged"
                          docs root · nWave-ness          + confirm the                        honestly
                                                          assumptions
```

## Wave: DISCUSS / [REF] Slices and order

| # | Slice | Ships | Hypothesis it can disprove |
|---|---|---|---|
| 01 | Probe and write, on a repo with no block *(skeleton)* | end-to-end probe → region | **the whole feature**, if the discoverable set is too thin to be worth a command |
| 02 | Coexist with prose the probe cannot regenerate | placement + drift report + migration offer | the delimited-region model, if the region cannot be placed without duplicating or orphaning |
| 03 | Elicit what no forge records | the label-family question | the elicitation design, if Robin cannot answer from the evidence offered |
| 04 | The assumed category | assumption labels + confirm offer | [D5]'s taxonomy, if no reader can tell an assumption from a fact |
| 05 | Staleness and safe re-run | change report, refusals | safe re-runnability, if a second run churns the file |
| 06 | GitLab | the `glab` probe equivalents | forge-neutrality, if the block's *shape* must differ, not just its values |

**Order rationale — highest learning leverage first.** 01 is first because everything downstream assumes
the probe pays for itself and nothing has ever measured that; a failure there costs one slice rather than
six. 02 second because the delimited-region model ([D4]) is the second-largest untested commitment and
this repo is the hardest available case for it. 03 and 04 are the human half, and 04 follows 03 because
its confirm-offer reuses the question machinery 03 ships. 05 needs something to re-run. 06 last: it is
the widest in surface and the narrowest in learning — by then the shape is settled and only the calls
change.

`Order: slice number — final; /nw-roadmap does not run in this repo.`

**Carpaccio taste tests.** No slice ships four or more new components. The abstraction everything
depends on — the probe — ships **first, as its own slice**, rather than being assumed by all six. Three
slices can disprove a pre-commitment (01, 02, 04), so the slicing is discipline rather than decoration.
No slice runs on synthetic data: every one runs against the real board. No two slices differ only by
scale — 01 and 02 differ by whether hand-written prose is present, which is a different case, not a
bigger one.

## Wave: DISCUSS / [REF] WS strategy

**C — real local resources** ([D7]). Slice 01 reads the real forge and writes a real `CLAUDE.md`.

The cost is a real write to a real file, mitigated by the target: a repo with **no** `## Issue board`
section, so nothing hand-written is at risk on the run that has the least machinery protecting it. The
existing-prose case is deliberately held back to slice 02, once refusal behaviour exists.

## Wave: DISCUSS / [REF] Driving ports

| Port | Surface | Change |
|---|---|---|
| `/phil:board-setup` | **New** command + new skill | The whole feature. `mutates: true` ([D11]) |
| `phil:issue-board` | Skill (knowledge-only) | *Per-project setup* gains the probed/elicited/assumed split and the marker convention; a route-1 fold-back records that `projectV2.workflows` is readable, with a fixture |
| `phil:groom-issues` | Command | **No change.** Rule 4 keeps reporting `unevaluated`; what changes is that its input now has an author ([D3]) |

The command name is provisional — `plugin-dev:command-development` owns naming and frontmatter, and is
consulted before the file is written, per the build path.

## Wave: DISCUSS / [REF] Journey

Full journey at `docs/product/journeys/board-setup-block.yaml`.

Robin runs the command in a repo. The forge target is derived from the git remote and **confirmed rather
than inferred** — `#12` exists in every repo, so an inferred remote mutates the wrong one successfully.
One probe pass returns the tier, the project, the Status field, its option ids, the enabled workflows and
the docs root, each reported beside the call that found it. The repo's `CLAUDE.md` is read: fresh,
configured, or configured-and-stale. Only then is Robin asked anything, and only for what no forge
records — with the labels in use shown as evidence and never as an answer. The region is written between
markers; everything outside them is left exactly as it was, and anything outside that the probe now
contradicts is **reported, not corrected**. The closing report separates what was probed, what Robin
declared, and what is assumed.

Arc: `wary → relief → recognition → control → ownership → trust → confidence` (upward).

**The accepted cost**, recorded in the journey's error paths: a declaration Robin declines is not
written, and rule 4 keeps reporting `unevaluated` for that family. The command says so plainly rather
than letting silence read as success — the same accepted cost `groom-ask` carries for a declined card,
and for the same reason: no marker is stored, so nothing can lie later.

## Wave: DISCUSS / [REF] User stories

Every story traces to `job_id: know-a-boards-hazards-before-contact`.

### S1 — Stand up a board's constants without looking any of them up

As Robin, I get a repo's board constants written down without opening the forge UI or copying an id.

**Elevator Pitch**
Before: the constants arrive by hand, one at a time, as each is discovered — and six of the seven
entries in this repo's own block were written *after* the thing they document had already gone wrong.
After: run `/phil:board-setup` → sees a `## Issue board` section written into `CLAUDE.md` containing the
forge and repo, the project id, the Status field id, every option id, the tier and the enabled
workflows — each line naming the call that produced it, inside timestamped markers.
Decision enabled: whether the block is complete enough to operate the board from, or which specific
lines still need a human.

AC1 — Every value inside the markers is accompanied by the query that produced it; no value inside the
markers was typed by a human.
AC2 — The command never asks for a value it could have probed; a run against a reachable board asks
zero questions in this story's scope.
AC3 — The forge target is confirmed with the user before any call is made; a repo with two remotes, or
a fork, produces a question rather than a guess.
AC4 — Of the fields in `phil:issue-board`'s *Per-project setup* template, at least half are populated
without human input (KPI-1).

### S2 — Add generated constants to a repo whose block is already hand-written

As Robin, I run it on a repo that already has an `## Issue board` section full of prose, and nothing I
wrote is disturbed.

**Elevator Pitch**
Before: a generator either has to be kept away from a configured repo, or it overwrites hazards nobody
can regenerate — this repo's block is mostly prose recorded after contact and no probe can reproduce a
line of it.
After: run `/phil:board-setup` on this repo → sees the marked region inserted into the existing section
with every hand-written bullet byte-identical, plus a report naming which existing lines the probe
**confirms**, which it **contradicts**, and which it **cannot evaluate**.
Decision enabled: whether to accept the offer to retire a superseded hand-written line, or keep it.

AC1 — Content outside the markers is byte-identical before and after, on every path including failure.
AC2 — A hand-written line stating a fact the region now owns, and disagreeing with it, is reported as a
contradiction and is **not** edited.
AC3 — Retiring such a line happens only on an explicit answer; silence is not consent, and a declined
offer leaves no trace.
AC4 — A section with a `begin` marker and no `end` marker is refused, with the file unchanged — the
region's extent is never guessed.

### S3 — Declare what the forge cannot record, without the tool guessing it

As Robin, I answer the questions no forge can answer, and see my answer written as mine.

**Elevator Pitch**
Before: `phil:groom-issues` rule 4 reads a label-family declaration that nothing helps anyone write, so
the check most likely to go dark is the one whose input has no author.
After: run `/phil:board-setup` → is asked which label families are single-valued, with the labels
actually in use displayed as evidence beneath the question, and sees the answer written **outside** the
markers as a declaration attributed to me.
Decision enabled: whether `bug` + `documentation` + `enhancement` co-occurring is a decision or a
defect — the judgement no forge records and no inference may make.

AC1 — The labels in use are shown as evidence and never pre-selected as an answer ([D6]).
AC2 — A declaration that contradicts what the labels suggest is written as given, and the disagreement
is recorded rather than resolved.
AC3 — A declined question writes nothing, and the report states that rule 4 will keep reporting
`unevaluated` for that family.
AC4 — A reply that is neither an answer nor a decline — "ok", "sure" — is treated as unanswered and
asked once more, naming what is still needed.

### S4 — Tell an assumption from a fact in the written block

As Robin, I can see at a glance which lines the forge told us and which lines we guessed.

**Elevator Pitch**
Before: a block states "Auto-close on Done is ENABLED" with no way to know that *enabled* was read from
the API and *on Done* was assumed — one confident sentence spanning a fact and a guess.
After: run `/phil:board-setup` → sees `Auto-close issue: enabled (probed)` and
`trigger status: Done (ASSUMED — the API exposes name and enabled, not the configured statuses)`, with
an offer to confirm.
Decision enabled: whether to spend thirty seconds in the project settings UI confirming the trigger, or
accept the assumption knowingly.

AC1 — Every line inside the markers carries exactly one of `probed` or `assumed`; a line carrying
neither is the defect.
AC2 — An assumption states what is *not* knowable and why, not merely that it is an assumption.
AC3 — A confirmed assumption becomes a declaration outside the markers attributed to Robin — it does
not become a probed fact, because nothing probed it.
AC4 — The closing report totals the three categories separately (KPI-2).

### S5 — Re-run it and trust the result

As Robin, I run it again months later and find out what moved, without the file churning.

**Elevator Pitch**
Before: a block written once decays silently — an option id that no longer exists reads exactly like one
that does, which is the same defect as a stale generated block nobody notices (issue #31).
After: run `/phil:board-setup` on a configured repo → sees either `unchanged` and a zero-byte diff, or a
line-by-line account of what the forge now says that the file did not.
Decision enabled: whether anything about the board moved under the repo since the last run.

AC1 — A re-run against an unchanged board writes zero bytes and says `unchanged` (KPI-3).
AC2 — A timestamp refresh alone is not a change; the markers carry the probe time and re-stamping does
not count as churn.
AC3 — An option id present in the file and absent from the forge is reported as vanished, inside the
markers refreshed and outside the markers reported only.
AC4 — A `CLAUDE.md` modified between the read and the write is re-read and the write refused.

### S6 — Do all of it on GitLab

As Robin, I get the same block on a GitLab repo, whose board is labels rather than a Status field.

**Elevator Pitch**
Before: `phil:issue-board` covers both forges and a GitHub-only setup command leaves every GitLab repo
learning its constants by contact — the defect closed on one forge and left open on the other.
After: run `/phil:board-setup` in a GitLab repo → sees the same marked region carrying the tier, the
board id, the `status::` label set and the docs root, probed with `glab`.
Decision enabled: the same one, on the other forge.

AC1 — The region's *shape* is identical across forges; only the values and the calls differ.
AC2 — Tier is probed, and a Free-tier instance produces a Free-shaped block — no scoped-label
convention is written where scoped labels do not exist.
AC3 — `glab`'s `-O` JSON flag is used, never `-F`, which fails silently (`phil:issue-board`).
AC4 — Absence of Projects v2 workflows is recorded as *not applicable on this forge*, never as *none
enabled* — the `unknown`-is-not-`not-started` discipline, one domain over.

## Wave: DISCUSS / [REF] Outcome KPIs

| # | KPI | Target | Method |
|---|---|---|---|
| KPI-1 | Fraction of `Per-project setup` template fields populated with no human input | ≥ 0.5 | Count on slice 01's real run; recorded in the brief, pass or fail |
| KPI-2 | A reader can say, for every line of a generated block, whether it was probed, declared or assumed | 100% of lines, under 60s | Timed read by someone who did not run the command |
| KPI-3 | A second run on an unchanged board writes zero bytes | binary | `git diff --stat` after the second run |
| KPI-4 | `/phil:groom-issues` rule 4 reports *evaluated* on a repo this command configured | binary | Run grooming after slice 03 |
| KPI-5 | Hazards present at t=0 rather than added after an incident | ≥ 5 of 7 | **Not measurable until a next repo exists.** Stated rather than fabricated |

KPI-5 is the KPI that matters and the one that cannot be measured yet, because this repo is already
configured and its seven entries are already the record of the failure. Recording it as unmeasurable is
the honest form; `single-issue-per-feature` recorded a *failed* KPI rather than quietly dropping it, and
the same discipline applies to one that cannot yet run.

## Wave: DISCUSS / [REF] Definition of Ready

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Persona identified | ✓ | `robin-backlog-curator`, extended; ninth persona considered and rejected in *Persona ID* |
| 2 | Job traceability | ✓ | New job `know-a-boards-hazards-before-contact` + a facet on `keep-a-backlog-trustworthy`, [D2] |
| 3 | Journey mapped | ✓ | `journeys/board-setup-block.yaml`, arc upward, error paths incl. the declined-declaration cost |
| 4 | Stories with elevator pitches | ✓ | S1–S6, each naming `/phil:board-setup` as a real invocable entry point |
| 5 | ACs testable | ✓ | Each AC names an observable; KPI-1 and KPI-2 supply numbers for the two that were vibes |
| 6 | Scope assessed | ✓ | PASS, one signal of five, answered by [D10] rather than by a split |
| 7 | Slice briefs exist | ✓ | Six briefs under `slices/`, each with a taste-test table |
| 8 | Outcome KPIs numeric | ✓ | KPI-1..5; KPI-5 declared unmeasurable rather than fabricated |
| 9 | Out-of-scope explicit | ✓ | Below |

Requirements completeness: **0.94**. The shortfall is named rather than rounded away — the three items
under *Open (→ authoring)*, of which the command's placement relative to `plugin-dev`'s naming
conventions is the one that could change a story's elevator pitch.

**These nine items were authored for this feature, not taken from a canonical list**, because none is
recorded in this repo — the same self-graded weakness `single-issue-per-feature` recorded. Treat the
ticked table as a structure check, not an external gate.

## Wave: DISCUSS / [REF] Open (→ authoring) — CLOSED 2026-08-17

All three settled at authoring time, after consulting `plugin-dev:command-development` (read directly:
invoking it fails, see *Also found* below) and `plugin-dev:skill-development`.

1. **The command's name — `/phil:board-setup`, confirmed. (User)** No longer provisional; S1–S6 stand
   byte-identical. **An objection was raised and overruled, recorded so this reads as decided rather
   than overlooked:** the name is noun-noun where both `plugin-dev` and this repo's convention
   (`groom-issues`, `rank-issues`, `review-code`) prescribe verb-noun, and *setup* names the one thing
   out-of-scope forbids — the command creates no project, field, option or label. `/phil:record-board`
   was recommended and declined. If the reading ever bites, the rename cost is six story pitches, this
   table and slice 01's brief.
2. **Probe logic lives in `scripts/probe-board.py`. (User)** A script emitting `{field, value, query}`
   JSON; the skill owns interpretation, placement and the write. Chosen because slice 01's AC1 (*no
   value inside the markers was typed by a human*) and KPI-3 (*a second run writes zero bytes*) are
   properties code can **hold** and prose can only **request** — and in the finished file a remembered
   id is indistinguishable from a probed one, which is this feature's own failure mode turned on
   itself. Written in Python, not the bash the option sketched, to match `check-invariants.py` and
   because assembling stable-ordered JSON from repeated `gh` calls is jq-fragile.
   **The honest cost, in the command's prose too:** the script calls `gh`, so the grant constrains the
   command to *the queries that script contains* rather than to any `gh` call. Safety moved from policy
   to code review; adding a mutating call to the script would widen the command's reach without
   changing a line of frontmatter.
3. **The tier probe is reused from `phil:issue-board`, never restated. (Session)** This repo's own rule
   — a second copy is a second authority — answers it. On GitHub the recorded value is *not applicable*
   rather than a plausible default: the bullet exists because GitLab gates scoped labels and real
   `blocks` links behind Premium, and GitHub gates neither. That is C6 applied, and the mirror of S6's
   AC4.

## Wave: DISCUSS / [REF] Pre-requisites

- `gh auth` with the `project` scope (`gh auth refresh -s project`), present in this repo as of
  2026-08-12. The command must detect its absence and name the fix rather than writing a partial block.
- `phil:issue-board`'s *Per-project setup* template is the content contract. This feature does not
  redesign it; #32 puts its content explicitly out of scope.
- No dependency on any prior wave of this feature — DISCOVER and DIVERGE did not run.

## Wave: DISCUSS / [REF] Out-of-scope

- **The template's content.** `phil:issue-board` owns what belongs in the block. This feature is about
  who writes it. (#32, verbatim)
- **`rules/`.** It ships to every consumer; a per-project constant would land in strangers' projects.
  (#32, and `CLAUDE.md`'s *Not `rules/`* rule)
- **Migrating this repo's existing block.** Slice 02 inserts a region *beside* the hand-written bullets
  and offers to retire one only on an explicit answer. Rewriting them is not in the feature.
- **An invariant check or hook** that fails a repo with board work and no declaration. Considered as a
  third driving-port option and **not chosen** ([D3] alternatives). Named here so a later reader can see
  it was decided rather than forgotten.
- **Writing any other repo's `CLAUDE.md`** ([D9]).
- **Writing to the forge.** The command reads the forge and writes one local file. It creates no
  project, no field, no option, and no label — `updateProjectV2Field`'s full-replacement hazard is a
  reason to *record* the field's shape, never to modify it.
- **Configuring a board that does not exist yet.** A repo with no project is reported as having none;
  creating one is a decision with a duplicate-board failure mode `phil:issue-board` documents.

## Wave: DISCUSS / [REF] Wave decisions summary

### Requirements summary

Primary need: a repo's board constants should be discovered and written down before they are learned by
contact, with each line labelled by where it came from — probed, declared, or assumed. One new
user-facing command, six slices, both forges, walking skeleton first.

### Constraints established

- **C1 PROBE-DON'T-ASK.** Anything the forge can answer is never a question. Asking a human to paste an
  id they must look up is the current failure, not a mitigation of it.
- **C2 DELIMITED, GENERATED, TIMESTAMPED, PLACED AMONG PROSE.** [D4]. The region is the only thing the
  command owns; everything outside it belongs to a human, permanently.
- **C3 THREE CATEGORIES, EACH LABELLED.** [D5]. A line carrying no provenance label is the defect —
  the shape `groom-ask` arrived at on 2026-08-14 when an unlabelled field, not a drafted one, became
  the thing to forbid.
- **C4 NEVER INFER A DECLARATION.** [D6]. Evidence beside the question; never in the answer.
- **C5 REPORT DRIFT, DO NOT FIX IT.** Outside the markers, the command's only power is to say what it
  found and to ask.
- **C6 ABSENT IS NOT BENIGN.** A forge that cannot answer produces *unknown* or *not applicable*, never
  a plausible default — inherited from `nwave-issue-board` C6.
- **C7 SILENCE IS NOT CONSENT.** No offer is adopted without an explicit answer — inherited from
  `groom-ask`, where it is the one path by which the tool's own words could reach the artifact
  unnoticed.

### Upstream changes

None. No DISCOVER or DIVERGE artifacts exist for this feature; nothing prior is contradicted.

### Also found, out of scope

- **`docs/product/architecture/brief.md` stops at `session-handoff` and ADR-014.** It has no
  `single-issue-per-feature` entry and no ADR-015+, so the architecture SSOT lags the last two features.
  Noticed, not carded — raised to the user 2026-08-14.
- **Issue #31 is open and has no card on the project board.** It appears in `gh issue list` and not in
  the project's items, so it can carry no Status and is invisible on the kanban. Raised to the user
  2026-08-14; fixed by one `gh project item-add`.
- **`skills/issue-board/SKILL.md` needs a route-1 fold-back** recording that
  `projectV2 { workflows { name enabled } }` is readable, with the fixture that would have caught it.
  This is a fold-back rather than part of this feature, and it is small enough to take that route.
  **The 2026-08-17 run adds two more to the same fold-back:** that `repository.projectsV2` can be empty
  while a board exists (so the owner-level route is required, not optional), and that `views.layout`
  makes the kanban view probeable.
- **`plugin-dev:command-development` cannot be invoked as a skill.** Its `SKILL.md` embeds
  `` !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/script.sh` `` — a placeholder copied from its own documented
  example — and the installed copy has no `scripts/` directory, so the Skill tool fails on the shell
  pattern before the body loads. Read the file directly instead; the consult is unaffected. Worth a card
  against the upstream plugin, not against this feature. Found 2026-08-17.
