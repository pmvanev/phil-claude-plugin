<!-- markdownlint-disable MD024 -->
# Feature Delta — lambda-web-app-speed

Wave: DISCUSS ✓ (2026-10-26) · Density: lean
Build path: DISCUSS here, then the rule and skill are written directly. The deliverable is prose, so
DESIGN, DISTILL and DELIVER stay out (edd-loop DDD8). Rules are not a plugin component; `plugin-dev`'s
skill, command and validator guidance governs the new command and its skill.

This feature adds one standard, `rules/lambda-web-app-speed.md`, and one command that applies it,
`/phil:lambda-web-app-speed`, which measures a web app served from AWS Lambda, finds where its load time
goes, ranks the fixes and stops where returns fall off. `/phil:review-code` applies the rule's
file-checkable rows. It rests on `docs/research/web-speed/lambda-web-app-speed-canonical-sources.md`
(52 sources) and on mining 208 sessions of two projects that did this work by hand. Tracked on issue 59.

---

## Wave: DISCUSS / [REF] The gap, measured

Measured 2026-10-26 against `main` at `abe481e`:

- **No rule or skill mentions cold starts, Lambda INIT, memory sizing, packaging, cache headers,
  compression, code splitting or keeping a server warm.** A search of `rules/`, `skills/`, `commands/`
  and `agents/` returns nothing on any of them.
- **Half the lessons already have a home.** `coding.md` §8 pools connections and §15 batches every call
  that crosses the network, both added in 1.1.0 from beatrix's connection work. Neither says what is
  Lambda-specific: connections scale with execution environments, so a cap belongs outside the function.
- **Two projects learned the rest by hand, and the second copied without measuring.** beatrix cut a cold
  first load from 13.4 s to 3.4 s over one card, by measuring one level deeper each time. modive adopted
  beatrix's levers three weeks later; on 2026-10-26 its simulation API took 7–9.5 s to start, about
  6.5 s of it waiting on the first Postgres connection, and hit Lambda's 10 s INIT ceiling in front of a
  user. None of the copied levers touched that cost; only the cold-start timing line it also copied
  revealed it.
- **A canonical claim the projects relied on is stale.** "INIT is free up to 10 s" has been false since
  2025-08-01, when AWS began billing INIT for every configuration (research 1.2).

### Mined from 208 sessions (130 beatrix, 78 modive), 2026-10-01 to 10-26

The measured gains, in the order they paid on beatrix's dev stack (cold `GET /`):

| Change | INIT | First request | First byte |
|---|---|---|---|
| Start, 512 MB | 2.3–3.1 s | 8.5–9.5 s | 13.4 s |
| Build the app during INIT, plus cache headers, gzip and lazy panes | 7.1 s | 0.15 s | 8.1 s |
| 1769 MB | 5.8–6.1 s | 0.05 s | 6.6–6.9 s |
| Compiled bytecode | 5.1–5.4 s | 0.01 s | 5.9–6.2 s |
| Startup checks batched and run concurrently; one deferred to first use, one to deploy | 2.8–3.0 s | 0.013 s | 3.4 s (browser) |

Separately: one shared pool and plural boundary calls cut connections per acceptance run from 20,789 to
1,589; route-level splitting cut the entry chunk 27% gzipped; a heartbeat from open, signed-in pages kept
every post-break action warm for about $0.30 a month per open page.

**Corrections the user made**, each now a decision below:
- *"really the problem I care about is B, not A"*: the cold start that matters is a second one while a
  person is using the app; paying to stay warm for nobody was ruled out (D9).
- *"not quite. If my tab is open… some sort of heartbeat"*: a client cache does not keep the server warm
  (D9).
- *"we aren't batching database lookups. is that right?!"* and *"are we also batching/optimizing
  Cedar/AVP…?"*: an authorization call is a network call too (D6).
- *"an important factor to me… is to follow standard, canonical, intuitive patterns"*: the bundle split
  had been judged on milliseconds alone (D13).
- *"we don't necessarily need a strict before and after measurement"*: fix what the code plainly shows
  without waiting on a baseline (D8).

Claude corrected itself twice in ways the rule must carry: bytecode pushed beatrix's zip past Lambda's
50 MB direct-upload limit and broke a prod apply (D11); and a first guess at a 4–5 minute ping interval
was measured at 2–8 minute recycles, so 60 s (D9).

## Wave: DISCUSS / [REF] Pre-requisites

- **Research precursors (D1), done, not yet committed:** the research document, and the mining notes,
  which stay outside this public repo; this delta carries their distilled findings.
- **Verification precursors, not done** — each closes before the slice that cites it ships:
  - **V1 (slice 01):** every GovCloud availability fact a row cites (SnapStart for Python, Function URLs,
    CloudFront) is re-read on its AWS page on the day the row is written (research Gap 5).
  - **V2 (slice 02):** the composed Logs Insights cold-start query (research 9.1) runs against real logs
    and its `pct()` and `count(@initDuration)` results are checked by hand against the raw `REPORT`
    lines (research Gap 7).
  - **V3 (slice 04):** NIST SP 800-63B-4's session and reauthentication sections are read before
    "a background request is not use" becomes more than Advisory (research Gap 4).
- **Production data:** beatrix and modive, both on this machine, with their history before and after
  the work: beatrix before issue 254 and modive at `43e6b85`, the commit modive's audit read. Read-only
  CloudWatch access to modive's dev stack for slices 02 and 03.
- **Existing artifacts touched:** `rules/lambda-web-app-speed.md` (new); `skills/lambda-web-app-speed/`
  and `commands/lambda-web-app-speed.md` (new); `skills/review-code/SKILL.md` (reads the new rule when
  it meets the files D4 names); one cross-reference line each in `coding.md` §8 and `react.md`;
  `README.md`; `.claude-plugin/plugin.json`; `docs/product/jobs.yaml`;
  `docs/product/personas/quinn-codebase-steward.yaml`.

