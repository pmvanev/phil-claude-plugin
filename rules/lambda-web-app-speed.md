---
paths:
  - "**/*.tf"
  - "**/template.y*ml"
  - "**/serverless.y*ml"
  - "**/vite.config.*"
  - "**/webpack.config.*"
  - "**/.size-limit*"
---

# Lambda Web App Speed Guide

Guidelines drawn from the AWS Lambda Developer Guide (the execution environment lifecycle, memory, Python packaging, provisioned concurrency and SnapStart), the AWS GovCloud (US) User Guide, AWS's 2025 posts on INIT billing and cold starts, and the Serverless Applications Lens; RFC 9110, RFC 9111, RFC 8246 and RFC 5861 with MDN's `Cache-Control` reference; NIST SP 800-63B-4 on session management; web.dev on the HTTP cache, code splitting and performance budgets; the React, webpack, Vite and size-limit documentation; the Python and PostgreSQL documentation; Brendan Gregg's *Performance Analysis Methodology*; and Amdahl's law. Research: `docs/research/web-speed/lambda-web-app-speed-canonical-sources.md`.

This rule owns **how fast a web app served from AWS Lambda loads**: work done at INIT and on each invoke, memory, the deployment package, the options for keeping warm, the HTTP front door and static assets, and the front-end bundle. Neighbouring rules keep what they already own: `coding.md` §8 pooling connections and clients, and §15 batching every call that crosses the network; `react.md` React's idioms; `security.md` every security defect; `ci-pipelines.md` how fast the pipeline runs. Complement those — do not restate them.

**The two halves divide on checkability.** The reviewer half — Always-flag, Advisory and Do not flag — names the defects a handler, an IaC file, a response header or a bundler config shows, each by its `LWS-n` id, and the questions a reviewer asks where a file cannot settle one. The Principles half, which `/phil:lambda-web-app-speed` applies, is design: choosing among fixes needs a measurement, and a file holds none.

---

## Principles — design, not review criteria

No principle yields a review finding. The first seven govern how to measure a slow load and choose its fixes; the last five, how a web app on Lambda is built to load fast.

### 1. Measure, then divide the time

State the problem as latency on a named path — a cold navigation, a warm one, a repeat visit — and divide that path's time into its layers before changing anything. Change only what a measurement points at: applying a list of fixes unmeasured is what Gregg calls the Random Change anti-method, and tuning whatever the team's tools happen to show is his Streetlight. A defect a file plainly shows is the exception, and the Always-flag rows below fix it on sight.

### 2. Count every cold start, including the two that hide

Lambda marks one kind of cold start with `Init Duration`; two other kinds carry none. After an INIT that times out or fails, Lambda retries it inside the first invoke, and that invoke's `REPORT` folds the retry into `Duration`. After an invoke that timed out or crashed, Lambda resets the environment, and the next invoke pays a *suppressed init*, folded the same way. Both read as slow warm invokes, so a count of `Init Duration` misses them, and a warm percentile absorbs them. Read each log stream — one execution environment — in time order to find them. Count INIT timeouts on their own: a person behind one waits ten seconds before the retry begins.

### 3. Measure the code that is running

A window that spans a deploy, or a change of memory, mixes two functions, and its percentiles describe neither. Start the window at the function's last change, and widen it only to gather enough cold starts, saying that the wider window mixes versions.

### 4. Drill one level into the largest slice, timed by the clock

When a slice has a size but no cause, time one level inside it — its phases, then the legs of whatever its slowest phase waits on — and stop at the level that names something to act on. Time concurrent work by the clock around it, and report each concurrent part beside it, never summed: ten startup checks that overlap can sum to five times the second they took together. Where several parts wait alike while the rest finish early, what they share is the next level to time. An instrument added to INIT must cost less than it can find, and one log line per cold start costs microseconds.

### 5. Fix the largest slice first, then measure again

A fix can save no more than the time its slice holds, so the largest slice has the most to give. After each fix, measure again: the largest slice moves, and the next fix belongs to whatever now holds it.

### 6. Rank fixes by the time they save; try what no measurement predicts

