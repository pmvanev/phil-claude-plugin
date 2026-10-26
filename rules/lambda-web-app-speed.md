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

Guidelines drawn from the AWS Lambda Developer Guide (the execution environment lifecycle, memory, Python packaging, provisioned concurrency and SnapStart), the AWS GovCloud (US) User Guide, AWS's posts on INIT billing (2025) and cold starts (2025), and the Serverless Applications Lens; RFC 9110, RFC 9111 and RFC 8246 with MDN's `Cache-Control` reference; web.dev on the HTTP cache, code splitting and performance budgets; the React, webpack, Vite and size-limit documentation; and the Python and PostgreSQL documentation. Research: `docs/research/web-speed/lambda-web-app-speed-canonical-sources.md`.

This rule owns **how fast a web app served from AWS Lambda loads**: work done at INIT and on each invoke, memory, the deployment package, the options for keeping warm, the HTTP front door and static assets, and the front-end bundle. Neighbouring rules keep what they already own: `coding.md` §8 pooling connections and clients, and §15 batching every call that crosses the network; `react.md` React's idioms; `security.md` every security defect; `ci-pipelines.md` how fast the pipeline runs. Complement those — do not restate them.

**The two halves divide on checkability.** The reviewer half — Always-flag and Do not flag — names defects a handler, an IaC file, a response header or a bundler config shows, each by its `LWS-n` id. The Principles half, which arrives with the planned `/phil:lambda-web-app-speed` command, is design: choosing among fixes needs a measurement, and a file holds none.

---

## Principles — design, not review criteria

Not yet written. They land with the planned `/phil:lambda-web-app-speed` command, which measures a cold path before it ranks a fix. Until then, this rule is its reviewer half alone, and no principle yields a finding.

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
| LWS-8 | SnapStart on a Python or .NET function in AWS GovCloud (US); or SnapStart beside provisioned concurrency, Amazon EFS, or ephemeral storage above 512 MB; or SnapStart on `$LATEST` — one item per incompatible option | Drop the incompatible option; in GovCloud, keep warm another way or not at all | AWS SnapStart docs; AWS GovCloud (US) User Guide, Lambda, read 2026-10-26 |
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

The rows cite the works named at the top. AWS's Lambda Developer Guide supplies INIT and the handler, memory, packaging and both warmth options; its GovCloud user guide, read on 2026-10-26, the two GovCloud rows and the absence of CloudFront there; its 2025 posts, that INIT has been billed since 2025-08-01 and that unused dependencies cost a cold start; its Serverless Lens, where static assets belong. RFC 9110, 9111 and 8246, MDN and web.dev supply the caching, compression and validator rows, and Chrome's Lighthouse the 1.4 KiB floor; web.dev, React, webpack, Vite and size-limit supply the bundle rows. PostgreSQL's documentation supplies `EXISTS`.

**This rule's own:** the `LWS-n` ids and the wording of every row, distilled from the research's twenty candidates and corrected against two real codebases; the split into Principles, Always-flag and Do not flag, which follows `security.md` and `ci-pipelines.md`; and four readings. Both codebases built their app on the first invoke and cached it, which a row about each invoke missed, so LWS-1 names the cached build too. LWS-15 adds Lambda's per-millisecond billing to RFC 9110's validator, which only implies a build step. LWS-16 fires only where CloudFront exists, because a row that flags the only design a partition allows teaches readers to skip it. And the projects behind this rule measured what the sources left open: in one, compiled bytecode halved import time, and pushed the package past Lambda's 50 MB direct-upload limit. The research lists what it could not settle under Knowledge Gaps.

---

## The Mantra

> **Build once per environment, not once per request; serve what never changes from the edge, named by its content; send the first route's code alone; and buy warmth on purpose, at a price.**