## Wave: DISCUSS / [REF] Persona ID

**`quinn-codebase-steward`, extended with a speed facet — no new persona.** Quinn already owns
"perf/dependency work" among the codebase's invisible initiatives. In every mined session the person who
measured the cold start also owned the infrastructure and the front end; the operator who felt the slow
load is a stakeholder, not the user of this command.

## Wave: DISCUSS / [REF] JTBD one-liner

**New job: `make-a-lambda-web-app-load-fast`.**

> When people wait on a web app I serve from AWS Lambda, I want to find where the load time actually
> goes and fix the largest share with the standard pattern — without paying to keep servers warm for
> nobody — so I can stop rediscovering the same levers in each project and stop copying levers that
> miss the cost a project actually has.

Recorded in `docs/product/jobs.yaml`. Not a facet of `shape-a-pipeline-to-the-change`: that job's
speed is the pipeline's, measured from forge job records; this one's is a person's page load, measured
from Lambda's logs and a browser.

## Wave: DISCUSS / [REF] Locked decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | **Research and session mining are precursors**, done before this delta. | The user's choice, 2026-10-26, following the CI standard's path. |
| D2 | **One rule, `rules/lambda-web-app-speed.md`, covering the whole path from INIT to the browser.** | User decision, 2026-10-26. The work ran that way in both projects, and a person's load time crosses every layer. |
| D3 | **The rule splits on checkability**: Principles, then **Always-flag**, **Advisory** and **Do not flag**. Rows carry stable ids `LWS-n`, cite a source beside them, and a retired id is never reused. | The `security.md` and `ci-pipelines.md` shape. A principle filed as a defect borrows authority it has not earned. |
| D4 | **`/phil:review-code` applies the Always-flag and Do-not-flag lists** whenever it reads a Lambda handler, IaC that defines a Lambda function or its HTTP front door, a web bundler config, or code that sets response headers. | User decision, 2026-10-26. The `security.md` precedent: defects surface in ordinary review, not only when someone measures. |
| D5 | **`/phil:lambda-web-app-speed` measures, then ranks.** It has no file-review mode; D4 covers that. | User decision, 2026-10-26. A file cannot tell a fix that saves a second from one that saves a millisecond. |
| D6 | **Cite `coding.md` §8 and §15; add only the Lambda-specific half.** Connections scale with execution environments, so a cap lives outside the function (RDS Proxy or reserved concurrency), and a pool is sized to the concurrency one request uses. Authorization, identity and secrets calls are network calls under §15. | Research 5.2; the mined AVP correction. Restating §8 and §15 would make two owners of one rule. |
| D7 | **Build what every request uses during INIT, and hold INIT to a stated budget under its 10 s ceiling.** INIT is billed, so this is a latency rule, not free compute. A check that proves the deployment rather than the instance moves to the deploy when INIT nears the budget. | Research 1.1, 1.2. modive dropped "checks once per deploy" because INIT had taken them off the request path; its 10 s timeout on 2026-10-26 put them back on it. |
| D8 | **An Always-flag row needs no measurement; a ranking always does.** A defect the code plainly shows is fixed on sight; choosing among fixes needs numbers. | The user's waiver on beatrix 254, and Gregg's drill-down (research 10.1). The two halves of the feature divide on this line. |
| D9 | **Keeping warm is a priced choice, and no row flags its absence.** The rule names provisioned concurrency as AWS's documented answer, SnapStart where the runtime and partition allow, and a heartbeat from open, signed-in pages where use is sparse and idle billing is unwanted. The cold start that matters is the one a present person pays. Scheduled pings are never called a guarantee. | Research 4.1–4.3; the user's two corrections on beatrix 174; the measured 2–8 minute recycle. |
| D10 | **Static assets go to S3 behind CloudFront where CloudFront exists.** Where it does not, as in GovCloud, the function serves them with build-time ETags, precompressed files and `immutable` lifetimes. The routing row fires only where CloudFront is available. | Research 6.3, 6.4; beatrix ADR-22. A row that flags the only available design teaches readers to skip it. |
| D11 | **Bytecode is Advisory either way.** Compile with the runtime's own Python, in `unchecked-hash` mode; check the zip against the 50 MB direct-upload and 250 MB unzipped limits. Shipping `.pyc` built by another Python minor version is Always-flag. | Research Conflict 1 against beatrix's measured halving of import time and its broken prod apply. |
| D12 | **The skill reads; it never deploys, applies, changes a function's configuration or forces a cold start without a yes for that action.** It may ask the person to deploy or to force one. | beatrix ADR-118 gives deploys to CI; CLAUDE.md's rule for outward actions. |
| D13 | **Among fixes of similar payoff, rank the standard, documented pattern first.** | Mined 33 times in 24 sessions; codified in beatrix's *Solution Selection*. |
| D14 | **Rows give Python forms first, Node.js where a source gives one; Principles stay runtime-neutral.** Lambda Web Functions get one Advisory line. | Both projects are Python; Web Functions are two weeks old, Node.js 24 only, and in five commercial Regions (research 6.5). |
| D15 | **The front end is held to what the evidence covers**: route-level lazy loading, a bundle budget that fails the build, a stale-while-revalidate cache per open view, and cache headers. | Research Gap 8 left fonts, LCP images, preload hints and streaming unresearched. Rows without sources are speculation. |
| D16 | **Targets: LCP ≤ 2.5 s and TTFB ≤ 0.8 s at p75, plus a cold-path budget the project declares. Stop at the target, or where the next fix costs more than the delay it saves.** | web.dev Core Web Vitals (research 9.3); Reinertsen's U-curve, inherited from the CI research. |

## Wave: DISCUSS / [REF] Driving ports