Order the fixes on one measured path by the time each saves, largest first; where two save about the same, the cheaper goes first, and among equals the standard, documented pattern. Read each saving off the measurement: a call taken off the path saves its time, calls run one after another and made concurrent save their sum less the slowest, a batch of N calls saves N − 1 of them. A fix that changes the machine rather than the work — more memory, work moved into INIT — has a saving no log measurement predicts: on one project, moving the build into INIT, with smaller changes alongside, cut first byte by 5.3 s, where moving work should save nothing. List it apart as an experiment: make it, measure, keep it or revert it, the cheapest first.

### 7. Stop at the target

Stop when the path meets its target — LCP within 2.5 s and TTFB within 0.8 s at the 75th percentile of page loads, and a cold-path budget the project declares — or when the next fix saves less than the run-to-run noise, or costs more than the delay it removes. A p75 over all requests hides cold starts that are under a quarter of them, so a cold path is measured, and budgeted, as its own population.

### 8. Hold INIT to a budget under its ceiling

Build what every request uses during INIT, and declare how long INIT may take, well under its 10 s limit: an INIT that reaches the limit is retried inside the first invoke, and the person behind it waits for both. AWS has billed INIT since 2025-08-01, so a slow INIT costs money as well as time. When INIT nears its budget, move each check that proves the deployment rather than the instance — a bucket's semantics, a schema's version — to the deploy, and each check a rare path needs to that path's first use.

### 9. Buy warmth on purpose, at a price

Keeping an environment warm is a purchase, never a default. Price each option for the app's own traffic: provisioned concurrency, AWS's documented answer for interactive functions; SnapStart, where the runtime and partition offer it; and a heartbeat from open, signed-in pages, where use is sparse and idle billing unwanted. The cold start worth buying away is the one a present person pays. Lambda recycles environments every few hours even under steady traffic, re-initialising provisioned ones in the background; a ping or heartbeat cannot stop that recycle, so call no scheduled ping a guarantee.

### 10. Serve what never changes from the edge, named by its content

Name each static asset by a hash of its content, let browsers keep it a year, and let the HTML shell revalidate on every load; make validators and compressed copies once, at build time; and serve the assets from S3 behind CloudFront wherever the partition offers CloudFront. LWS-11 to LWS-16 name the defects.

### 11. Send the first route's code alone, and fail the build past its budget

Load every view but the landing one on demand, and hold the bundle to a size budget that fails the build, so growth is a decision rather than drift. LWS-17 to LWS-19 name the defects.

### 12. Show a view's cached data at once, and revalidate behind it

A view a person returns to renders from its cache at once and refreshes in the background, as RFC 5861's stale-while-revalidate does for HTTP; only a failed refresh keeps stale data on screen.

---

## Always-flag — objective defects

Name each finding by its `LWS-n` id and take the fix from the row: copy the row's Preferred form verbatim, then write ` — here: ` and the one change this code needs. **File one item per missing protection**: where a row names two defects, as LWS-15 names compressing and hashing, code with both gets two items. **A defect that a row here and `coding.md` both describe is one item, filed under the `LWS-n` id**, which names the Lambda form of the fix.

**The rows apply to functions a person waits on**: those behind the app's HTTP front door, and those invoked while someone waits, as a Cognito trigger is during sign-in. A function an S3 event, a queue or a schedule starts falls outside every row but the package rows, LWS-5 and LWS-6.

**A row fires only on what the review read.** Where a row turns on a fact the files do not settle — the Region a stack deploys to, a value set in an unread variable or module, an integration or a CI pipeline defined in another repository — raise it as a question instead of an item, and name the unread source.

