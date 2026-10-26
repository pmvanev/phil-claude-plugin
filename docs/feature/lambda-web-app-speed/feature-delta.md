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