- **`/phil:lambda-web-app-speed [<function> | <url>]`** — measures the cold and warm paths from Lambda's
  `REPORT` and `INIT_REPORT` lines and a browser trace, divides the time, drills one level into the
  largest slice, ranks candidate fixes by saving per unit of effort with the standard pattern first
  among equals, prices the warmth options, and draws the stopping line.
- **`/phil:review-code`** — applies the rule's Always-flag and Do-not-flag lists to the files D4 names.
- **The rule file** — read by any skill that names it, and by a consumer who copies it into
  `.claude/rules/`, where its `paths:` frontmatter loads it for Lambda IaC, handlers and bundler config.

## Wave: DISCUSS / [REF] WS strategy

**A — none.** Additive and brownfield: one new rule, one new command, and a read added to
`review-code`. Slice 01 is the thinnest end-to-end value: a review that names a real project's load-time
defects by row id.

## Wave: DISCUSS / [REF] Scope Assessment: PASS

Four slices, one done precursor, three verification precursors. One context: the rules and review
system. No oversized signal fires: four user stories, one new command, each slice against a real project
or its real logs. The user asked for one card.

## Wave: DISCUSS / [REF] User stories

Every story traces to `job_id: make-a-lambda-web-app-load-fast`.

### US-01 — `review-code` flags load-time defects by row id *(walking-skeleton slice)*

**Problem.** Quinn's handler builds its app and clients inside the first request, its hashed assets go
out with no cache lifetime, and the function gzips its entry chunk on every response. A review reads all
three files and says nothing, so Quinn learns about each from a slow page.

**Solution.** `rules/lambda-web-app-speed.md` with its Always-flag rows (research LWS-1 to LWS-20,
revised by D6, D10 and D11) and Do-not-flag list; `/phil:review-code` applies them (D4).

#### Elevator Pitch
Before: a load-time defect visible in a file surfaces only when someone feels the page is slow.
After: run `/phil:review-code` on a Lambda web app → sees items such as `LWS-1: boto3 client built
inside the handler on every request — build it at module scope`, and no item for a client built lazily
on one rare route.
Decision enabled: which load-time defects to fix before the next deploy.

#### Acceptance Criteria
- [ ] `rules/lambda-web-app-speed.md` exists with an Always-flag table. Each row names the defect, its
      `LWS-n` id, its source and a preferred form; V1 closed for every GovCloud row.
- [ ] A Do-not-flag list covers at least: a client built lazily on a rare path; no provisioned
      concurrency, SnapStart or pings; a zip without `.pyc`; a static asset served by the function where
      CloudFront is unavailable; VPC attachment on a function that reaches RDS.
- [ ] `review-code` reads the rule only when it meets the files D4 names, and names each finding by row
      id with the row's fix.
- [ ] A self-test fixture seeds at least eight Always-flag defects beside five look-alikes; a test pins
      every `LWS-n` id to its row and each expected item's id and fix.
- [ ] Backtest: one review of beatrix before issue 254 and one of modive at `43e6b85` are recorded here,
      each listing which of that project's hand-found, file-visible fixes the rows caught and missed.

### US-02 — Measure the cold path and divide its time

**Problem.** Quinn hears that the first load "takes a while". Nothing says whether the time is INIT, the
first request, the network or the browser, so the first fix goes to whatever looks slow.

**Solution.** `/phil:lambda-web-app-speed` v1: reads `REPORT` and `INIT_REPORT` lines through Logs
Insights (filtered on `@type` first, so no application line is read), counts cold starts, INIT timeouts
and suppressed inits, and divides one cold path into INIT, first invoke and first byte. The rule's
Principles on measuring land with it.

#### Elevator Pitch
Before: "it's slow" with no number and no owner.
After: run `/phil:lambda-web-app-speed simulation-api` → sees `7 days: 41 cold starts (18%); INIT p50
7.8 s, 2 INIT timeouts; first invoke p50 0.12 s — INIT owns the cold path`, with the query that produced
each number.
Decision enabled: which layer to look inside first.

#### Acceptance Criteria
- [ ] V2 closed: the query's percentiles match a hand count of the raw lines.
- [ ] The report names INIT timeouts and suppressed inits separately, since each hides inside another
      number.
- [ ] No command writes to AWS; every number cites its query (D12).
- [ ] A fixture of recorded `REPORT` and `INIT_REPORT` lines yields the expected split.
- [ ] Dogfood: one read-only run against modive's simulation API is recorded here.

### US-03 — Drill one level into the largest slice

**Problem.** INIT owns 7 s and nothing says which part of it. beatrix found its answer only after adding
a timing line per phase, then per AWS call; modive's 6.5 s first connection is still unexplained.

**Solution.** When the top-level split does not explain the largest slice, the skill proposes the next
instrument — a cold-start line timing each phase and check, then each network call or connection leg
— with a reference example for Python, and reads its output once the person deploys it.

#### Elevator Pitch
Before: the largest slice has a size but no cause.
After: run `/phil:lambda-web-app-speed simulation-api` with the timing line deployed → sees `INIT 7.8 s:
first DB connection 6.4 s (token signing 0.1 s, DNS 0.0 s, TLS + auth 6.3 s) · imports 0.9 s · checks
0.3 s`.
Decision enabled: which cause to fix, or which instrument to add next.

#### Acceptance Criteria
- [ ] The skill proposes an instrument only for a slice the measurement left unexplained, and says what
      the instrument costs at INIT.
- [ ] The reference timing line reports elapsed time by the clock, not a sum of concurrent durations.
- [ ] Dogfood: with the user, on modive's simulation API, the first Postgres connection's legs are
      timed and the cause named or narrowed.

### US-04 — Rank the fixes, price the warmth, draw the line

**Problem.** Ten candidate fixes exist and the order they go in decides whether the project stops at
3.4 s or at 8 s. Keeping warm is either rejected outright or bought without a price.