### INIT and the handler

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| LWS-1 | An SDK client, database pool, HTTP client or app object built by the handler or a route each time it runs — or on its first run and then cached there (`functools.cache`, a global the handler sets) — where every run of that path uses it | Build it at module scope, so INIT builds it once per environment; build lazily only what a rare path uses | AWS Lambda lifecycle, "Optimizing static initialization"; AWS provisioned concurrency docs |
| LWS-2 | A function that serves web requests at Lambda's 128 MB default — `memory_size`, SAM `MemorySize` or Serverless `memorySize` unset, or set to 128 | Size memory by measurement; at 1,769 MB a function has the equivalent of one vCPU | AWS "Configure Lambda function memory" |
| LWS-3 | Network checks or reads run one after another during INIT or on the first invoke — flag each that needs no other's result | Run them concurrently — a `ThreadPoolExecutor`, with every boto3 client built before the threads start, or an `asyncio.TaskGroup` in async code — and batch the calls to one service (`coding.md` §15) | Python `concurrent.futures` and `asyncio` docs; boto3 guide, "Clients", on multithreading |
| LWS-4 | A `count(*)` run only to learn whether a row exists — compared with zero, tested for truth, or discarded | `EXISTS (…)`, or `LIMIT 1` | PostgreSQL docs §9.24.1 |

### The deployment package

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| LWS-5 | `.pyc` files compiled by a Python minor version other than the function's `runtime` — a build step that compiles with another interpreter, or a copy that carries a developer's `__pycache__` into the package | Compile in the build with the runtime's own Python version, or ship no `.pyc` | AWS Python `.zip` packaging docs; Python tutorial §6.1.3 |
| LWS-6 | Test or development dependencies, or test files, in the production deployment package — including a server only a local run imports | Install the production dependency set and copy the production modules only | AWS Lambda lifecycle; AWS, "Understanding and Remediating Cold Starts" (2025) |

### Keeping warm

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| LWS-7 | Provisioned concurrency on an alias or version while the HTTP integration invokes the unqualified function or another qualifier | Point the integration at the alias that holds the provisioned concurrency | AWS provisioned concurrency docs |
| LWS-8 | SnapStart on a Python or .NET function in AWS GovCloud (US); or SnapStart beside provisioned concurrency, Amazon EFS, or ephemeral storage above 512 MB; or SnapStart on a function invoked unqualified, at `$LATEST`, where no snapshot is ever restored — one item per incompatible option | Drop the incompatible option; in GovCloud, keep warm another way or not at all | AWS SnapStart docs; AWS GovCloud (US) User Guide, Lambda, read 2026-10-26 |
| LWS-9 | With SnapStart on, INIT code that generates a unique id or a random seed, or opens a connection used after restore without revalidating it | Generate unique values after restore; revalidate or reopen connections in an after-restore hook or on first use | AWS SnapStart, "Compatibility considerations" |

### The front door and static assets

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| LWS-10 | A Lambda Function URL in an AWS GovCloud (US) stack | API Gateway or an Application Load Balancer | AWS GovCloud (US) User Guide, Lambda, read 2026-10-26 |
| LWS-11 | A content-hashed asset served with a `max-age` below 31536000, or with no `immutable` | `Cache-Control: max-age=31536000, immutable`; add `public` only where requests carry `Authorization` | RFC 8246; MDN `Cache-Control`; web.dev HTTP cache |
| LWS-12 | The HTML shell, or any document that names hashed assets, served with a positive `max-age` and no `no-cache`, or with no `Cache-Control` at all | `Cache-Control: no-cache` | RFC 9111 §4.2.2, §5.2.2.4; MDN `Cache-Control` |
| LWS-13 | Text responses over 1.4 KiB — HTML, scripts, stylesheets, JSON, SVG — sent with no `Content-Encoding` to a client that accepts `br` or `gzip`: a server or route that never compresses, or a CloudFront cache behaviour without `compress = true` over objects stored uncompressed | Precompress static files at build time and compress dynamic text in the server, serving `br` or `gzip` with `Vary: Accept-Encoding`; behind CloudFront, store precompressed objects or set `compress = true` | Chrome Lighthouse, "Enable text compression"; RFC 9110 §8.4; CloudFront, "Serve compressed files" |
| LWS-14 | One strong `ETag` sent for different content codings of the same file — gzip, br and identity | A distinct strong `ETag` per coding, or a weak `ETag` | RFC 9110 §8.8.3 |
| LWS-15 | A handler that compresses or hashes a static file on each request | Precompress and compute `ETag`s at build time, and serve the stored results | RFC 9110 §8.8.3; AWS Lambda billing per millisecond |
| LWS-16 | Static assets — `/assets/*`, scripts, stylesheets, images — routed to a Lambda origin in a stack whose partition offers CloudFront, which every commercial Region's does | S3 behind CloudFront, with Lambda behind the API path only | AWS Serverless Applications Lens, web application; Lambda 6 MB payload quota |