**Solution.** The skill ranks candidates on the measured path by saving per unit of effort, puts the
standard pattern first among equals (D13), prices provisioned concurrency, SnapStart and a heartbeat for
the app's measured traffic (D9), measures a browser load's TTFB and LCP, and draws the stopping line
(D16). The rule's remaining Principles and its Advisory list land with it; V3 closes first.

#### Elevator Pitch
Before: fixes go in the order someone thought of them, and warmth is argued, not priced.
After: run `/phil:lambda-web-app-speed https://app.example` → sees `LCP p75 4.0 s against 2.5 s; ranked:
1 batch the startup checks (−2.3 s, S) 2 bytecode (−0.7 s, S) … stop after 3`, and a line pricing each
warmth option per month at this traffic.
Decision enabled: which fixes to make, which warmth to buy, and when to stop.

#### Acceptance Criteria
- [ ] Each candidate carries an estimated saving, an effort class and the measurement behind both.
- [ ] Warmth options are priced from the app's own invocation counts, with partition availability
      checked.
- [ ] Replay: given beatrix 254's measurements in order, the ranking puts its three largest measured
      gains in its top three.
- [ ] The report names the stopping point and the target it stopped at.

## Wave: DISCUSS / [REF] Definition of Done

1. The rule shipped, with each source cited by title and a section on what is the rule's own.
2. The command shipped, with `mutates:` declared and `scripts/check-readonly-commands.py` green.
3. `review-code` reads the rule only for the files D4 names, with a fixture that fails without it.
4. Every rule row pinned by a test; every fixture fails without the row it guards, watched once.
5. `python3 -m pytest -q` and `scripts/check-invariants.py` green.
6. `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` run, and their findings fixed.
7. Prose edited to `rules/writing.md` with `phil:eos`; the skill and command hardened with
   `/phil:harden-instructions`.
8. README and plugin version updated.
9. Each slice's dogfood recorded here, naming whether it drove the working tree's prose or a released
   version; issue 59's candidate targets each encoded with a fixture or struck through with the reason.

## Wave: DISCUSS / [REF] Out of scope

- Pooling and batching in general — `coding.md` §8 and §15.
- Pipeline and deploy speed — `ci-pipelines.md`.
- Fonts, LCP images, preload hints, response streaming and the sign-in chain before first render (D15).
- Platforms other than Lambda, and Lambda form factors beyond one Advisory line (D14).
- Changing beatrix or modive. They are sources and dogfood targets; a fix found while dogfooding goes to
  that project's own card.
- Deciding to adopt RDS Proxy; the rule names it as the cap, and the choice stays the project's.

## Wave: DISCUSS / [REF] Outcome KPIs

| KPI | Target | Measured by |
|-----|--------|-------------|
| Seeded defects found, look-alikes left alone | 100% of defects, 0 look-alikes, in the slice 01 fixture | Fixture grading |
| Hand-found, file-visible fixes the review catches on the backtest | ≥ 80% across beatrix before 254 and modive at `43e6b85` | Slice 01 backtest, recorded here |
| The skill names modive's dominant cold-start slice, then its cause | Slice from logs alone; cause one level down | Slices 02 and 03 dogfood |
| The ranking reproduces beatrix 254's measured order | Its three largest gains in the top three | Slice 04 replay |
| Levers copied without measuring | No lever adopted in a dogfood without a number behind it | Slice dogfood records |

## Wave: DISCUSS / [REF] Slice 01 delivered and backtested (2026-10-26)

**What landed.** `rules/lambda-web-app-speed.md`, its reviewer half: nineteen Always-flag rows (LWS-1 to
LWS-19) in five tables — INIT and the handler, the deployment package, keeping warm, the front door and
static assets, the bundle — and a Do-not-flag list. `review-code` reads the rule in a repository that
deploys to Lambda, applies it to every file it gathers (build, dependency and CI files included), files
each finding by its `LWS-n` id with the row's Preferred form, and counts load-time items on their own
Summary line. `coding.md` §8 points at LWS-1. Fixture 07 seeds fourteen items beside six look-alikes;
`tests/test_lambda_web_app_speed_rule.py` pins the ids, the dated GovCloud rows, D9, D10 and D11, the
review's trigger and gather, and every expected item to its row. Each new test was watched failing on
the input it guards before it passed.

**V1 closed.** AWS's GovCloud (US) Lambda page, read 2026-10-26: "AWS Lambda Function URLs is not
available" and "Lambda SnapStart for Python and .NET is not available". CloudFront has no page among the
guide's 179 service pages, and its URL redirects to the guide's index; the rule cites that absence, not a
quoted sentence. boto3's "Clients" guide, read the same day, backs LWS-3's build-clients-first clause.

**Backtests, read-only, in scratch clones.** A fresh agent applied the rule alone to each project as it
stood before its speed work, then I compared its items with the fixes each project made by hand. Fixes
that a measurement chose — memory raised from 512 MB, bytecode, the cold-start timing line — are left
out, since D8 and D11 keep them out of the file rows.

| | beatrix before issue 254 | modive at `43e6b85` |
|---|---|---|
| First pass | 4 of 8 | 6 of 11 |
| After the revisions below | 5 of 8 | 9 of 11 |

- *What the first pass missed, and what changed:* both projects built their app on the first invoke and
  cached it, which a row about "each invoke" missed, so LWS-1 now names the cached build. modive's
  existence probes tested `bool(count)`, not `== 0`, so LWS-4 now covers any count run only to learn
  whether a row exists. Neither project compressed its static files and no row said so, so LWS-13, from
  Lighthouse's "Enable text compression", is new.
- *Still missed, by design:* beatrix's Bedrock check moved to the first chat turn, its bucket check moved
  to the deploy, and its alembic import replaced by a baked head. Each is a judgement about what a cold
  start must prove, which slice 04's Principles own (D7); none is a file-visible defect. modive's S3
  client, which the review read as a rare path the Do-not-flag list clears.