### The bundle

| Id | Violation | Preferred form | Cite |
|---|---|---|---|
| LWS-17 | A production web build that no size budget fails: no `size-limit` step, or equivalent, in the CI the review read, and no webpack `performance.hints: "error"`. A Vite `chunkSizeWarningLimit` above its default is evidence, not the defect | A budget that fails the CI build: a `size-limit` step, or webpack `performance.hints: "error"` | web.dev performance budgets; size-limit; webpack and Vite build docs |
| LWS-18 | `lazy()` called inside a component body, or a lazy component with no `<Suspense>` above it | Call `lazy` at module top level, and wrap the component in `<Suspense>` with a fallback | React `lazy` reference |
| LWS-19 | A static import of any routed view other than the one a first visit lands on, in an app with two or more views — routes in a router, or panes a navigation table selects. One item per router or table | Load every view but the landing one with `lazy` and a dynamic `import()`, under a `<Suspense>` with a fallback | web.dev code splitting; React `lazy` reference |

---

## Advisory — judgment calls, not hard blocks

A reviewer raises these; the author decides. Each needs a measurement, a traffic figure or an intent the files do not show.

- **Shipping compiled bytecode.** Bytecode compiled by the runtime's own Python, in `unchecked-hash` mode, halved one project's imports — and pushed its zip past Lambda's 50 MB direct-upload limit, failing a production deploy. Ask whether the gain was measured, and what holds the zip under 50 MB zipped and 250 MB unzipped. Bytecode from another Python version is LWS-5. *Source: AWS, Python `.zip` packaging and Lambda quotas; Python `compileall`.*
- **A background request that counts as the person's activity.** A keep-warm heartbeat or a poll that resets the session's idle timer keeps a session alive with nobody there. NIST SP 800-63B-4 (read 2026-10-26) ends a session "without activity from the subscriber" and forbids reading "the presence of an access token as an indicator of the subscriber's presence in the absence of other signals"; it does not define activity. Ask whether the idle timer ignores such requests. *Source: NIST SP 800-63B-4, §5.2 and the AAL reauthentication sections.*
- **A check in INIT that proves the deployment rather than the instance** — a bucket's semantics, a schema's version, a model's availability — while INIT nears its budget. Ask whether it belongs in the deploy, or at its feature's first use. *Source: AWS, the Lambda execution environment lifecycle, on INIT's 10 s limit and its billing.*
- **A Node.js web app on a Lambda function and an adapter, in a Region that offers Lambda Web Functions.** Web Functions multiplex up to 128 requests per environment, so cold starts follow environments rather than concurrent requests; at launch (2026-10-12) they ran Node.js 24 only, in five commercial Regions. Ask whether the app should move. *Source: AWS News Blog, "Announcing AWS Lambda Web Functions", 2026-10-12, read 2026-10-26.*
- **Database connections with no cap outside the function.** Connections scale with execution environments, so a pool caps nothing across them. Ask where the cap sits: RDS Proxy, or reserved concurrency. `coding.md` §8 owns the pool itself. *Source: AWS, "Using AWS Lambda with Amazon RDS" and "Understanding Lambda function scaling".*

---

## Do not flag

- **A client built inside the handler on a path few requests take** — an export, an admin action. AWS recommends lazy loading there. It clears LWS-1.
- **No provisioned concurrency, SnapStart or heartbeat.** Keeping warm is a priced choice, not a defect, until a measured cold path misses a stated budget. A scheduled ping is no defect either, though no one should call it a guarantee.
- **A package without `.pyc` files.** It is AWS's own recommendation; whether bytecode pays is measured, not read.
- **Memory between 128 MB and 1,769 MB, or above it.** LWS-2 flags the default alone; any other size is a measured choice.
- **Static assets served by the function where the partition offers no CloudFront**, as in AWS GovCloud (US), whose user guide documents none (read 2026-10-26). LWS-16 stays silent; LWS-11 to LWS-15 still apply.
- **VPC attachment.** Since 2019 it adds no network interface to a cold start, and a function that reaches RDS or ElastiCache needs it.
- **Startup checks run in order where each needs the previous one's result.**
- **A `count(*)` whose number is shown or used.** LWS-4 is a count run only to learn whether a row exists.
- **No `public` on assets fetched without `Authorization`**, and **no `ETag` on hashed, `immutable` assets**: neither changes what a browser does.
- **A text response under 1.4 KiB sent uncompressed.** Lighthouse skips those too.
- **An entry chunk of any size.** LWS-17 fires on a missing budget, never on a size.
- **Lambda layers** shared across functions — a deployment choice.