- *One regression, fixed and not re-driven:* the second modive pass skipped the web UI object a route
  built on every request, reading "every request uses" as the whole function's requests. LWS-1 now says
  "every run of that path uses it", which should make modive 10 of 11.
- *KPI:* 14 of 19 hand-found fixes caught across both projects (74%), against a target of 80%. Over the
  sixteen that a file can show, 14 (88%). The three check-placement fixes are the gap, and slice 04 is
  where they belong.

**What the reviews and drives caught, each fixed:** `plugin-dev:plugin-validator` passed with warnings and
`plugin-dev:skill-reviewer` rated the change "needs improvement".
- The gather step checked build, dependency and CI files "against `security.md` alone", so LWS-5, LWS-6
  and LWS-17 could never fire. Those files now meet the rule too.
- The trigger read as "any web app"; it is now a repository that deploys to Lambda.
- LWS-5 (VPC) had no cold-start cost to name once the Do-not-flag list said so; it became a Do-not-flag
  entry. Rows now apply to functions a person waits on.
- LWS-17 turned on intent; it now turns on a CI step the review read. LWS-19 covers navigation tables,
  files one item per router, and its fix names `<Suspense>`.
- An unsettled fact files an Advisory item naming the row and the unread source.
- The fixture's path join, an expected fix naming the wrong function, a build script that shipped a test
  file and no `dist/`, and an API with no route were fixed.

**Fixture 07, two blind drives.** *Drive 1*, before the revisions, filed all fourteen then expected, no
look-alike, and LWS-15 twice — now expected. *Drive 2*, after them, filed every expected item and no
look-alike; it split LWS-19 into three and found the missing `<Suspense>`, both since fixed and not
re-driven.

**`phil:eos`** rewrote four sentences of the rule and changed no Preferred form.
**`/phil:harden-instructions`** over the skill's new text made no edit; its checks are authoring-time
tests only.

**Seen, no row covers:** a provider at the app's root that statically imports three.js into the entry
chunk (modive); a cold-start probe that opens its own connection outside the pool, and startup checks
that write and roll back (beatrix); a render-blocking font stylesheet, which D15 leaves out.

**Not verified:** `/phil:review-code` itself, which runs the installed copy (1.9.0) until this releases.

## Wave: DISCUSS / [REF] Slice 02 delivered and dogfooded (2026-10-26)

**What landed.** `/phil:lambda-web-app-speed` v1 (`commands/lambda-web-app-speed.md`,
`skills/lambda-web-app-speed/`): it resolves a function, starts the window at the function's last change,
fetches the `REPORT` and `INIT_REPORT` lines with `aws logs filter-log-events`, divides them with
`scripts/cold-path.py`, names the layer to look inside, and cites both commands. The rule gained its
first three Principles: measure, then divide the time; count every cold start, including the two that
hide; measure the code that is running. `tests/test_lambda_cold_path.py` pins the script to fixture 01,
31 recorded lines; `tests/test_lambda_web_app_speed_command.py` pins the grant to AWS read verbs and the
prose to D12. Each test was watched failing first, and each detection branch was removed once to watch a
test catch it.

**V2 closed, and it changed the design.** The composed Logs Insights query ran over fourteen days of
modive's simulation API (7,876 invokes) and was checked by hand against the raw lines the same day:

| | Logs Insights | Hand count |
|---|---|---|
| `count(*)` | 7,876 | 7,876 |
| `count(@initDuration)` | 96 | 96 |
| `pct(@initDuration, 50 / 95)` | 1,691.19 / 8,906.14 ms | 1,691.19 / 8,906.14 ms, nearest rank |
| `pct(@duration, 50 / 95)` | 18.04 / 297.13 ms | 18.05 / 297.19 ms, nearest rank |

The functions agree: `pct()` returns the nearest-rank value over 96 values and approximates it, within
0.1%, over 7,876. **The query is still wrong for this job**: reading each log stream in order found 105
cold starts, not 96. After an INIT timeout, the first `REPORT` carries no `Init Duration` and its
`Duration` holds the retried INIT (2,004 ms against a 112 ms START-to-END span); after an invoke timeout,
the next `REPORT` folds a fresh INIT the same way (5,238 ms against 4,117 ms, memory back to a fresh
environment's). Five and four such cold starts hid among the warm invokes. Logs Insights cannot order
lines within a stream, so v1 reads the raw lines through the script instead of the brief's Insights
queries. The CLI's filter pattern does the brief's `@type` filtering, and the script drops any other
line unread.

**Dogfood, read-only, against modive's simulation API in AWS GovCloud (US)**, driving the commands the
skill names by hand. Since its last change (2026-10-26 14:37 UTC): 749 invokes, 9 cold starts (8
recorded, 1 after an INIT timeout); INIT p50 2.40 s and p95 9.97 s; first invoke p50 0.14 s. **INIT owns
the cold path, 97% of the split time**, and reached its 10 s ceiling once. Over fourteen days, which
mixes 1,024 MB and 1,769 MB: 105 cold starts, five INIT timeouts, INIT 58% of the split time — the first
invoke owned more of it before modive moved its checks into INIT. The learning hypothesis holds: the
function's existing logs named the layer without new instrumentation.

**Moved:** US-02 named a first-byte slice. A function's logs hold no first byte, so it moves to slice 04
with the browser, where its brief already puts the browser.

**What the reviews caught, each fixed.** `plugin-dev:plugin-validator` passed the change with two major
gaps, and `plugin-dev:skill-reviewer` rated it "needs improvement".
- The skill asked for epoch milliseconds with no tool to compute them, so a run would do the arithmetic
  by hand and cite a silently wrong window. The script now computes the window (`--window`, `--days`).
- No granted command returned the Region. The configuration read now takes `FunctionArn`, which holds
  the partition, Region and account; `aws sts` left the grant.
- The truncation warning could never fire, because the CLI drops `NextToken` once it fetches every page.
  The fetch now carries `--max-items`, and the warning names where it stopped (checked against the real
  log group with a cap of 50).
- An INIT that errored was counted as a timeout; INIT failures are now counted by status, and the kind
  renamed "after a failed INIT". A SnapStart restore, which carries `Restore Duration`, would have
  counted as warm; the script now refuses it.
- The rules for choosing a layer had a dead branch and no wording for "none". The choice moved into the
  script as `Look inside:`, pinned by four tests.
- A `REPORT` line with no `Duration` crashed the script, and its annotations failed on Python 3.9; both
  fixed. The script is executable.

**`phil:eos`** rewrote four sentences of the rule's new prose; one widened "an INIT timeout" to an INIT
that times out or fails, to match the script. **`/phil:harden-instructions`** made two edits to the
skill — a bare prohibition given its alternative, a vague timeout made exact — and none to the command.
Every rule a test enforces is authoring-time only, so its prose stays.

**Blind drive, read-only, of this working tree's `SKILL.md`** by a fresh agent against the same function:
it ran the configuration read, the window and the fetch — read verbs only — and reached the hand run's
numbers exactly: 9 cold starts, INIT 97%, `Look inside: INIT, because INIT reached its 10 s ceiling 1
time`. It found four gaps, each fixed and not re-driven: the citation block left out the configuration
read and shortened the script's path; the p75 line had no place in the report; the owner line did not
say INIT's share includes failed INITs; and "move the start later by half" did not say half of what.
It also noted, unfixed, that a window three hours long rests its verdict on nine cold starts, and that
the window ends when `--window` runs, a moment before the fetch.

**Not verified:** `/phil:lambda-web-app-speed` itself, which runs the installed copy until this releases.

## Wave: DISCUSS / [REF] Slice 03 delivered and dogfooded (2026-10-26)

**What landed.** The command's Step 4 drills one level into the layer `Look inside:` names. It looks
for a timing line the function already writes in CloudWatch's Embedded Metric Format, fetches its
records over the same window, and divides them with `scripts/phases.py`: phases add up, concurrent
members sit beside their phase unsummed, the largest phase is the one with the most time across the
window, and members that wait alike are marked. Only where the slice stays unexplained does it propose
an instrument, from `references/cold-start-line.md` or `references/connection-legs.md`, with its cost
at INIT, for the person to deploy. The rule gained Principles 4 and 5: drill one level into the largest
slice, timed by the clock; fix the largest slice first, then measure again. Fixture 02 holds twelve
recorded lines; `tests/test_lambda_init_phases.py` pins the script, both references' Python and metric
names, and the skill's drill. Each script guard was removed once to watch a test catch it.

**The dogfood was already done by hand, and the skill reproduces its first level.** modive's
`fix-listing-cold-start` RCA (its issue 21, 2026-10-26) drilled the simulation API's INIT the way this
slice prescribes. Run read-only over the window since the function's last change — the commands driven by hand from
this working tree, not the released command — the new step found the same thing from the logs alone: checks 66% of the time the code timed, ten checks whose medians sum to
6.11 s inside a 0.99 s phase, and six — every check that opens a Postgres connection — waiting alike
near 8 s at p95 while the rest finished in 0.21 s. The skill would then propose the connection-legs
probe; modive's own probe, run in the API's subnets that day, timed DNS at 31–65 ms, TCP 1–5 ms, TLS
42–69 ms and a password sign-in 45–109 ms, against 2,295–4,604 ms for the first IAM sign-in after 5 to
40 minutes idle.

**The learning hypothesis holds in part.** Two levels of timing named the cause's place — the first IAM
sign-in to Aurora after idle — and not its reason: modive's memory explanation failed its own test when
a 1-ACU floor left the sign-in at 4–5 s. "Named or narrowed" was the criterion, and this is narrowed.
The fix modive chose, password sign-in for its app roles, acts on the place without the reason.

**Moved, and why.** The brief's level 2 read the probe's output; modive's probe prints a Python dict,
not EMF, so the reference probe writes EMF and the comparison above is against modive's recorded
readings, not a fresh read.

**What the reviews caught, each fixed.** `plugin-dev:plugin-validator` passed the change with three
major findings, and `plugin-dev:skill-reviewer` rated it "needs improvement".
- `phases.py` trusted the phase convention blindly: a line that writes a total beside its parts would be
  summed with them and named the largest phase. It now refuses a phase within 10% of the others' sum in
  every record, lists a member whose prefix starts two phases as unattached, and Step 4 confirms the
  convention from the line's code first.
- "Explained" could not be decided. Step 4 now decides in a fixed order from the report's own lines: no
  timing line, the untimed gap, members that wait alike, otherwise the cause.
- The gap to `Init Duration` was described and never computed; `phases.py --init-p50 --cold-starts`
  reports it, and the lines against the cold starts they describe.
- "Waits with the phase" compared two tails that could come from different cold starts; it now tests
  record by record, in the slow half. The fixture still marks the same six checks.
- A timed-out INIT writes no line, so the drill cannot see the attempts that made INIT the layer; the
  skill and the reference now say so. The layer maps to its group (`INIT` to `init`, `first invoke` to
  `first_request`), and the reference covers the first request.
- `phases.py` missed truncation and crashed on a group with no phase and on a nameless metric; fixed.
- The search found only hand-built EMF; it now looks for `add_metric` and `put_metric` too, and asks,
  through the decision-request standard, when it finds none.
- The probe had no handler, no read-back and an unverified sign-in. It gained a handler, string
  dimensions, its prerequisites, `sslmode="verify-full"`, an SSL-reply check and a read-back block, and
  Hard rule 4 admits a probe's lines.

**`phil:eos`** found a wrong warrant, not a style fault: Principle 5 said a second saved outside the
largest slice saves nothing. That is Goldratt's constraint, true of parallel work on a critical path;
a cold start's phases run in sequence, where every second counts. The Principle now rests on Amdahl's
law — a fix saves at most its slice's share — and its sources changed with it.
**`/phil:harden-instructions`** over Step 4 and the references found nothing further.

**Blind drive, read-only, of this working tree's `SKILL.md`** by a fresh agent from modive's directory:
it ran read verbs and the two scripts only, found the cold-start line by its code, reached the same
split, and traced the six waiting checks on its own to one SQLAlchemy engine that signs in to Aurora
with a fresh IAM token — then proposed the connection-legs probe, adapted to modive's names. It found
seven gaps, each fixed and not re-driven: the timed-out attempt writes no line but its retry does, so
the caveat now says the attempt; "the same connection" now reads one engine, one pool, one sign-in; a
probe the project already holds is asked about before another is proposed; the probe signs in with the
function's own `sslmode`; the probe's CloudWatch cost is stated; the report cites the project files a
Step 4 decision rests on; and the p75 line has its wording. It also noted an INIT of 9.97 s that no line
remarked on, so `cold-path.py` now counts INITs within a second of the ceiling.

**Not verified:** `/phil:lambda-web-app-speed` itself, which runs the installed copy until this releases.

## Wave: DISCUSS / [REF] Slice 04a delivered and replayed (2026-10-26)

**D17, decided 2026-10-26 by the user:** rank fixes by the time each saves, largest first; effort breaks
near-ties, and the standard pattern goes first among equals (D13). A fix no measurement can predict is
listed apart as an experiment. This replaces US-04's "saving per unit of effort", which put a quick
0.7 s fix above a day's 2.3 s one and so could never pass its own replay test, and it agrees with
Principle 5. The replay's pass test becomes: where the measurement divides the time, the real gains
fall in the order estimated.

**Slice 04 split.** 04a, here: the ranking and its stopping line, V3, the rule's remaining Principles and
its Advisory list. 04b: pricing the warmth options from the app's own traffic, and the browser trace.

**V3 closed.** NIST SP 800-63B-4, read 2026-10-26: an inactivity timeout ends a session "without
activity from the subscriber"; "The RP SHALL NOT interpret the presence of an access token as an
indicator of the subscriber's presence in the absence of other signals"; nothing defines activity or
names polling or heartbeats. So "a background request is not the person's activity" stays an Advisory
question, framed by those two sentences.

**What landed.** `scripts/rank.py` orders the candidates, lists experiments, drops savings inside the
noise below the line, keeps other paths apart, draws the stopping line, and refuses a candidate with no
evidence. The skill's Step 5 builds the candidates from Steps 3 and 4 alone. The rule gained Principles
6 to 12 — rank by time saved and try what no measurement predicts; stop at the target; hold INIT to a
budget; buy warmth on purpose; static assets; the bundle; cached views — and an Advisory list: bytecode,
a background request as activity, deployment checks in INIT, Lambda Web Functions, and an uncapped
connection count. Each rank rule was removed once to watch a test catch it.

**The replay holds the revised hypothesis, after the fact.** Fixture 03 replays beatrix's record at two
points, every figure from a measurement taken before its fix and cited by issue note. After memory, with
per-phase and per-call timings, the ranking put concurrent checks with Bedrock moved out (2.13–2.47 s
estimated) above bytecode (0.74–1.02 s); the real gains were 2.3–2.4 s and 0.69–0.86 s, the largest
first. Before the INIT move, no timing line existed, so the ranking claimed nothing and listed building
during INIT (first byte −5.3 s, with smaller changes) and more memory (1.2–1.5 s) as experiments — which
is what beatrix did, unmeasured. The original hypothesis, the three largest gains in the top three by
saving per effort, fails on this record by construction. Two limits: D17 was chosen knowing this record,
and only two fixes rank, so no tie-break is exercised on real figures. A held-out case waits for a project
that measures before it fixes.

**What the reviews caught, each fixed.** `plugin-dev:plugin-validator` passed with one major finding and
`plugin-dev:skill-reviewer` rated the change "needs improvement".
- The first fixture broke Step 5's own definitions: a browser first byte as `now_ms`, a noise figure with
  no source, kilobytes read as milliseconds, and a bytecode estimate no rule derived. It was rebuilt on
  the cold wait, the spread of repeated cold starts, and a stated basis per saving.
- Step 5 needed arithmetic by hand. Each saving now names its basis — a call removed, calls made
  concurrent, a batch, a time scaled by a measured fraction — and `rank.py` computes it; `cold-path.py`
  reports the cold wait, each cold start's INIT plus its first invoke, since medians do not add.
- The default target borrowed TTFB's 0.8 s, a client-side p75 over all page loads, for a server-side cold
  path. The target is now the project's or the person's, and with none there is no stopping line.
- `rank.py` recommended a fix for a path already within its target, accepted any `kind` and a string
  `standard`, and hid why a range was too wide; all fixed, each with a test watched failing.
- Step 5 never said where candidates come from, or showed their full shape; it now does both, and lists
  experiments even where Step 4 proposed an instrument.
- Principle 9 said no option survives Lambda's recycle; provisioned environments are re-initialised in
  the background, so it now says a ping cannot stop the recycle. Principle 6 overstated the INIT move's
  gain. Every Advisory bullet now names its source, and a test checks each; the bytecode bullet no longer
  reads as a question about a package without bytecode.
- `review-code` never said to raise this rule's Advisory bullets. It now raises them where a file shows
  the subject, and fixture 07 expects one: the module-scope connection with no cap in the stack.

**`phil:eos`** rewrote two sentences of the new Principles; **`/phil:harden-instructions`** closed one
case Step 5 left open, and flags the skill body at about 2,450 words, past plugin-dev's 2,000-word ideal:
Step 5's candidate format is the first to move to a reference.

**Fixture 07, third blind drive**, of this working tree's `review-code` after the Advisory bullet landed:
all fourteen load-time items, LWS-15 twice; the expected Advisory question on the uncapped connection;
no look-alike. It also raised the deployment-checks Advisory question and a `coding.md` §8 item on the
bare connection, both allowed. Noted, unfixed: the fixture gzips without `Vary: Accept-Encoding`, which
LWS-13's Preferred form names and no row's Violation covers.

**Not verified:** a run of Step 5 on live data. modive's drill ends at the probe, and beatrix's
cold-start line declares one metric and keeps its phases as plain properties, so Step 4 rightly finds no
usable line there — a project with a rich line in another shape gets no drill yet.

## Wave: DISCUSS / [REF] Slice 04b delivered and dogfooded (2026-10-26)

**What landed.** Step 6 prices keeping the function warm: `cold-path.py` now reports the traffic —
active hours, the peak of environments busy in a minute, the invoke time — and `scripts/warmth.py`
fetches the Region's prices from AWS's public price list, which needs no credentials, and prices
provisioned concurrency for one environment and the peak, SnapStart where the runtime and partition
offer it, and a heartbeat from open pages, each per month and per cold start at least. Step 7 measures
one page load: `scripts/firstbyte.py --get` times DNS, TCP, TLS and the wait of one GET, and `--split`
matches the function's `REPORT` to it and divides the first byte into the network, the function and the
front door — the first-byte slice US-02 moved here. LCP comes from a browser trace where the session has
one, or the person's Lighthouse run. Step 5's candidate format moved to `references/candidates.md`.
Fixtures 04 and 05 hold real prices, real traffic and a real cold load; each pricing and matching rule
was removed once to watch a test catch it.

**Dogfood, read-only.** Warmth for modive's simulation API, priced from fourteen days of its traffic and
GovCloud West's price list (published 2026-10-22): provisioned concurrency $23.92 a month for one
environment, $95.74 for the measured peak of four, at least $0.10 for each cold start removed; SnapStart not available
for Python in GovCloud; a heartbeat while pages are open, under a cent. One page load of beatrix's
production landing route, after a quiet spell: first byte 4.21 s — network 0.27 s, the function 3.33 s
(INIT 3.31 s), the front door 0.62 s — against TTFB's 0.8 s; the next load, warm, 0.48 s, most of it
the client's network. A Chrome DevTools trace of a warm load gave LCP 1.17 s (first byte 0.25 s, render
delay 0.91 s); CrUX holds no field data for the page. One load each, not the 75th percentile.