---

## Sources and Synthesis

Each row cites its sources beside it; the works named at the top are the chief ones. Gregg supplies the first Principle and, with his Drill-Down method, the fourth; AWS's lifecycle page the INIT retry and the suppressed init behind the second; Amdahl's law, that speeding up one part saves at most that part's share, the fifth; the third is this rule's own, below. web.dev's Core Web Vitals and TTFB pages supply the seventh's targets, and Reinertsen's cost of delay, as `docs/research/ci/ci-pipeline-canonical-sources.md` cites it, its cost test; AWS's lifecycle, billing, provisioned concurrency and SnapStart pages the eighth and ninth; the rows' own sources the tenth and eleventh; RFC 5861 the twelfth. NIST SP 800-63B-4, read 2026-10-26, frames the background-request question, which it does not answer. AWS supplies the rest of the server side: its Lambda Developer Guide, INIT and the handler, memory, packaging, provisioned concurrency and SnapStart; its GovCloud (US) User Guide, read 2026-10-26, the two GovCloud rows and the absence of CloudFront there; its 2025 posts, that INIT has been billed since 2025-08-01 and that unused dependencies cost a cold start; its Serverless Lens, where static assets belong. RFC 9110, 9111 and 8246, MDN and web.dev supply the caching, compression and validator rows, and Chrome's Lighthouse the 1.4 KiB floor; web.dev, React, webpack, Vite and size-limit supply the bundle rows. PostgreSQL's documentation supplies `EXISTS`.

**This rule's own:** the `LWS-n` ids and the wording of every row, distilled from the research's twenty candidates and corrected against two real codebases; the split into Principles, Always-flag, Advisory and Do not flag, which follows `security.md` and `ci-pipelines.md`; and its own readings of the evidence. Both codebases built their app on the first invoke and cached it, which a row about each invoke missed, so LWS-1 names the cached build too. LWS-15 adds Lambda's per-millisecond billing to RFC 9110's validator, which only implies a build step. LWS-16 fires only where CloudFront exists, because a row that flags the only design a partition allows teaches readers to skip it. The third Principle, measuring the code that is running, is this rule's reading of both projects, whose numbers moved with each deploy. And the projects behind this rule measured what the sources left open: in one, compiled bytecode halved import time, and pushed the package past Lambda's 50 MB direct-upload limit. The second Principle's signatures are this rule's own reading of a real function's logs on 2026-10-26: AWS names both hidden kinds without saying how a `REPORT` line shows them, and over fourteen days a count of `Init Duration` found 96 of that function's 105 cold starts. The sixth Principle's experiments come from replaying the other project's record: where the logs divided the time, the estimates fell in the order the real gains did — 2.12–2.47 s estimated for concurrent checks against 2.3–2.4 s, 0.74–1.02 s for bytecode against 0.69–0.86 s — while the two fixes that changed the machine, building during INIT and more memory, saved 5.3 s of first byte (with smaller changes beside it) and 1.2–1.5 s, gains no measurement had predicted. The fourth Principle's arithmetic is the same function's, over its last twelve cold starts on 2026-10-25 and 26: ten concurrent checks whose medians summed to 4.99 s inside a phase the clock timed at 0.92 s. The research lists what it could not settle under Knowledge Gaps.

---

## The Mantra

> **Measure the wait before you fix it; build at INIT what every request uses; serve what never changes from the edge, named by its content; send the first route's code alone; and buy warmth on purpose, at a price.**