**What the live runs taught.** The first split found no `REPORT`: CloudWatch receives lines seconds
late, so the step fetches again once. The second found none either: the `REPORT` was stamped 285 ms
before the GET began, since the client's clock and AWS's differ, so the window now reaches three
seconds either side.

**What the reviews caught, each fixed.** `plugin-dev:plugin-validator` failed the change and
`plugin-dev:skill-reviewer` rated it "needs improvement".
- Hard rule 1 forbade invoking the function while Step 7 loaded a page that runs it, and can start it
  cold. Step 7 now asks the person first, as D12 requires of forcing a cold start, and the rule names it
  as its one exception; the command takes `--url`.
- The per-cold-start price was labelled "at most"; divided by every cold start, it is the least each
  removed one costs. Relabelled "at least" everywhere.
- SnapStart for Java was priced as for Python and called unavailable in GovCloud; AWS charges nothing
  for Java's, and GovCloud bars only Python and .NET. An arm64 function was priced at x86 rates; Step 1
  now reads the architecture and `warmth.py --arch` the `-ARM` prices. A container image is named as
  having no SnapStart.
- A truncated fetch was priced as a whole window, and a stopped `cold-path.py` read as a price failure;
  both are refused with their own message. Warmth is now priced over fourteen days whatever window
  Step 3 measured, so its length comes from the script.
- The first-byte match accepted a `REPORT` whose invoke began before the GET; it now matches on the
  invoke's span, refuses a split the figures cannot hold, refuses a response that is not 2xx and a
  SnapStart restore, and names everything the remainder holds — the front door, placement, one round
  trip and, cold, Lambda's setup before INIT. `--get` prints the fetch window, so no step works it out.
- Step 7 now runs GET, trace, split, so the trace gives CloudWatch its seconds; the trace takes one load
  with no other interaction, reported as warm, and says whether the browser was signed in.
- The skill description had grown past Claude Code's 1,024-character limit; it is 796, and a test holds
  the limit. The stop-handling lists moved to `references/when-a-script-stops.md`, bringing the body under
  plugin-dev's 3,000-word flag.

**Blind drive, read-only, of the whole command** by a fresh agent, against beatrix's production function
and its landing page, the person's agreement given: INIT owns 99% of the cold path, 3.10 s at p50 over 59
cold starts; provisioned concurrency $23.94 a month for one environment, $71.81 for the peak of three,
SnapStart unavailable in GovCloud; a cold load's first byte 4.57 s — network 0.74 s, the function 3.11 s
(INIT 3.10 s), the rest 0.72 s; a warm traced load's LCP 1.00 s, in an isolated browser, not signed in.
Read verbs and the five scripts only. It found five gaps, each fixed and not re-driven: Step 4 had no
way to find a timing line whose name no one knew, so it now filters on the layer's dimension; beatrix's
line times INIT as one undivided phase, which the decision list let pass as a cause, so a one-phase
line now counts as no timing line and `phases.py` says it divides nothing; the convention could not be
confirmed without the code, and now says so; `warmth.py` did not print the cold starts Step 6 names;
and the trace's sequence risked loading the page twice. It also met more timing lines than cold starts,
which `phases.py` now explains, and warm invokes up to 4.6 s that no step addresses.

**Not verified:** `/phil:lambda-web-app-speed` itself, which runs the installed copy until this releases.
