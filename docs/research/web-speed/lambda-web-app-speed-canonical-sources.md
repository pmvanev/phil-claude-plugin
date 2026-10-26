# Research: Canonical Sources for a Lambda Web-App Speed Rule

**Date**: 2026-10-26 | **Researcher**: nw-researcher (Nova) | **Confidence**: High for INIT lifecycle and billing, memory-to-CPU, keep-warm options, HTTP caching and bundle rows; Medium for `.pyc` packaging, VPC residual cost, connection-count rows and the ranking procedure; Low for the background-activity principle and the Goldratt and Reinertsen quotations | **Sources**: 52

> Input to a future `rules/lambda-web-app-speed.md` (working name) with two halves — **Principles** and
> an **always-flag reviewer table** — and to a companion skill that measures a cold start and a page
> load, finds where the time goes, ranks fixes by payoff per effort and stops where returns fall off.
> Each finding uses: **Work** / **Evidence** / **Canonicity** / **Contributes** / **Checkable in a file?** / **Caveats**.
> Access date for every web source: 2026-10-26 unless stated.
> Scope: `rules/coding.md` §8 (pooling, scope-bound ownership) and §15 (batch network calls) are cited,
> not re-researched; only their Lambda-specific part is added. `rules/react.md`, `ux.md` and `ui.md`
> were skimmed; overlaps are cross-referenced.

## Executive Summary

**The INIT claim is half wrong.** Building clients, pools and the app object in Lambda's INIT phase is
still AWS's guidance, because a warm environment reuses them. But "INIT is free" has been false since
2025-08-01: AWS now bills INIT for every configuration, and it was never free for container images,
custom runtimes or provisioned concurrency. The 10-second INIT limit is real; an INIT that exceeds it is
retried inside the first invoke under the function timeout, and an invoke error causes a "suppressed init"
that hides inside the next `REPORT` line's `Duration`. AWS states the memory dial exactly: "At 1,769 MB,
a function has the equivalent of one vCPU", up to about 6 vCPUs at 10,240 MB. That more vCPUs do little
for single-threaded Python follows from Python's GIL; AWS never states it. Shipping `.pyc` is contested:
Python says bytecode speeds loading and is meant for unwritable directories, while AWS advises against
shipping `__pycache__` in zips. The safe form compiles with the runtime's own interpreter, and the effect
should be measured.

**Keep-warm resolves cleanly, with a GovCloud twist.** AWS names provisioned concurrency for web apps
and calls scheduled pings "not a guaranteed way to reduce cold starts". SnapStart supports Python 3.12+
in commercial Regions, but the GovCloud (US) guide says "Lambda SnapStart for Python and .NET is not
available"; Function URLs and JSON logs are unavailable there too. Every environment is recycled "every
few hours" whatever the warming. Since 2019, VPC attachment no longer costs an ENI per cold start, but an
idle VPC function goes `Inactive` after 14 days and its first invoke fails. Connections scale with
environments, so the Lambda-specific half of `coding.md` §8 is one connection per environment, capped
outside the function by RDS Proxy or reserved concurrency. One new fact the claim list missed: AWS
launched **Lambda Web Functions** on 2026-10-12. They multiplex up to 128 requests per environment, but
only for Node.js 24 in five commercial Regions.

**The front-end and HTTP claims hold at standard level.** RFC 9111, RFC 8246, MDN and web.dev agree on
`max-age=31536000, immutable` for hashed assets and `no-cache` for the HTML shell. RFC 9110 requires a
distinct strong ETag per content coding, which a build step produces naturally. AWS's Serverless Lens
serves static assets from S3 through CloudFront, with Lambda only behind the API. Route-level `lazy`
splitting and a budget are canonical, but webpack and Vite only *warn* by default, so a budget binds
only when it fails the build. For the procedure, Gregg's Time Division and Drill-Down methods,
Goldratt's constraint focus and Reinertsen's U-curve combine with Core Web Vitals targets (LCP ≤ 2.5 s;
TTFB ≤ 0.8 s as a diagnostic) into "measure, cut the largest slice, stop at target or when cost exceeds
delay saved". Twenty always-flag rows result (LWS-1 to LWS-20).

## Research Methodology

**Search Strategy**: Primary sources first. AWS documentation (Lambda Developer Guide, GovCloud User
Guide, CloudFront, CloudWatch, Well-Architected) and AWS-authored blog posts for platform behaviour.
IETF RFCs at rfc-editor.org for HTTP. MDN and web.dev for web platform metrics. docs.python.org and
postgresql.org for language and database behaviour. Vendor docs (React, Vite, webpack, size-limit, uv,
TanStack Query, SWR) for each tool's own defaults. Brendan Gregg's methodology page for procedure; Goldratt
and Reinertsen inherited from the CI research. Third-party blogs appeared in search results and were not
used as support.
**Source Selection**: Types: official, standards, technical docs. Reputation: high for every row-bearing
claim. **Verification**: AWS-behaviour claims checked across several AWS pages (lifecycle, billing,
provisioned concurrency, SnapStart, GovCloud); HTTP claims across IETF, MDN and Google; front-end claims
across Google, React and bundler docs. Page dates recorded; 2018-era web.dev pages are marked.
**Quality Standards**: Target 3 sources per major claim, 1 authoritative minimum; unconfirmed facts are
marked in place and collected in Knowledge Gaps. Avg reputation ≈ 0.93.

---

## Findings

## 1. Lambda execution environment, INIT phase and billing

### 1.1 AWS Lambda Developer Guide, "Understanding the Lambda execution environment lifecycle"

**Work**: AWS. *AWS Lambda Developer Guide*, "Understanding the Lambda execution environment lifecycle".
https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html (official, high; page
undated, current text read 2026-10-26).
**Evidence**: "In the `Init` phase, Lambda performs three tasks: Start all extensions (`Extension
init`) / Bootstrap the runtime (`Runtime init`) / Run the function's static code (`Function init`)".
"The `Init` phase is limited to 10 seconds. If all three tasks do not complete within 10 seconds, Lambda
retries the `Init` phase at the time of the first function invocation with the configured function
timeout." "The 10-second timeout doesn't apply to functions that are using provisioned concurrency,
SnapStart, or Lambda Managed Instances. For provisioned concurrency, SnapStart, and Managed Instances
functions, your initialization code can run for up to 15 minutes. The time limit is 130 seconds or the
configured function timeout (maximum 900 seconds), whichever is higher." "If the `Init` phase is
successful, Lambda doesn't emit the `INIT_REPORT` log unless SnapStart or provisioned concurrency is
enabled." On an invoke failure Lambda resets the environment and the next invoke re-runs INIT: "This is
called a *suppressed init*. When suppressed inits occur, Lambda doesn't explicitly report an additional
**INIT** phase in CloudWatch Logs. Instead, you might notice that the duration in the REPORT line
includes an additional **INIT** duration + the **INVOKE** duration." "For functions using on-demand
concurrency, Lambda might occasionally initialize execution environments ahead of invocation requests
... We recommend you to not take a dependency on this behavior." "Lambda terminates execution
environments every few hours to allow for runtime updates and maintenance—even for functions that are
invoked continuously." "Objects declared outside of the function's handler method remain initialized
... if your Lambda function establishes a database connection, instead of reestablishing the connection,
the original connection is used in subsequent invocations." On cold starts: "You are charged for this
time, and it adds latency to your overall invocation duration." "Cold starts typically occur in under 1%
of invocations. The duration of a cold start varies from under 100 ms to over 1 second." "The largest
contributor of latency before function execution comes from initialization code." Factors: "The size of
the function package, in terms of imported libraries and dependencies, and Lambda layers. / The amount
of code and initialization work. / The performance of libraries and other services in setting up
connections and other resources." "Static initialization is also often the best place to open database
connections ... However, you might have large numbers of objects that are only used in certain execution
paths in your function. In this case, you can lazily load variables in the global scope to reduce the
static initialization duration."
**Canonicity**: The service's own definition of the lifecycle; every other source in this section
restates it.
**Contributes**: (a) **Candidate claim 1, first half, confirmed**: build clients and pools in static
init so warm invokes reuse them — AWS's own example creates `boto3.client('s3')` at module scope. (b)
**The 10-second limit is real, but the consequence is a retry, not a failure**: an INIT over 10 s is
re-run inside the first invoke under the function timeout, so the user waits for both. (c) A web app's
first request after an invoke error pays a *suppressed init* that the `REPORT` line hides inside
`Duration` — a measurement trap for the skill. (d) Even a continuously invoked function cold-starts
"every few hours", so keep-warm can never reach zero cold starts. (e) AWS names lazy loading for objects
"only used in certain execution paths" — the balance to (a).
**Checkable in a file?** Partly. Module-scope client and pool construction versus construction inside
the handler is visible in code. The 10-second limit is visible only in logs (`INIT_REPORT ... Status:
timeout`, or `Init Duration` near 10 000 ms).
**Caveats**: "under 1%" is a fleet-wide figure; a low-traffic web app sees a far higher cold-start share
(AWS itself says development functions cold-start more often). Lambda Managed Instances (concurrent
invokes, customer-owned capacity) follow a different lifecycle and were not researched; see Knowledge
Gaps.

### 1.2 AWS Compute Blog, "AWS Lambda standardizes billing for INIT phase" (2025)

**Work**: Shubham Gupta, Jeff Gebhart (AWS). AWS Compute Blog, 2025-04-29.
https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/ (AWS authors on
aws.amazon.com, high). The Developer Guide (1.1) links to it from the sentence "You are charged for this
time".
**Evidence**: "Effective August 1, 2025, AWS will standardize billing for the initialization (INIT)
phase across all function configurations." Before, INIT was unbilled only for "on-demand invocations of
Lambda functions packaged as ZIP files that use managed runtimes"; "functions configured with custom
runtimes, Provisioned Concurrency (PC), or OCI packaging" "already included the INIT phase duration in
their Billed Duration." Worked example: `Duration: 250.06 ms` with `Init Duration: 100.77 ms` billed
251 ms before and 351 ms after. "You can decrease INIT phase duration by reducing package size, resulting
in faster cold starts and lower INIT costs." "INITs (cold starts) typically occur in under 1% of
invocations." It supplies a Logs Insights query that estimates the unbilled INIT share:
```
filter @type = "REPORT"
stats
sum((@memorySize/1000000/1024) * (@billedDuration/1000)) as BilledGBs,
sum((@memorySize/1000000/1024) * ((@duration + @initDuration - @billedDuration)/1000)) as UnbilledInitGBs,
UnbilledInitGBs / (UnbilledInitGBs + BilledGBs) as UnbilledInitRatio
```
**Canonicity**: AWS's announcement of the change; the Developer Guide now cites it.
**Contributes**: **Candidate claim 1's "INIT is free up to 10 s" is refuted.** Since 2025-08-01 INIT is
billed for every configuration at the Region's on-demand duration rate. INIT was never free for
container images, custom runtimes (including `provided.al2023`) or provisioned concurrency. The *design*
advice in claim 1 survives on latency and reuse grounds alone; only the cost argument is gone. Work moved
into INIT is now paid once per environment instead of once per invoke — still the cheaper place for
anything the invokes share.
**Checkable in a file?** No; a rule or comment asserting "INIT is free" is checkable as stale prose.
**Caveats**: The post is written in the future tense before the change; no later AWS revision was found
(searched 2026-10-26). Whether AWS ever documented a CPU boost during INIT for small memory sizes — a
widely repeated community claim — was not found on any AWS page; see Knowledge Gaps.

### 1.3 AWS Compute Blog, "Understanding and Remediating Cold Starts: An AWS Lambda Perspective" (2025)

**Work**: Aakash Bhattacharya, Tian Wen (AWS). AWS Compute Blog, 2025-08-07.
https://aws.amazon.com/blogs/compute/understanding-and-remediating-cold-starts-an-aws-lambda-perspective/
(high). Page text was truncated in retrieval; sections on X-Ray and Logs Insights were not seen.
**Evidence**: "The size and number of dependencies directly affects initialization time"; "keep your
deployment ZIP packages small, remove unused dependencies"; "Employ lightweight libraries and implement
lazy loading for resources to further cut initialization time." VPC: "the Lambda service creates an
Elastic Network Interface"; "applying this configuration might introduce additional latency"; "you
should only use it when access to VPC resources is necessary." Memory: more memory gives "more CPU
power", "often improving cold start performance." "SnapStart is an efficient cold start solution,
currently available for Java, Python, and .NET functions." Containers: "pulling large images from ECR
might contribute to cold start latency"; "keep your image sizes minimal by removing unnecessary
artifacts." Measurement: "The INIT duration metric, found in the REPORT section of function logs".
**Canonicity**: AWS's current (post-billing-change) cold-start guidance, by AWS solutions architects.
**Contributes**: Corroborates 1.1 on package size, dependencies and lazy loading (claim 11); still names
VPC as a possible latency source (claim 12, see 5.1); names SnapStart for Python (claim 10).
**Checkable in a file?** Partly: unused dependencies in a lockfile, a VPC config on a function that
reaches no VPC resource.
**Caveats**: Several quotations are sentence fragments (retrieval limit). Same publisher as 1.1–1.2, so
independent only of non-AWS sources.

## 2. Memory, CPU and sizing

### 2.1 AWS Lambda Developer Guide, "Configure Lambda function memory"

**Work**: AWS. https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html (official, high).
**Evidence**: "Lambda allocates CPU power in proportion to the amount of memory configured." "You can
configure memory between 128 MB and 10,240 MB in 1-MB increments. At 1,769 MB, a function has the
equivalent of one vCPU (one vCPU-second of credits per second)." "Memory is the principal lever for
controlling the performance of a function." "A higher memory allocation can improve performance for
functions that use imported libraries, Lambda layers, Amazon Simple Storage Service (Amazon S3) or
Amazon Elastic File System (Amazon EFS)." "If a function is CPU, network or memory-bound, then increasing
the memory setting can dramatically improve its performance." It names AWS Lambda Power Tuning, which
"run[s] multiple concurrent versions of a Lambda function at different memory allocations and measure[s]
the performance", and Compute Optimizer recommendations ("supports only functions that use x86_64
architecture").
**Canonicity**: The service's own statement of the memory-to-CPU relation.
**Contributes**: **Candidate claim 2's first half confirmed verbatim**: 1,769 MB is one vCPU-equivalent.
The memory setting is also the cold-start CPU lever — imports and library loading run faster with more
CPU (1.3: "often improving cold start performance").
**Checkable in a file?** Yes: `memory_size` in Terraform (`aws_lambda_function`), `MemorySize` in
SAM/CloudFormation. A web-serving function at the 128 MB default is visible.
**Caveats**: The phrase "one vCPU-second of credits per second" implies a credit/share model below
1,769 MB; AWS publishes no table of fractional CPU per size.

### 2.2 AWS News Blog, "New for AWS Lambda – Functions with Up to 10 GB of Memory and 6 vCPUs" (2020)

**Work**: Danilo Poccia (AWS). AWS News Blog, 2020-12-01.
https://aws.amazon.com/blogs/aws/new-for-aws-lambda-functions-with-up-to-10-gb-of-memory-and-6-vcpus/
(high; [Published 2020; limits unchanged in the 2026 Developer Guide]).
**Evidence**: "Lambda allocates CPU and other resources linearly in proportion to the amount of memory
configured." "That means you can now have access to up to 6 vCPUs in each execution environment." "In
this way, your multithreaded and multiprocess applications run faster." The same limits reached AWS
GovCloud (US) in August 2021 (What's New, 2021-08; title read via search only).
**Canonicity**: AWS's launch post for the current memory ceiling.
**Contributes**: The ceiling (10,240 MB ≈ 6 vCPUs) and AWS's own framing that the extra vCPUs serve
*multithreaded and multiprocess* code.
**Checkable in a file?** As 2.1.
**Caveats**: The post makes no statement about single-threaded code.

### 2.3 Python `threading` docs: the GIL

**Work**: Python Software Foundation. *The Python Standard Library*, `threading`.
https://docs.python.org/3/library/threading.html (official, high; 3.x current docs).
**Evidence**: "In CPython, due to the Global Interpreter Lock, only one thread can execute Python code at
once (even though certain performance-oriented libraries might overcome this limitation). If you want
your application to make better use of the computational resources of multi-core machines, you are
advised to use multiprocessing or concurrent.futures.ProcessPoolExecutor. However, threading is still an
appropriate model if you want to run multiple I/O-bound tasks simultaneously." "As of Python 3.13,
free-threaded builds can disable the GIL ... but this feature is not available by default (see PEP 703)."
**Canonicity**: The language's own documentation.
**Contributes**: **Candidate claim 2's second half is an inference, not an AWS statement — confirmed as
inference.** AWS says extra vCPUs help multithreaded and multiprocess code (2.2); Python says one thread
runs Python bytecode at a time. Together they imply single-threaded CPython CPU work gains little from
memory above 1,769 MB, except where (a) a C library releases the GIL, (b) the code is memory-bound, or
(c) more memory buys network bandwidth (2.1 names network-bound functions). No AWS page states "Python
gains nothing above 1,769 MB"; third-party guides do (medium, not cited as support).
**Checkable in a file?** Partly: `memory_size` above 1769 with a single-threaded Python handler is a
question, not a defect — memory may be needed for its own sake.
**Caveats**: Whether Lambda's managed Python runtimes ship a free-threaded build was not checked; AWS
documents none (Knowledge Gaps). Measure with Power Tuning (2.1) rather than assume.

## 3. Python startup: bytecode, imports, package size

### 3.1 Python docs: compiled files, `compileall`, cached-bytecode invalidation

**Work**: Python Software Foundation. *Tutorial* §6.1.3 "'Compiled' Python files"
(https://docs.python.org/3/tutorial/modules.html); `compileall`
(https://docs.python.org/3/library/compileall.html); *Language Reference* §5.4.6 "Cached bytecode
invalidation" (https://docs.python.org/3/reference/import.html). Official, high.
**Evidence**: "To speed up loading modules, Python caches the compiled version of each module in the
`__pycache__` directory"; "the compiled modules are platform-independent"; the file name encodes the
version, e.g. `spam.cpython-33.pyc`, so "compiled modules from different releases and different versions
of Python [can] coexist". "A program doesn't run any faster when it is read from a `.pyc` file than when
it is read from a `.py` file; the only thing that's faster about `.pyc` files is the speed with which
they are loaded." `compileall` "can be used to create the cached byte-code files at library installation
time, which makes them available for use even by users who don't have write permission to the library
directories." Invalidation: by default "the source's last-modified timestamp and size" are stored and
checked; "For unchecked hash-based `.pyc` files, Python simply assumes the cache file is valid if it
exists." `--invalidation-mode` defaults to `timestamp`, or `checked-hash` when `SOURCE_DATE_EPOCH` is
set.
**Canonicity**: The language's own documentation.
**Contributes**: **Candidate claim 3 confirmed in principle**: precompiled `.pyc` saves only load
(parse and compile) time, which is cold-start time; and precompiling exists precisely for directories the
process cannot write — as Lambda's code directory is (3.2). Without shipped `.pyc`, every cold start
recompiles every imported module and cannot cache the result.
**Checkable in a file?** Yes: a build script that runs `compileall` / `uv ... --compile-bytecode`, or
excludes `__pycache__`, and the `--invalidation-mode` it passes.
**Caveats**: A timestamp `.pyc` is valid only if the source mtime and size survive packaging and
extraction unchanged. ZIP stores DOS times at two-second resolution (PKWARE APPNOTE, prior knowledge,
**not re-verified**), and how Lambda sets mtimes on extraction is **not documented**. A mismatch makes
Python silently recompile on every cold start. `--invalidation-mode unchecked-hash` removes the
dependency on mtimes (interpretation; untested here — see Knowledge Gaps).

### 3.2 AWS: Python `.zip` packaging and the read-only file system

**Work**: AWS. "Working with .zip file archives for Python Lambda functions"
(https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) and "Create a Lambda function using a
container image" (https://docs.aws.amazon.com/lambda/latest/dg/images-create.html). Official, high.
**Evidence**: "We recommend that you don't include `__pycache__` folders in your function's deployment
package. Python bytecode that's compiled on a build machine with a different architecture or operating
system might not be compatible with the Lambda execution environment." "The maximum size for a .zip
deployment package for Lambda is 250 MB (unzipped). Note that this limit applies to the combined size of
all the files you upload, including any Lambda layers." Packages are mounted at `/var/task`; layers
extract to `/opt/python`. "The container image must be able to run on a read-only file system. Your
function code can access a writable `/tmp` directory". "Lambda supports a maximum uncompressed image
size of 10 GB". "For optimal performance, keep your image manifest size under 25,400 bytes." "If a
function is not invoked for multiple weeks, Lambda reclaims its optimized version, and the function
transitions to the `Inactive` state ... Lambda rejects the first invocation".
**Canonicity**: The service's own packaging guidance.
**Contributes**: **Conflicts with candidate claim 3** (see Conflict 1). AWS's stated reason — bytecode
from a different architecture or OS — contradicts Python's "compiled modules are platform-independent";
the real compatibility key is the interpreter version tag and magic number. The safe reading: ship `.pyc`
only when built by the *same Python minor version* as the Lambda runtime (or in the runtime's own build
image), and expect a mismatched `.pyc` to be ignored, not to crash. The read-only file system is
confirmed for images and implied for zip by the `/tmp`-only writable area.
**Checkable in a file?** Yes: a build that compiles bytecode with a Python whose minor version differs
from the function's `runtime`; a zip that ships `__pycache__` built on a developer machine.
**Caveats**: The `.zip` page does not itself say "read-only"; the statement is on the container-image
page. The Inactive state for idle *image* functions (weeks) is a separate first-request penalty from a
cold start.

### 3.3 uv, "Using uv with AWS Lambda"

**Work**: Astral. https://docs.astral.sh/uv/guides/integration/aws-lambda/ (vendor docs, high for uv's
behaviour; page undated).
**Evidence**: Docker image: `ENV UV_COMPILE_BYTECODE=1` with the comment "Enable bytecode compilation,
to improve cold-start performance." Zip: `uv pip install --no-installer-metadata --no-compile-bytecode
--python-platform x86_64-manylinux2014 --python 3.13 --target packages -r requirements.txt`, with no
comment on why bytecode is off. "To generate deterministic zip archives, consider passing the -X flag to
zip". A dependencies layer "can improve cold-start performance for application updates".
**Canonicity**: The packaging tool claim 3 names; authoritative for its flags only.
**Contributes**: Confirms `--compile-bytecode` as a cold-start measure *for images*; its own zip recipe
turns it off, which agrees with AWS 3.2 for zips. Claim 3 is therefore **refined**: compile bytecode in
the image build (the runtime's own interpreter) by default; for zips, compile only with the matching
interpreter, and measure.
**Checkable in a file?** Yes (`UV_COMPILE_BYTECODE`, `--compile-bytecode`, `compileall`).
**Caveats**: uv gives no reason for `--no-compile-bytecode` in the zip recipe; the size cost and the
mtime question (3.1) are plausible reasons, not stated ones.

### 3.4 Package size, dependency closure, lazy imports, layers, images (claim 11)

**Evidence** (from 1.1, 1.2, 1.3, 3.2): AWS names package size, imported libraries and layers as
initialization-latency factors (1.1); "reducing package size, resulting in faster cold starts and lower
INIT costs" (1.2); "remove unused dependencies"; "Employ lightweight libraries and implement lazy loading"
(1.3); import only the SDK clients you need (1.1, Node.js example); lazily load objects "only used in
certain execution paths" (1.1). Layers count toward the 250 MB unzipped limit (3.2) — they move bytes,
they do not remove them (interpretation). Large images "might contribute to cold start latency" (1.3).
**Contributes**: **Claim 11 confirmed** for size and dependency count, from three AWS pages. Layers are
a deployment-reuse tool, not a cold-start tool: no AWS page read says a layer loads faster than the same
bytes in the function zip.
**Checkable in a file?** Yes: unused dependencies in the lockfile; dev/test dependencies in the
production package; whole-SDK imports where one client serves; heavy imports at module scope used on one
route.
**Caveats**: No AWS page gives a size-to-latency curve; the effect must be measured per app. Python's
own `-X importtime` (prior knowledge, documented in the command-line docs; **not re-read this session**)
is the tool that shows which imports cost the most.

## 4. Keeping the server warm

### 4.1 AWS Lambda Developer Guide, "Configuring provisioned concurrency"

**Work**: AWS. https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html (official,
high). Also the lifecycle page (1.1), section "Reducing cold starts with Provisioned Concurrency".
**Evidence**: Provisioned concurrency is "the number of pre-initialized execution environments allocated
to your function ... designed to make functions available with double-digit millisecond response times.
Generally, interactive workloads benefit the most from the feature. Those are applications with users
initiating requests, such as web and mobile applications". "Configuring provisioned concurrency incurs
additional charges". "You cannot use provisioned concurrency with the $LATEST version of any function."
"Lambda uses on-demand instances to handle any excess traffic"; the environment variable
`AWS_LAMBDA_INITIALIZATION_TYPE` reads `provisioned-concurrency` or `on-demand`. "Lambda bills you for
initialization even if the environment instance never processes a request." "If your function receives
predictable traffic patterns, use scheduled scaling." "Lambda emits the `ProvisionedConcurrencyUtilization`
metric only when your function is active ... auto-scaling alarms enter the `INSUFFICIENT_DATA` state ...
This might lead to unexpected billing." Lifecycle page: "If you need predictable function start times for
your workload, provisioned concurrency is the recommended solution to ensure the lowest possible latency."
"Concurrency = (average requests per second) * (average request duration in seconds)"; "Lambda suggests
adding a 10% buffer".
**Canonicity**: AWS's named answer to cold starts for interactive workloads.
**Contributes**: (a) The recommended keep-warm mechanism, named by AWS for "web and mobile
applications". (b) **Checkable traps**: provisioned concurrency on `$LATEST` is refused; an integration
(API Gateway, Function URL, ALB target) that points at the unqualified function bypasses an alias's
provisioned environments ("ensure that you are invoking the version of alias with provisioned concurrency
configured"). (c) A sizing formula for the skill. (d) Scheduled scaling fits office-hours web apps.
**Checkable in a file?** Yes: `aws_lambda_provisioned_concurrency_config` with `qualifier`, and whether
the HTTP integration's URI names the same alias.
**Caveats**: Cost is continuous; the skill must price it against the cold starts it removes.

### 4.2 AWS Lambda Developer Guide, "Improving startup performance with Lambda SnapStart"; AWS GovCloud (US) User Guide

**Work**: AWS. https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html and
https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-lambda.html (official, high).
**Evidence**: SnapStart supports "Java 11 and later / Python 3.12 and later / .NET 8 and later" across
ZIP and container-image formats on AWS base images. "SnapStart does not support provisioned concurrency,
Amazon Elastic File System (Amazon EFS), Amazon S3 Files, or ephemeral storage greater than 512 MB." "You
can't use SnapStart on a function's unpublished version ($LATEST)." "Lambda SnapStart is available in all
commercial Regions except Asia Pacific (New Zealand) and Asia Pacific (Taipei)." "SnapStart works best
when used with function invocations at scale. Functions that are invoked infrequently might not
experience the same performance improvements." "Use provisioned concurrency if your application has
strict cold start latency requirements that can't be adequately addressed by SnapStart." Network
connections: "The state of connections that your function establishes during the initialization phase
isn't guaranteed when Lambda resumes your function from a snapshot. Validate the state of your network
connections and re-establish them as necessary." Uniqueness: generate "unique IDs, unique secrets, and
entropy" after initialization. Pricing (non-Java): a caching charge per published version ("minimum of 3
hours") and a "restoration charge" per restore; "For Java managed runtimes, there's no additional cost".
Restore must complete "within the timeout limit (10 seconds)" (1.1). **GovCloud**: "Lambda SnapStart for
Python and .NET is not available." The same list: "AWS Lambda Function URLs is not available." "JSON log
formatting is not available." A September 2024 What's New post announced SnapStart for *Java* in
GovCloud (read via search result only).
**Canonicity**: The service's own feature and partition documentation.
**Contributes**: **Candidate claim 10 resolved for SnapStart**: available for Python 3.12+ in commercial
Regions, **not available for Python in AWS GovCloud (US)**. A Python web app in GovCloud has two
platform options — provisioned concurrency or scheduled pings — plus the in-code levers (sections 2–3).
SnapStart's snapshot also breaks the "open the DB pool in INIT" pattern unless connections are validated
after restore. GovCloud's lack of Function URLs and JSON logs constrains the front door and the
`platform-initReport` measurement path.
**Checkable in a file?** Yes: `snap_start { apply_on = "PublishedVersions" }` with a Python runtime in a
`us-gov-*` provider; SnapStart with `provisioned_concurrency_config`, EFS or ephemeral storage > 512 MB;
`aws_lambda_function_url` in a GovCloud stack.
**Caveats**: Partition availability changes; recheck before encoding. Pricing figures not read.

### 4.3 AWS Compute Blog, "Operating Lambda: Performance optimization – Part 1" (2021)

**Work**: James Beswick (AWS). AWS Compute Blog, 2021-04-26.
https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/ (high).
**Evidence**: "The broader serverless community provides open source libraries to "warm" Lambda
functions via a pinging mechanism. This approach uses EventBridge rules to schedule invocations of the
function every minute ... However, this is not a guaranteed way to reduce cold starts." "each additional
concurrent invocation of the function requires a new execution environment"; "Each environment has to be
set up independently, so each invocation experiences a full cold start." After a code or configuration
update, "the next invocation results in a cold start."
**Canonicity**: AWS's "Operating Lambda" series, the closest AWS text to a stated position on warmers.
**Contributes**: **Candidate claim 10, scheduled pings: AWS calls them "not a guaranteed way" and
recommends provisioned concurrency instead (4.1).** One ping keeps at most one environment warm; a second
concurrent user, a deploy, or the every-few-hours recycle (1.1) still cold-starts. Pings remain the only
option for a GovCloud Python app that will not pay for provisioned concurrency — a defensible, cheap,
best-effort choice, not a guarantee.
**Checkable in a file?** Yes: an EventBridge `schedule_expression` targeting the web function; whether
the handler short-circuits the ping before touching the database or session store.
**Caveats**: 2021 text; consistent with the 2025–2026 pages read.

### 4.4 Background requests and user activity (claim 10, last part)

**Work**: OWASP. *Session Management Cheat Sheet*.
https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html (standards body,
high).
**Evidence**: "All sessions should implement an idle or inactivity timeout." The idle timeout "limits the
chances an attacker has to guess and use a valid session ID from another user"; attackers "can generate
activity on the session periodically to keep the session active for longer periods of time." "Session
timeout management and expiration must be enforced server-side." "All sessions should implement an
absolute timeout, regardless of session activity."
**Contributes**: The principle under the claim: an idle timeout measures *human* inactivity. A request
the page issues on its own — a warming ping, a stale-while-revalidate refetch (8), a poll — that renews
the session turns the idle timeout off for any open tab (**interpretation**; OWASP does not discuss
client-initiated background requests).
**Checkable in a file?** Partly: a session middleware that refreshes expiry on every request, combined
with a client poller or refetch-on-interval, is visible.
**Caveats**: No source found that states "background requests must not extend the idle timeout"
outright; NIST SP 800-63B-4's reauthentication section was not read for it. Low-Medium confidence.

## 5. VPC, database connections and startup work

### 5.1 VPC attachment: Hyperplane ENIs (claim 12)

**Work**: Chris Munns (AWS). "Announcing improved VPC networking for AWS Lambda functions". AWS Compute
Blog, 2019-09-03. https://aws.amazon.com/blogs/compute/announcing-improved-vpc-networking-for-aws-lambda-functions/
(high). AWS. "Giving Lambda functions access to resources in an Amazon VPC".
https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html (official, high).
**Evidence**: 2019: "The network interface creation happens when your Lambda function is created or its
VPC settings are updated"; the change "dramatically reduces the latency that was previously associated
with creating" network interfaces at cold start; "the network interfaces are shared across execution
environments". Current guide: "The first time you attach a function to a VPC using a particular subnet
and security group combination, Lambda creates a Hyperplane ENI. Other functions in your account that use
the same subnet and security group combination can also use this ENI." "For new functions, while Lambda
is creating a Hyperplane ENI, your function remains in the Pending state and you can't invoke it ...
which can take several minutes." "if a Lambda function remains idle for 14 days, Lambda reclaims any
unused Hyperplane ENIs and sets the function state to `Inactive`. The next invocation attempt will fail,
and the function re-enters the Pending state". "When you attach your function to a VPC, it can only
access resources available within that VPC. To give your function access to the internet, you also need
to configure the VPC to have internet access." The 2025 cold-start post (1.3) still says VPC "might
introduce additional latency" and to "only use it when access to VPC resources is necessary."
**Canonicity**: AWS's announcement of the change and the current service guide.
**Contributes**: **Claim 12 refined.** Since 2019 the ENI is built at create/update time, not per cold
start, so VPC attachment is no longer a per-cold-start cost of seconds. Two residual costs remain: (a) a
function idle 14 days goes `Inactive` and its first invoke *fails* — a real outage for a rarely used
internal web app, and a reason a weekly ping may be justified on availability rather than speed grounds
(interpretation); (b) AWS SDK and other outbound calls from a VPC function need a NAT gateway or VPC
endpoints, whose path adds latency (not quantified by any source read).
**Checkable in a file?** Yes: `vpc_config` on a function whose code reaches no VPC resource; a VPC
function calling AWS services with no VPC endpoint or NAT route in the same stack.
**Caveats**: The 2025 post's "additional latency" is unquantified; no AWS page read gives a current
VPC-attached versus not cold-start delta. Medium confidence on "no longer a cold-start factor".

### 5.2 Database connections under Lambda concurrency (Lambda-specific part of `coding.md` §8)

**Work**: AWS. "Using AWS Lambda with Amazon RDS".
https://docs.aws.amazon.com/lambda/latest/dg/configuration-database.html; "Understanding Lambda function
scaling" https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html (official, high).
**Evidence**: "Direct connections are useful in simple scenarios, and proxies are recommended for
production. A database proxy manages a pool of shared database connections which enables your function
to reach high concurrency levels without exhausting database connections." "We recommend using Amazon RDS
Proxy for Lambda functions that make frequent short database connections, or open and close large numbers
of database connections." "Amazon RDS charges an hourly rate for proxies". Concurrency: "For each
concurrent request, Lambda provisions a separate instance of your execution environment." During Init and
Invoke "this execution environment is busy and cannot process other requests." Reserved concurrency can
prevent a function "from overloading downstream resources". Scaling: "1,000 execution environment
instances every 10 seconds" per function. The lifecycle page (1.1): "if your Lambda function establishes
a database connection, instead of reestablishing the connection, the original connection is used in
subsequent invocations. We recommend adding logic in your code to check if a connection exists before
creating a new one."
**Canonicity**: The service's own guidance.
**Contributes**: What is Lambda-specific about `coding.md` §8's "The application owns the pool": (a)
**the application is one execution environment**, and each environment serves one request at a time, so
an in-process pool larger than one connection holds idle connections (interpretation from "busy and
cannot process other requests"); (b) **database connections ≈ concurrent environments × pool size**, and
concurrency scales by up to 1,000 environments per 10 s, so the cap belongs outside the function — RDS
Proxy, or reserved concurrency as a hard ceiling; (c) the pool lives in module scope (1.1) and must be
validated before use, because a frozen environment's socket may be dead on thaw and a SnapStart restore
does not guarantee it (4.2).
**Checkable in a file?** Yes: pool `max_size`/`pool_size` above 1 in a Lambda handler module; a
connection opened inside the handler on every request without a proxy; a Lambda-to-RDS stack with
neither `aws_db_proxy` nor `reserved_concurrent_executions`.
**Caveats**: AWS's own Python RDS sample opens the connection *inside* the handler on every call,
contradicting its lifecycle page; cite the lifecycle page. Async frameworks that run several coroutines
in one invoke (rare on Lambda) can use more than one connection. RDS Proxy adds a network hop and an
hourly cost; whether it adds per-query latency was not measured by any source read.

### 5.3 Startup checks: run them concurrently; ask for existence, not a count (claim 5)

**Work**: Python. "Coroutines and Tasks" (`asyncio.gather`, `asyncio.TaskGroup`).
https://docs.python.org/3/library/asyncio-task.html (official, high). PostgreSQL 18.6 Documentation
§9.24.1 `EXISTS`. https://www.postgresql.org/docs/current/functions-subquery.html (official, high).
PostgreSQL Wiki, "Slow Counting" (last edited 2021-04-10). https://wiki.postgresql.org/wiki/Slow_Counting
(project wiki, medium-high).
**Evidence**: `asyncio.gather`: "Run awaitable objects in the *aws* sequence *concurrently*." "TaskGroup
provides stronger safety guarantees than gather ... if a task ... raises an exception, TaskGroup will,
while gather will not, cancel the remaining scheduled tasks." PostgreSQL: "The subquery will generally
only be executed long enough to determine whether at least one row is returned, not all the way to
completion." Wiki: "PostgreSQL must walk through all rows to determine visibility. This normally results
in a sequential scan reading information about every row in the table."
**Canonicity**: Language and database vendor documentation.
**Contributes**: **Claim 5 confirmed for both halves.** Independent startup I/O (secrets fetch, schema
check, cache warm) costs the *sum* of round trips when sequential and roughly the *maximum* when
concurrent; `TaskGroup` cancels the rest on the first failure, which fits a fail-fast startup. A
`count(*)` used to ask "is there any row?" scans the table under MVCC; `EXISTS` / `LIMIT 1` stops at the
first row. This is the database-side twin of `coding.md` §15 (batch every network call) — cite §15 for
round-trip count, this finding for per-query cost.
**Checkable in a file?** Yes: `SELECT count(*)` whose result is compared only with zero; sequential
`await` of independent startup calls; startup checks in the request path rather than INIT.
**Caveats**: The wiki is a community page on postgresql.org; MySQL/InnoDB behaviour was not researched.
Concurrency in INIT only helps when the checks are I/O-bound (2.3).

## 6. Static assets: caching, validators, compression, where to serve them

### 6.1 RFC 9111 "HTTP Caching" and RFC 8246 "HTTP Immutable Responses" (claim 6)

**Work**: R. Fielding, M. Nottingham, J. Reschke (eds.). RFC 9111, June 2022.
https://www.rfc-editor.org/rfc/rfc9111.html. P. McManus. RFC 8246, September 2017.
https://www.rfc-editor.org/rfc/rfc8246.html. (IETF Standards Track, high.)
**Evidence**: RFC 9111 §4.2.2: "a cache MAY assign a heuristic expiration time when an explicit time is
not specified" ("A typical setting of this fraction might be 10%" of the time since `Last-Modified`).
§5.2.2.4 `no-cache`: the response "MUST NOT be used to satisfy any other request" without successful
validation on the origin server. §5.2.2.9 `public`: "a cache MAY store the response even if it would
otherwise be prohibited". RFC 8246 abstract: `immutable` "allows servers to identify resources that will
not be updated during their freshness lifetime. This ensures that a client never needs to revalidate a
cached fresh resource"; §2: "Clients SHOULD NOT issue a conditional request during the response's
freshness lifetime (e.g., upon a reload) unless explicitly overridden by the user (e.g., a force
reload)"; the introduction's pattern "allows a very large freshness lifetime to be used for the
sub-resource without guessing when it will be updated in the future."
**Canonicity**: The HTTP caching standard and its immutable extension.
**Contributes**: **Claim 6 confirmed** at standard level: a content-hashed URL never changes content, so
a year-long freshness plus `immutable` removes even reload revalidation; the HTML that names the hashes
must revalidate every use (`no-cache`), or a user keeps an old shell pointing at old (or deleted) asset
hashes. A response with *no* `Cache-Control` is not uncached: §4.2.2 lets caches guess.
**Checkable in a file?** Yes — in server code, CloudFront response-headers policies, S3 object metadata
in the deploy script: hashed asset paths without a long `max-age` + `immutable`; the HTML shell without
`no-cache` (or with a long `max-age`); any HTML or asset response with no `Cache-Control` at all.
**Caveats**: `public` is not required for unauthenticated assets; it matters only where the request
carries `Authorization` (MDN, 6.2). `immutable` support varies by browser (web.dev, 6.2).

### 6.2 MDN "Cache-Control" and web.dev "Prevent unnecessary network requests with the HTTP Cache"

**Work**: MDN contributors. "Cache-Control". https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
(last modified 2026-09-17; canonical web reference, high). Ilya Grigorik, Jeff Posnick (Google). web.dev,
https://web.dev/articles/http-cache (last updated 2018-11-05; high; [Published 2018; concept remains
current]).
**Evidence**: MDN, cache-busting use case: "You can add a long `max-age` value and `immutable` because the
content will never change. `# /assets/*` `Cache-Control: max-age=31536000, immutable`"; "Use a `no-cache`
to make sure that the HTML response itself is not cached ... `# /index.html` `Cache-Control: no-cache`".
"If you don't add a `Cache-Control` header because the response is not intended to be cached, that could
cause an unexpected result. Cache storage is allowed to cache it heuristically". `public` is needed for
shared caching only where `index.html` sits behind HTTP authentication: "you also need one of `public`,
`s-maxage` or `must-revalidate`." web.dev: versioned URLs get `Cache-Control: max-age=31536000`;
`immutable` is an optional addition "some browsers ignore"; `no-cache` "instructs the browser that it must
revalidate with the server every time before using a cached version of the URL"; "We recommend using
`ETag` because it's more accurate" than `Last-Modified`.
**Canonicity**: MDN is the canonical web reference; web.dev is Google's Chrome team guidance.
**Contributes**: Two independent restatements of claim 6 with the exact header values. Refinement: the
claim's `public` is optional for anonymous static assets; the minimum is `max-age=31536000, immutable`.
**Checkable in a file?** As 6.1.
**Caveats**: web.dev's article is 2018; MDN's is current and agrees.

### 6.3 RFC 9110 "HTTP Semantics": entity tags and content codings (claim 7)

**Work**: R. Fielding, M. Nottingham, J. Reschke (eds.). RFC 9110 (STD 97), June 2022.
https://www.rfc-editor.org/rfc/rfc9110.html (IETF, high).
**Evidence**: §8.8.3: "The "ETag" field in a response provides the current entity tag for the selected
representation". §8.8.1: "A "strong validator" is representation metadata that changes value whenever a
change occurs to the representation data". §8.8.3.3 shows the same resource as `ETag: "123-a"` unencoded
and `ETag: "123-b"` with `Content-Encoding: gzip`, noting "a strong entity tag for a content-encoded
representation has to be distinct". §13: "A recipient MUST use the weak comparison function when
comparing entity tags for If-None-Match".
**Canonicity**: The HTTP semantics standard.
**Contributes**: **Claim 7 refined.** An ETag is a function of the representation bytes, so it can be
computed once at build time for each (file, encoding) pair and stored beside the file — the standard
requires a distinct strong tag per content coding, which a build step naturally produces. Computing a
hash or compressing per request on Lambda spends billed CPU on every request for an answer fixed at
build time (interpretation). For *hashed* assets with `immutable`, ETags barely matter: the client does
not revalidate while fresh (6.1).
**Checkable in a file?** Yes: a handler that hashes or gzips a static file per request; the same strong
ETag sent for gzip, brotli and identity bodies.
**Caveats**: Section 8.4.1 (content codings) was not read this session; brotli's `br` coding is RFC 7932
(prior knowledge, not re-read).

### 6.4 Where static assets belong: AWS Serverless Applications Lens, CloudFront compression, Lambda quotas

**Work**: AWS Well-Architected, *Serverless Applications Lens*, "Web application".
https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/web-application.html;
CloudFront Developer Guide, "Serve compressed files".
https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html; "Lambda
quotas". https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html (official, high).
**Evidence**: Lens reference architecture: "**Amazon S3** hosts web application static assets such as
HTML, CSS, JavaScript and images. Content is securely served through CloudFront." "**Amazon CloudFront**
provides a better user experience by accelerating content delivery of static assets and calls to your
backend compute layer." "An **AWS Lambda** function provides create, read, update, and delete (CRUD)
operations". "For single-page web applications you can use AWS Amplify Hosting to manage atomic
deployments, cache expiration and custom domains." CloudFront: "When the viewer supports both Gzip and
Brotli, CloudFront uses Brotli"; "CloudFront compresses objects that are between 1,000 bytes and
10,000,000 bytes in size"; "When a response from an origin includes the `Content-Encoding` header,
CloudFront doesn't compress the object"; "CloudFront compresses objects on a best-effort basis. In rare
cases, CloudFront skips compressing an object when CloudFront experiences high traffic load ... it caches
the uncompressed object"; on compression it converts a strong ETag to weak (`W/`). Lambda quotas:
invocation payload "6 MB each for request and response (synchronous)"; "1 MB for the total combined size
of request line and header values". Lambda Web Functions launch post (6.5): "Static assets are served
from the cache while dynamic requests route to your Web Function."
**Canonicity**: AWS's reference architecture for serverless web apps.
**Contributes**: **Claim 7's second question answered**: AWS's canonical layout serves static assets
from S3 through CloudFront, with Lambda behind the API path only. Serving assets from Lambda pays an
invoke (and possibly a cold start) per asset miss, and caps each at 6 MB. Precompressing at build time
and uploading with `Content-Encoding` avoids CloudFront's best-effort skip and its size window
(interpretation from the "skips compressing" and size-range sentences).
**Checkable in a file?** Yes: a Lambda route serving `/assets/*` or `*.js`; a CloudFront behaviour for
static paths whose origin is the Lambda/API; `Compress = false` (or no Brotli in the cache policy) with
no precompressed objects.
**Caveats**: The lens page is undated (search snippet dated it 2022). Where a team must serve assets
from the app (e.g. no CloudFront in GovCloud stack), build-time compression and ETags (6.3) are the
fallback. CloudFront in GovCloud was not researched.

### 6.5 AWS News Blog, "Announcing AWS Lambda Web Functions" (2026) — claim 13

**Work**: Micah Walter (AWS). AWS News Blog, 2026-10-12.
https://aws.amazon.com/blogs/aws/announcing-aws-lambda-web-functions-for-fast-consistent-web-app-performance-anywhere/
(high). Quotas: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html.
**Evidence**: Web Functions are "a new form factor that lets you run standard HTTP web applications on
Lambda." "Each execution environment handles multiple requests simultaneously (up to 128 concurrent
requests per environment)"; "a burst of incoming traffic can share warm environments instead of mapping
each request to a new one." "Web Functions meter the CPU time your code uses"; "Memory is metered for as
long as the execution environment exists." "Web Functions run Node.js 24 (nodejs24.x) on Arm64 at
launch." Regions at launch: US East (N. Virginia), US East (Ohio), US West (Oregon), Asia Pacific
(Tokyo), Europe (Ireland). "Lambda Event Functions are what you already know as Lambda functions."
Quotas page: Web Function "Initialization timeout (time for your server to start listening) 10 seconds";
"vCPUs per execution environment 2"; "Memory per execution environment 2 GB"; "Concurrent requests per
environment (maxConcurrencyPerEnvironment) 64 (range 1–128)"; "Deployment package size 512 MB
(unzipped)".
**Canonicity**: AWS's launch announcement, two weeks old at access.
**Contributes**: **The largest item claim 13 adds.** For a web app, AWS now offers a form factor whose
environments multiplex requests, so cold starts scale with environments, not concurrent requests, and a
pool larger than one connection per environment becomes correct again (contrast 5.2). It is Node.js-only
and commercial-Region-only at launch, so a Python or GovCloud app cannot use it today.
**Checkable in a file?** Partly: a Node.js web app on an Event Function behind an adapter, in a launch
Region, is a candidate for migration (advisory only).
**Caveats**: Two weeks old; behaviour, pricing and Regions will change. Not cross-verified outside AWS.
Web Function quota "Initialization timeout 10 seconds" is the same ceiling as Event Function INIT (1.1).

## 7. Front-end bundle

### 7.1 Route-level code splitting: web.dev and React `lazy` (claim 8)

**Work**: Houssein Djirdeh, Jeremy Wagner (Google). "Reduce JavaScript payloads with code splitting".
https://web.dev/articles/reduce-javascript-payloads-with-code-splitting (last updated 2018-11-05; high;
[Published 2018; concept remains current]). React. "lazy". https://react.dev/reference/react/lazy
(official, high).
**Evidence**: web.dev: "Split the JavaScript bundle to only send the code needed for the initial route
when the user loads an application." "Splitting on the route or component level when using a client-side
framework is a simpler approach"; bundlers "support dynamic imports". React: "`lazy` lets you defer
loading component's code until it is rendered for the first time." "you also need to specify what should
be displayed while it is loading ... wrapping the lazy component or any of its parents into a
`<Suspense>` boundary". "Do not declare `lazy` components *inside* other components ... always declare
them at the top level of your module".
**Canonicity**: Google's web-performance guidance and React's own reference.
**Contributes**: **Claim 8's first half confirmed**: split at routes; each lazy route needs a Suspense
fallback, which `rules/ux.md` already requires as a loading state ("Data-driven view with no loading /
empty / error state") — cross-reference, do not restate.
**Checkable in a file?** Yes: a router whose route components are all static imports; `lazy()` declared
inside a component body (re-created each render); a `lazy` component with no `Suspense` ancestor.
**Caveats**: `rules/react.md` does not cover `lazy`; the new rule (or `react.md`) owns this row. Splitting
adds requests; on HTTP/2 the cost is small but not zero (not researched).

### 7.2 Bundle-size budgets: web.dev, size-limit, webpack, Vite (claim 8)

**Work**: Milica Mihajlija. "Performance budgets 101". https://web.dev/articles/performance-budgets-101
(2018-11-05; high). size-limit README. https://github.com/ai/size-limit (vendor, high for the tool).
webpack. "Performance". https://webpack.js.org/configuration/performance/ (official). Vite. "Build
Options" (v8.3.4). https://vite.dev/config/build-options (official).
**Evidence**: web.dev: "A performance budget is a set of limits imposed on metrics that affect site
performance." Budget kinds: quantity-based (page weight, "maximum script size"), milestone timings
("user-centric performance metrics"), rule-based (Lighthouse). Suggested start: "Under 5 s Time to
Interactive" and under 170 KB of critical-path resources "compressed/minified"; example: "Our product page
must ship less than 170 KB of JavaScript on mobile". Tools named: webpack performance features,
bundlesize, Lighthouse CI. size-limit: "Calculate the real cost to run your JS app or lib to keep good
performance"; it "throws an error if the cost exceeds the limit"; `@size-limit/file` "checks the size of
files with Brotli (default), Gzip or without compression"; `limit` such as "10 kB". webpack:
`maxAssetSize` and `maxEntrypointSize` default `250000` bytes; `hints` defaults to `'warning'` in
production; "We recommend using `hints: "error"` during production builds to help prevent deploying
production bundles that are too large". Vite: `build.chunkSizeWarningLimit` default `500` (kB) — a
warning only; `build.reportCompressedSize` default `true`.
**Canonicity**: Google guidance plus the bundlers' and budget tool's own docs.
**Contributes**: **Claim 8's second half confirmed**: a budget is only enforced when it *fails the
build*. webpack's default is a warning; Vite's is a warning; size-limit and `hints: "error"` fail. The
170 KB figure is web.dev's suggested starting point, not a standard.
**Checkable in a file?** Yes: no size-limit (or equivalent) config, or a webpack `performance.hints`
other than `"error"`, in a production SPA; a Vite `chunkSizeWarningLimit` raised to silence the warning.
**Caveats**: Budgets measured uncompressed (webpack's bytes) and compressed (size-limit's brotli) are not
comparable; the rule should name the unit. TTI has been retired by Chrome in favour of INP/TBT (prior
knowledge, not re-verified); prefer Core Web Vitals (9.3) for milestone budgets.

## 8. Data caching per view

### 8.1 RFC 5861, MDN, TanStack Query, SWR (claim 9)

**Work**: M. Nottingham. RFC 5861 "HTTP Cache-Control Extensions for Stale Content", May 2010,
Informational. https://www.rfc-editor.org/rfc/rfc5861.html (high). MDN "Cache-Control" (6.2). TanStack
Query, "Important Defaults".
https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults (vendor docs, high for
the library; no version shown). SWR, "Getting Started". https://swr.vercel.app/docs/getting-started
(vendor docs).
**Evidence**: RFC 5861 §3: `stale-while-revalidate` "indicates that caches MAY serve the response in
which it appears after it becomes stale"; caches "SHOULD attempt to revalidate it while still serving
stale responses." §4 `stale-if-error`: "a cached stale response MAY be used to satisfy the request". MDN:
"the cache could reuse a stale response while it revalidates it". TanStack Query defaults: cached data is
considered stale by default; stale queries refetch in the background when "New instances of the query
mount", "The window is refocused", "The network is reconnected"; "inactive" queries are garbage collected
"after 5 minutes"; failed queries are "silently retried 3 times, with exponential backoff delay". SWR
dedupes, caches and shares requests with the same key and refreshes on focus or reconnect.
**Canonicity**: The HTTP extension that named the pattern, and the two dominant React data libraries.
**Contributes**: **Claim 9 confirmed**: show the cached view at once, refetch behind it, keyed per view
(query key). Two Lambda-specific consequences (interpretation): (a) default refetch-on-focus and
refetch-on-mount multiply invokes — every tab focus is a request, possibly a cold one; set `staleTime`
deliberately; (b) a background refetch is not user activity and must not renew an idle session (4.4).
**Checkable in a file?** Yes: `useQuery`/`useSWR` with default `staleTime: 0` on an expensive endpoint;
`refetchInterval` with `refetchIntervalInBackground: true`; a fetch-in-`useEffect` with no cache
(`rules/react.md` says `useEffect` is for synchronization — cross-reference).
**Caveats**: RFC 5861 is Informational and governs HTTP caches; the client libraries borrow the name, not
the protocol. TanStack's `staleTime` default value was not quoted verbatim on the page read.

## 9. Measurement (claim 4)

### 9.1 Lambda's own numbers: `REPORT`, `INIT_REPORT`, Logs Insights, Lambda Insights

**Work**: AWS lifecycle page (1.1); billing post (1.2); CloudWatch Logs "Sample queries".
https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-examples.html; "Monitor function
performance with Amazon CloudWatch Lambda Insights".
https://docs.aws.amazon.com/lambda/latest/dg/monitoring-insights.html; provisioned-concurrency page
(4.1). Official, high.
**Evidence**: `REPORT` lines carry `Duration`, `Billed Duration`, `Memory Size`, `Max Memory Used` and,
on a cold start, `Init Duration` (1.1 examples). Successful INIT emits no `INIT_REPORT` "unless SnapStart
or provisioned concurrency is enabled"; a suppressed init hides inside `Duration` and is visible only as
the gap between `START` and `REPORT` timestamps or via the Telemetry API's events "with `phase=invoke`"
(1.1). Sample queries: `filter @type = "REPORT" | stats avg(@duration), max(@duration), min(@duration) by
bin(5m)`; an over-provisioned-memory query on `@memorySize` and `@maxMemoryUsed`; slow invocations with
`@duration > 1000`. The billing post's query uses `@initDuration` (1.2). Lambda Insights "collects,
aggregates, and summarizes system-level metrics including CPU time, memory, disk and network usage" and
"diagnostic information such as cold starts"; it runs as an extension "provided as a Lambda layer";
"every function invocation sends about 1KB of log data". Provisioned concurrency logs `Init Duration` in a
`platform-initReport` event in JSON log format (4.1); GovCloud: "JSON log formatting is not available"
(4.2).
**Canonicity**: The platform's own telemetry.
**Contributes**: The skill's server-side measurements: cold-start share = count of `REPORT` lines with
`@initDuration` over all `REPORT` lines; INIT p50/p95 from `@initDuration`; warm handler time from
`@duration` where `@initDuration` is absent. A query of the form `filter @type = "REPORT" | stats
count(*) as invokes, count(@initDuration) as cold, pct(@initDuration, 95) as p95Init, pct(@duration, 95)
as p95Dur` is a composition of the documented fields (**interpretation**; not an AWS sample verbatim).
**Checkable in a file?** No; run-time evidence.
**Caveats**: Lambda Insights is itself an extension, and extensions start during INIT (1.1: "Start all
extensions") — measuring with it adds to what it measures (interpretation). `pct()` and `count(field)`
semantics in Logs Insights were not re-read this session.

### 9.2 Browser side: Navigation Timing, `Server-Timing`, TTFB

**Work**: Barry Pollard, Jeremy Wagner (Google). "Time to First Byte (TTFB)". https://web.dev/articles/ttfb
(updated 2025-11; high). MDN. "Server-Timing".
https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Server-Timing (last modified
2026-07-28; high).
**Evidence**: TTFB "measures the time between starting navigating to a page and when the first byte of a
response begins to arrive"; it "is the sum of" redirect time, service worker startup, DNS lookup,
"Connection and TLS negotiation", and the request "up until the point at which the first byte of the
response has arrived." "most sites should strive to have a TTFB of 0.8 seconds or less"; "poor values are
greater than 1.8 seconds"; "TTFB isn't a Core Web Vitals metric". "You can measure the TTFB of navigation
requests in the browser with the Navigation Timing API" (`responseStart`). MDN: `Server-Timing`
"communicates one or more performance metrics about the request-response cycle to the user agent", e.g.
`Server-Timing: cache;desc="Cache Read";dur=23.2`; "may expose potentially sensitive application and
infrastructure information ... you may decide to only show metrics to authenticated users"; the
`PerformanceServerTiming` interface "is restricted to the same origin, but you can use the
`Timing-Allow-Origin` header".
**Canonicity**: Google's metric definition and the canonical web reference.
**Contributes**: The join between server and browser: emit `Server-Timing` entries (`init`, `db`,
`render`) from the handler so one browser navigation shows where the server's share of TTFB went. A
Lambda cold start lands entirely inside TTFB's last phase, so TTFB on a cold navigation minus TTFB on a
warm one approximates the user-visible cold-start cost (interpretation).
**Checkable in a file?** Yes: whether the app emits `Server-Timing`, and whether it does so on
unauthenticated responses (MDN's exposure warning).
**Caveats**: A Lambda handler cannot time the platform's INIT from inside the invoke except by recording
a module-load timestamp; the INIT share in `Server-Timing` is therefore approximate.

### 9.3 Core Web Vitals and RAIL: what "fast" means to the user

**Work**: web.dev. "Web Vitals". https://web.dev/articles/vitals (updated 2024-10-31; high). web.dev.
"Measure performance with the RAIL model". https://web.dev/articles/rail (updated 2020-06-10; high).
**Evidence**: "LCP should occur within 2.5 seconds of when the page first starts loading"; "pages should
have a INP of 200 milliseconds or less"; "pages should maintain a CLS of 0.1. or less"; "a good threshold
to measure is the 75th percentile of page loads, segmented across mobile and desktop devices". RAIL:
"Make users the focal point of your performance effort"; Core Web Vitals "is the recommended approach for
defining performance goals over RAIL."
**Canonicity**: Google's current user-centric targets; RAIL is the predecessor it names as superseded.
**Contributes**: The skill's target and stopping signal: LCP ≤ 2.5 s and TTFB ≤ 0.8 s at p75. A cold
start shows up in TTFB, then pushes LCP; bundle size shows up between TTFB and LCP.
**Checkable in a file?** No.
**Caveats**: p75 hides cold starts if they are under 25% of loads — the reason the skill must measure the
cold path separately (interpretation; AWS's "under 1%" figure, 1.1, makes this likely for busy apps and
unlikely for low-traffic ones).

### 9.4 Python import profiling

**Work**: Python. "Command line and environment", `-X importtime`.
https://docs.python.org/3/using/cmdline.html (official, high).
**Evidence**: "`-X importtime` to show how long each import takes. It shows module name, cumulative time
(including nested imports) and self time (excluding nested imports)." "Added in version 3.7."
`PYTHONPROFILEIMPORTTIME=1` is equivalent. `-B` / `PYTHONDONTWRITEBYTECODE`: "Python won't try to write
`.pyc` files on the import of source modules."
**Contributes**: The tool that splits a Python INIT into per-module cost, so the skill can rank lazy-import
candidates (3.4) by measured self time. Setting `PYTHONPROFILEIMPORTTIME=1` as a Lambda environment
variable writes the report to stderr, hence CloudWatch Logs (interpretation; not tested).
**Checkable in a file?** No (diagnostic).

## 10. Procedure: bottleneck, payoff per effort, stopping rule

### 10.1 Brendan Gregg, "Performance Analysis Methodology"

**Work**: Brendan Gregg. https://www.brendangregg.com/methodology.html (author's site, last updated
2025-01-23; medium-high to high — Gregg is the author of *Systems Performance*, Addison-Wesley; book
editions prior knowledge, **not re-verified**).
**Evidence**: Anti-methods: Streetlight ("Pick observability tools that are" familiar ... "Look for
obvious issues"); Random Change ("Pick a random attribute to change (eg, a tunable)"); Blame-Someone-Else.
Problem Statement Method: "What makes you think there is a performance problem?"; "Has this system ever
performed well?"; "Can the performance degradation be expressed in terms of latency or run time?". USE
method: "For every resource, check:" utilization, saturation, errors. Time Division Method ("I previously
called this the "Latency Analysis Method""): "Measure operation time (or latency)" then divide it.
Drill-Down: "Start at highest level"; "Examine next-level details"; "Pick most interesting breakdown"; "If
problem unsolved, go to 2". Stopping: "Methodologies can help with another difficult issue: when to give
up." "Performance engineers can spend six months working a single issue without success, when it would
be better to try for a week".
**Canonicity**: The most cited practitioner methodology in systems performance (USE method).
**Contributes**: **The skill's diagnostic loop.** For a page load the operation is the navigation; the
Time Division method splits it into DNS/TLS, cold-start INIT, handler (by `Server-Timing` phase),
transfer, and front-end parse/render; Drill-Down picks the biggest slice. The anti-methods name what the
skill must not do: apply the list of fixes in this document without measuring (Random Change), or tune
what the team's tools happen to show (Streetlight). The Problem Statement questions are the skill's
opening. USE fits resource questions (memory at 128 MB, DB connection saturation) better than latency
questions.
**Checkable in a file?** No.
**Caveats**: Author's site, not peer-reviewed; quotations are short fragments.

### 10.2 Goldratt and Reinertsen (cross-reference)

`docs/research/ci/ci-pipeline-canonical-sources.md` §6.5–6.6 already carries both, with their caveats
(secondary quotations, unverified against the books). What transfers: Goldratt's "an hour saved at a
non-bottleneck is a mirage" is the warrant for fixing the largest time slice first (10.1's Drill-Down
reaches it); "repeat, because the constraint moves" — after the cold start is fixed, the bundle or a
query becomes the constraint. Reinertsen's U-curve gives the stopping rule: stop when the next fix costs
more (build complexity, monthly spend such as provisioned concurrency or RDS Proxy, maintenance) than the
user delay it removes. Confidence: Low for the quotations, Medium for the procedure.

### 10.3 Ranking by payoff per effort; stopping (synthesis, interpretation)

No source read gives a numeric payoff-per-effort ranking for web-speed fixes. Assembled from the sources:
1. **Payoff** = (seconds removed on the affected path) × (share of loads on that path). Cold-path fixes
   pay only on the cold share (9.1); bundle fixes pay on every first visit; cache-header fixes pay on
   every repeat visit (6.1).
2. **Effort** includes recurring cost: provisioned concurrency and RDS Proxy bill by the hour (4.1,
   5.2); SnapStart for Python bills caching and restores (4.2); pings cost almost nothing but guarantee
   nothing (4.3).
3. **Stop** when the measured p75 meets the target (LCP ≤ 2.5 s, TTFB ≤ 0.8 s, 9.3) *and* the cold path
   meets the team's stated cold-start budget, or when the next fix's cost exceeds its delay saved
   (Reinertsen), or when a fix's measured gain is inside run-to-run noise (Gregg's "when to give up").
Confidence: Medium (procedure from three independent sources; ranking formula is interpretation).

## Synthesis

### Candidate claims tested against sources

| # | Candidate claim | Verdict | Evidence | Confidence |
|---|---|---|---|---|
| 1 | Build app, clients and DB pool in INIT; "INIT is free up to 10 s" | **Design confirmed; cost claim refuted.** INIT is billed for every configuration since 2025-08-01, and never was free for images, custom runtimes or provisioned concurrency. The 10 s limit is real; an INIT over it is *retried inside the first invoke* under the function timeout, and an invoke error causes a *suppressed init* hidden inside the next `REPORT` `Duration`. AWS balances static init with lazy loading for objects on rare paths. | 1.1, 1.2, 4.1 | High |
| 2 | 1,769 MB = one vCPU; single-threaded Python gains little above it | **First half confirmed verbatim; second half is a sound inference AWS does not state.** AWS: extra vCPUs help "multithreaded and multiprocess applications"; Python: the GIL lets one thread run Python bytecode at a time. Exceptions: memory-bound code, C extensions that release the GIL, network bandwidth. | 2.1, 2.2, 2.3 | High / Medium |
| 3 | Ship compiled `.pyc` (`--compile-bytecode`, `compileall`) | **Refined, with a conflict.** Python: `.pyc` saves load time only, and `compileall` exists for unwritable directories, as Lambda's are. AWS: do not ship `__pycache__` in zips (compatibility). uv: compile for images, not in its zip recipe. Compile with the runtime's own Python minor version (image build or matching interpreter); consider `--invalidation-mode unchecked-hash`; measure. | 3.1–3.3, Conflict 1 | Medium |
| 4 | Measure first: `REPORT`, `@initDuration`, Logs Insights, X-Ray/Lambda Insights, Navigation/Resource Timing, `Server-Timing`, TTFB, LCP | **Confirmed.** All instruments exist and are documented; two traps added: suppressed inits hide in `Duration`; Lambda Insights is an extension that adds INIT work. TTFB is not a Core Web Vital; LCP is. | 9.1–9.4, 10.1 | High |
| 5 | Run startup checks concurrently; existence check over `count(*)` | **Confirmed.** `asyncio.gather`/`TaskGroup`; PostgreSQL `EXISTS` stops at the first row, `count(*)` scans under MVCC. | 5.3 | High (PostgreSQL), Medium (other engines) |
| 6 | Hashed assets `public, max-age=31536000, immutable`; HTML `no-cache` | **Confirmed, minor refinement.** RFC 9111, RFC 8246, MDN and web.dev agree; `public` is needed only where requests carry `Authorization`. A response with no `Cache-Control` is heuristically cacheable. | 6.1, 6.2 | High |
| 7 | ETags and compression at build time; precompressed static serving; Lambda vs S3+CloudFront | **Confirmed.** RFC 9110 makes a strong ETag a function of the encoded bytes (distinct per coding), so build time is the natural place. AWS's reference architecture serves static assets from S3 through CloudFront, Lambda only behind the API; CloudFront compression is best-effort and size-bounded. | 6.3, 6.4 | High (where), Medium (precompress over CloudFront compress) |
| 8 | Route-level splitting and a bundle-size budget | **Confirmed.** web.dev, React `lazy`, size-limit; webpack and Vite *warn* by default, so a budget is enforced only when it fails the build. 170 KB is a suggested start, not a standard. | 7.1, 7.2 | High |
| 9 | Stale-while-revalidate per open view | **Confirmed.** RFC 5861, TanStack Query and SWR defaults. Lambda-specific: default refetch-on-focus multiplies invokes. | 8.1 | High |
| 10 | Keep-warm: pings vs provisioned concurrency vs SnapStart; GovCloud; background ≠ user activity | **Resolved.** AWS recommends provisioned concurrency for interactive apps; calls pings "not a guaranteed way"; SnapStart supports Python 3.12+ in commercial Regions but **"Lambda SnapStart for Python and .NET is not available"** in GovCloud (US). Every environment is recycled "every few hours" regardless. Background-not-activity rests on OWASP's idle-timeout purpose plus interpretation. | 4.1–4.4 | High / Low-Medium (last part) |
| 11 | Package size, dependency closure, lazy imports; layers; images vs zip | **Confirmed for size and dependencies** (three AWS pages). Layers reuse bytes, they do not remove them; no AWS page says layers load faster. Large images "might contribute"; idle image functions go `Inactive` after weeks and reject the first invoke. | 1.1–1.3, 3.2, 3.4 | High / Medium |
| 12 | VPC attachment cost today | **Changed.** Since 2019 Hyperplane ENIs are built at create/update, not per cold start. Residuals: `Pending` for minutes on create; `Inactive` after 14 idle days, first invoke *fails*; NAT or VPC endpoints for outbound calls. AWS (2025) still says "might introduce additional latency", unquantified. | 5.1 | Medium |
| 13 | What the list misses | (a) **Lambda Web Functions** (2026-10-12): multi-request environments, Node.js 24 only, five commercial Regions; (b) suppressed inits; (c) extensions run in INIT; (d) `Inactive` states for idle image and VPC functions; (e) DB connections scale with environments — RDS Proxy or reserved concurrency; (f) provisioned concurrency only applies when the integration invokes the configured alias; (g) GovCloud also lacks Function URLs and JSON logs; (h) 6 MB synchronous payload cap. | 1.1, 3.2, 4.1, 4.2, 5.1, 5.2, 6.4, 6.5 | Medium-High |

### Candidate Principles (the rule's prose half)

1. **Measure, then divide the time.** State the problem as latency on a named path (cold navigation,
   warm navigation, repeat visit); split it into network, INIT, handler phases, transfer and render;
   change nothing that no measurement points at. — Gregg (10.1); AWS `REPORT`/`Init Duration` (9.1);
   web.dev TTFB and Core Web Vitals (9.2, 9.3).
2. **Fix the largest slice first, then re-measure; the constraint moves.** — Goldratt via 10.2; Gregg
   Drill-Down (10.1).
3. **Stop at the target or where the next fix costs more than the delay it saves.** Target: LCP ≤ 2.5 s
   and TTFB ≤ 0.8 s at p75, plus a stated cold-path budget. — web.dev (9.3, 9.2); Reinertsen via 10.2.
4. **Pay setup once per environment, not once per request.** Clients, pools and the app object live in
   module scope; objects used on one rare path load lazily. INIT is billed since 2025-08-01, so this is a
   latency rule, not a free-compute trick. — AWS (1.1, 1.2, 4.1).
5. **Ship less code into INIT.** Package size, dependency count and import cost set INIT time; profile
   imports before choosing what to defer. — AWS (1.1, 1.3); Python `-X importtime` (9.4).
6. **Memory is the CPU dial.** 1,769 MB is one vCPU; Python's GIL caps one thread's use of more; tune by
   measurement (Power Tuning). — AWS (2.1, 2.2); Python (2.3).
7. **Buy warmth deliberately.** Provisioned concurrency is AWS's answer for interactive apps; SnapStart
   where the runtime and partition allow; scheduled pings only as a cheap, unguaranteed fallback. No
   option removes the every-few-hours recycle. — AWS (1.1, 4.1–4.3).
8. **Cap database connections outside the function.** Connections scale with environments; use a proxy
   or reserved concurrency, one connection per environment, validated on use. Cross-reference
   `coding.md` §8. — AWS (5.2).
9. **Serve static assets from the edge, named by content.** Hashed URLs, a year's freshness and
   `immutable`; the HTML shell revalidates; ETags and compression made once at build time. — RFC 9111,
   RFC 8246, RFC 9110, MDN, AWS Serverless Lens (6.1–6.4).
10. **Send the first route's code only, and fail the build past the budget.** — web.dev, React, size-limit,
    webpack (7.1, 7.2).
11. **Show cached data at once and revalidate behind it; a background request is not user activity.** —
    RFC 5861, TanStack, SWR (8.1); OWASP (4.4).

### Candidate always-flag list

Objective defects in code, Terraform/SAM/CloudFormation, build scripts, HTTP response headers or bundle
config. `coding.md` §8 and §15 own pooling and batching in general; rows below add only the Lambda-specific
part.

| # | Defect a reviewer flags | Preferred form | Source | Confidence |
|---|---|---|---|---|
| LWS-1 | An SDK client, DB pool, HTTP client or app/router object constructed inside the Lambda handler on every request, where it serves every request | Construct in module scope (INIT); defer only objects used on rare paths | AWS lifecycle "Optimizing static initialization" (1.1); provisioned-concurrency page: "initializing libraries or instantiating clients within your main handler code means your function must run this each time it's invoked" (4.1) | High |
| LWS-2 | A web-serving function at the 128 MB default (`memory_size` unset or 128) | Size by measurement (Power Tuning); AWS reserves 128 MB for "simple Lambda functions, such as those that transform and route events" | AWS memory page (2.1) | High |
| LWS-3 | Provisioned concurrency configured on an alias or version, while the HTTP integration (API Gateway, ALB, Function URL) invokes the unqualified function or another qualifier | Point the integration at the same alias | AWS provisioned-concurrency page ("ensure that you are invoking the version of alias with provisioned concurrency configured"; not on `$LATEST`) (4.1) | High |
| LWS-4 | SnapStart enabled with a Python or .NET runtime in AWS GovCloud (US); or SnapStart combined with provisioned concurrency, EFS, or ephemeral storage above 512 MB; or on `$LATEST` | Provisioned concurrency or in-code fixes in GovCloud; drop the incompatible option elsewhere | AWS SnapStart page; GovCloud Lambda differences (4.2) | High |
| LWS-5 | With SnapStart on, INIT code that generates unique IDs, secrets or random seeds, or opens a DB/socket connection used without re-validation after restore | Generate uniqueness after restore; validate or reopen connections in an after-restore hook or on use | AWS SnapStart "Compatibility considerations" (4.2) | High |
| LWS-6 | A content-hashed asset served without a long `max-age` and `immutable` | `Cache-Control: max-age=31536000, immutable` (`public` only if requests carry `Authorization`) | RFC 8246; MDN; web.dev (6.1, 6.2) | High |
| LWS-7 | The HTML shell (or any document naming hashed assets) served with a positive `max-age` and no `no-cache`, or with no `Cache-Control` at all | `Cache-Control: no-cache` (validators allow 304) | RFC 9111 §4.2.2, §5.2.2.4; MDN (6.1, 6.2) | High |
| LWS-8 | One strong `ETag` value sent for different content codings (gzip, br, identity) of the same file | A distinct strong ETag per coding, or a weak ETag | RFC 9110 §8.8.3.3 (6.3) | High |
| LWS-9 | A Lambda handler that compresses or hashes a static file on each request | Precompress and compute ETags at build time; store beside the file | RFC 9110 (ETag is a function of the bytes); AWS Lambda billing per ms (1.2); interpretation (6.3) | Medium |
| LWS-10 | Static assets (`/assets/*`, `*.js`, `*.css`, images) routed to a Lambda origin, or a CloudFront behaviour for static paths whose origin is the Lambda/API | S3 (or equivalent object store) behind CloudFront; Lambda only behind the API path | AWS Serverless Applications Lens "Web application"; Lambda 6 MB payload quota (6.4) | Medium-High |
| LWS-11 | A DB pool with more than one connection per Event Function environment, or a connection opened per request with neither RDS Proxy nor `reserved_concurrent_executions` capping connections | Pool size 1 per environment; RDS Proxy for production, or reserved concurrency as a ceiling | AWS RDS page ("proxies are recommended for production"); concurrency page (one request per environment) (5.2); cross-ref `coding.md` §8 | Medium |
| LWS-12 | `SELECT count(*)` whose result is only compared with zero | `EXISTS (...)` or `LIMIT 1` | PostgreSQL docs §9.24.1; PostgreSQL wiki (5.3) | High (PostgreSQL) |
| LWS-13 | Independent startup or per-request I/O awaited sequentially (`await a(); await b()`) where neither needs the other's result | `asyncio.TaskGroup` / `gather`; cross-ref `coding.md` §15 for round-trip count | Python asyncio docs (5.3) | Medium |
| LWS-14 | A production SPA build with no enforced bundle budget: no size-limit (or equivalent) step that fails, webpack `performance.hints` not `"error"`, or Vite `chunkSizeWarningLimit` raised to silence the warning | A failing budget in CI, in a named unit (brotli bytes or minified bytes) | web.dev budgets; size-limit; webpack performance docs ("We recommend using `hints: "error"`"); Vite build options (7.2) | Medium |
| LWS-15 | `lazy()` declared inside a component body, or a `lazy` component with no `<Suspense>` ancestor | Declare at module top level; wrap in `Suspense` with a fallback (the loading state `ux.md` requires) | React `lazy` reference (7.1) | High |
| LWS-16 | A multi-route SPA whose router imports every route component statically | Route-level `lazy`/dynamic `import()` | web.dev code splitting; React `lazy` (7.1) | Medium |
| LWS-17 | `vpc_config` on a function whose code reaches no VPC resource | No VPC attachment | AWS cold-start post ("only use it when access to VPC resources is necessary") (1.3, 5.1) | Medium |
| LWS-18 | A zip that ships `__pycache__` built on a developer machine, or `.pyc` compiled by a Python minor version other than the function's `runtime` | Compile in the runtime's build image (or the matching interpreter), or ship none | AWS Python packaging (3.2); Python tutorial on version-tagged `.pyc` (3.1) | Medium |
| LWS-19 | Development or test dependencies in the production package; a whole SDK imported where one client serves | Production dependency set only; import the client you use | AWS lifecycle ("only import the libraries and dependencies that they need"); cold-start post ("remove unused dependencies") (1.1, 1.3) | Medium |
| LWS-20 | `aws_lambda_function_url` in an AWS GovCloud (US) stack | API Gateway or ALB front door | GovCloud Lambda differences ("AWS Lambda Function URLs is not available") (4.2) | High |

### Candidate advisory list (judgment calls)

- **A scheduled warming ping** — legitimate as a cheap fallback (and against the 14-day `Inactive` state
  of VPC functions), but never documented as a guarantee; flag prose that calls it one (4.3, 5.1).
- **A ping or background refetch that touches the session store** or renews the idle timeout (4.4, 8.1).
- **Data queries left at default `staleTime`** on endpoints that are expensive or cold-start-prone, or
  `refetchIntervalInBackground: true` (8.1).
- **`Server-Timing` with infrastructure detail on unauthenticated responses** (MDN, 9.2).
- **Memory above 1,769 MB on a single-threaded Python function** with no measurement showing it pays
  (2.3).
- **Provisioned concurrency with no scheduled scaling** on an office-hours app (4.1).
- **Comments or docs that justify INIT work as "free"** — stale since 2025-08-01 (1.2).
- **A Node.js web app on an Event Function behind an adapter, in a Web Functions launch Region** — a
  migration candidate (6.5).
- **Lambda Insights left on in production** after the investigation that needed it (9.1).

### Do-not-flag list (common false positives)

- **Lazy initialization inside the handler of a client used on one rare route** — AWS recommends it (1.1,
  4.1).
- **No provisioned concurrency, SnapStart or pings** — a cost choice, not a defect, until a measured cold
  path misses a stated budget.
- **Scheduled pings in a GovCloud Python app** — the platform's cheaper options are unavailable there.
- **A zip without `.pyc` files** — AWS's own recommendation (3.2).
- **Missing `public`** on unauthenticated static assets (MDN, 6.2).
- **No `ETag` on hashed, `immutable` assets** — clients do not revalidate while fresh (RFC 8246).
- **VPC attachment on a function that reaches RDS or ElastiCache** — required; not a per-cold-start cost
  since 2019 (5.1).
- **A pool of exactly one connection per environment**, or no pool at all behind RDS Proxy.
- **A bundle above web.dev's 170 KB example** where the team has set and enforces its own budget.
- **Lambda layers** used to share dependencies across functions — a deployment choice (3.4).
- **Memory above 1,769 MB** where `Max Memory Used` or measured duration justifies it.

### Where sources support an existing rule line (cross-reference, do not restate)

| Existing line | Rule | Sources here |
|---|---|---|
| "The application owns the pool"; "create one long-lived client per remote service and reuse it" | `coding.md` §8 | AWS lifecycle (1.1); AWS RDS and concurrency (5.2) add the Lambda-specific ceiling |
| "Batch every call that crosses the network" | `coding.md` §15 | 5.3 adds concurrency for independent calls and `EXISTS` for per-query cost |
| "Data-driven view with no loading / empty / error state" | `ux.md` | React `Suspense` fallback for `lazy` (7.1) |
| "`useEffect` is for synchronization with external systems" | `react.md` | TanStack Query / SWR as the cache-owning alternative (8.1) |
| Session idle timeout (if present) | `security.md` | OWASP Session Management (4.4) |

## Source Analysis

All accessed 2026-10-26. Vendor documentation counts as official for its own product; it was used for
product behaviour, not for whether a practice is good.

| Source | Domain | Reputation | Type | Verification |
|---|---|---|---|---|
| Lambda Developer Guide (lifecycle, memory, Python packaging, container images, provisioned concurrency, SnapStart, VPC, RDS, concurrency, quotas, Lambda Insights) | docs.aws.amazon.com | High | Official | Read in full or targeted sections |
| AWS GovCloud (US) User Guide, Lambda | docs.aws.amazon.com | High | Official | Read |
| CloudFront "Serve compressed files"; CloudWatch Logs sample queries; Serverless Applications Lens | docs.aws.amazon.com | High | Official | Read |
| AWS Compute/News Blog posts (billing 2025, cold starts 2025, Operating Lambda 2021, VPC 2019, 10 GB 2020, Web Functions 2026) | aws.amazon.com | High | Official (AWS authors) | Read; cold-start 2025 post truncated |
| RFC 9110, 9111, 8246, 5861 | rfc-editor.org | High | Standards | Targeted sections read; RFC 9110 §8.4 not read |
| MDN Cache-Control, Server-Timing | developer.mozilla.org | High | Canonical web reference | Read |
| web.dev (http-cache, code splitting, budgets, TTFB, Vitals, RAIL) | web.dev | High | Google Chrome team | Read; four pages dated 2018–2020 |
| Python docs (threading, tutorial §6.1.3, compileall, import reference, asyncio, cmdline) | docs.python.org | High | Official | Read |
| PostgreSQL 18.6 docs | postgresql.org | High | Official | Read |
| PostgreSQL wiki "Slow Counting" | wiki.postgresql.org | Medium-high | Project wiki | Read; last edited 2021 |
| React `lazy` | react.dev | High | Official | Read |
| Vite, webpack, size-limit, uv, TanStack Query, SWR docs | vite.dev, webpack.js.org, github.com, docs.astral.sh, tanstack.com, swr.vercel.app | High (vendor, own product) | Technical docs | Read |
| OWASP Session Management Cheat Sheet | cheatsheetseries.owasp.org | High | Standards body | Read |
| Brendan Gregg, Methodology | brendangregg.com | Medium-high | Practitioner author | Read |
| Goldratt, Reinertsen | via `ci-pipeline-canonical-sources.md` | Low-medium | Secondary | Not re-read; inherited caveats |
| Third-party guides (oneuptime, Elva/blitzz, lumigo, Pulumi, Classmethod) | various | Medium or lower | Community | Seen in search results only; **not cited as support** |

Reputation: of 52 cited sources, 48 high (≈92%), 2 medium-high, 2 low-medium (Goldratt, Reinertsen,
inherited). Avg ≈ 0.93. **Bias note**: AWS documents services it sells (provisioned concurrency, RDS
Proxy, SnapStart, CloudFront); its pages were used for behaviour and limits, and the cost of each option
is left for the skill to price. AWS sources are one publisher; independence for AWS-behaviour claims
comes from multiple AWS documents agreeing, which is weaker than independent groups. HTTP and front-end
claims are cross-verified across IETF, MDN, Google and vendor docs (independent groups).

## Knowledge Gaps

### Gap 1: INIT CPU allocation
**Issue**: A widely repeated claim says INIT runs with a CPU boost independent of configured memory. |
**Attempted**: AWS lifecycle, memory and billing pages; no AWS statement found. | **Recommendation**:
treat as unconfirmed; measure `Init Duration` across memory sizes with Power Tuning.

### Gap 2: Do timestamp `.pyc` files stay valid in a Lambda zip?
**Issue**: Python validates timestamp `.pyc` by source mtime and size; ZIP stores two-second DOS times
(prior knowledge); how Lambda sets mtimes on extraction is undocumented. A mismatch makes every cold
start recompile silently. `unchecked-hash` is the likely fix, untested. | **Attempted**: Python import
reference, compileall, AWS Python packaging. | **Recommendation**: one experiment — deploy with and
without `compileall --invalidation-mode unchecked-hash` and compare `Init Duration` and `-X importtime`.

### Gap 3: No AWS numbers for VPC, layers, image vs zip, arm64
**Issue**: AWS says each "might" add latency but gives no current deltas. Graviton/arm64 cold-start
behaviour was not researched. | **Recommendation**: the skill measures; the rule should not assert
deltas.

### Gap 4: Background requests and idle timeouts
**Issue**: No source states that background requests must not extend an idle session; OWASP states the
idle timeout's purpose only. NIST SP 800-63B-4's reauthentication text was not read. |
**Recommendation**: read 800-63B-4's session and reauthentication sections before encoding this as more
than advisory.

### Gap 5: Partition and pricing details
SnapStart Python pricing figures; CloudFront feature parity in GovCloud; whether GovCloud SnapStart for
Python is on a roadmap; Web Functions' GovCloud plans. All change; recheck at rule-writing time.

### Gap 6: New Lambda form factors
Lambda Web Functions (two weeks old, Node.js only), Lambda Managed Instances and Lambda MicroVMs were
seen but not researched beyond the launch post and quotas page.

### Gap 7: Unverified tool semantics
Logs Insights `pct()` and `count(field)` behaviour; the composed cold-start query (9.1) is untested.
TanStack's `staleTime` default value was not seen verbatim. Whether `PYTHONPROFILEIMPORTTIME` output
reaches CloudWatch from INIT is untested.

### Gap 8: Front-end items outside the claim list
LCP image optimisation, font loading, `preload`/`modulepreload`, HTTP/2 and HTTP/3 effects on
splitting, and response streaming were not researched; each can move LCP more than the bundle.

### Gap 9: Free-threaded Python on Lambda
Whether any Lambda Python runtime ships a free-threaded (no-GIL) build was not checked; if one does,
claim 2's inference weakens.

### Gap 10: Book texts not read
Goldratt, Reinertsen and Gregg's *Systems Performance* were cited from secondary sources or the author's
site.

## Conflicting Information

### Conflict 1: Ship `.pyc` in the deployment package?
**Position A**: Python — `compileall` makes bytecode "available for use even by users who don't have
write permission"; compiled modules "are platform-independent"; uv compiles bytecode in images "to improve
cold-start performance". **Position B**: AWS — "We recommend that you don't include `__pycache__`
folders" because bytecode from "a different architecture or operating system might not be compatible";
uv's own zip recipe passes `--no-compile-bytecode`. **Assessment**: Python's statement on platform
independence is authoritative for Python; AWS's real risk is a different Python *version*, whose `.pyc`
is ignored by its version tag. Compile with the runtime's own interpreter (image builds do this
naturally), and measure. Medium confidence.

### Conflict 2: Static initialization or lazy loading?
**Position A**: AWS — static init "is also often the best place to open database connections"; move
initialization out of the handler under provisioned concurrency. **Position B**: AWS, same pages — "lazily
load variables in the global scope" for objects "only used in certain execution paths"; defer
`CLIENT_A` into the branch that uses it. **Assessment**: not a contradiction: initialize what every
request uses; defer what few requests use. Under provisioned concurrency INIT is off the request path, so
lean further toward static init.

### Conflict 3: Does VPC attachment still add cold-start latency?
**Position A**: AWS 2019 — the change "dramatically reduces" the latency. **Position B**: AWS 2025 —
VPC "might introduce additional latency". **Assessment**: both hold; the per-cold-start ENI cost is gone,
smaller and situational costs remain (Pending, Inactive, NAT path). Advisory, not always-flag, except for
a VPC that the code never uses (LWS-17).

### Conflict 4: AWS's own RDS sample connects per request
AWS's Python RDS example opens a connection inside `lambda_handler` on every call, while the lifecycle
page recommends reusing a connection from static init. The lifecycle page is the guidance; the sample is
a minimal demonstration. LWS-1 and LWS-11 follow the lifecycle page.

### Conflict 5: Load targets — RAIL and TTI vs Core Web Vitals
web.dev's 2018 budget article and RAIL use "Time to Interactive under 5 s"; web.dev's Vitals page and
RAIL's own page now prefer Core Web Vitals. Use LCP (and TTFB as a diagnostic) for the rule's targets.

## Full Citations

[1] AWS. "Understanding the Lambda execution environment lifecycle". *AWS Lambda Developer Guide*. https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html. Accessed 2026-10-26.
[2] Gupta, S.; Gebhart, J. "AWS Lambda standardizes billing for INIT Phase". AWS Compute Blog. 2025-04-29. https://aws.amazon.com/blogs/compute/aws-lambda-standardizes-billing-for-init-phase/. Accessed 2026-10-26.
[3] Bhattacharya, A.; Wen, T. "Understanding and Remediating Cold Starts: An AWS Lambda Perspective". AWS Compute Blog. 2025-08-07. https://aws.amazon.com/blogs/compute/understanding-and-remediating-cold-starts-an-aws-lambda-perspective/. Accessed 2026-10-26.
[4] AWS. "Configure Lambda function memory". https://docs.aws.amazon.com/lambda/latest/dg/configuration-memory.html. Accessed 2026-10-26.
[5] Poccia, D. "New for AWS Lambda – Functions with Up to 10 GB of Memory and 6 vCPUs". AWS News Blog. 2020-12-01. https://aws.amazon.com/blogs/aws/new-for-aws-lambda-functions-with-up-to-10-gb-of-memory-and-6-vcpus/. Accessed 2026-10-26.
[6] Python Software Foundation. "threading — Thread-based parallelism". https://docs.python.org/3/library/threading.html. Accessed 2026-10-26.
[7] Python Software Foundation. "Modules", §6.1.3 "'Compiled' Python files". *The Python Tutorial*. https://docs.python.org/3/tutorial/modules.html. Accessed 2026-10-26.
[8] Python Software Foundation. "compileall — Byte-compile Python libraries". https://docs.python.org/3/library/compileall.html. Accessed 2026-10-26.
[9] Python Software Foundation. "The import system", §5.4.6 "Cached bytecode invalidation". https://docs.python.org/3/reference/import.html. Accessed 2026-10-26.
[10] AWS. "Working with .zip file archives for Python Lambda functions". https://docs.aws.amazon.com/lambda/latest/dg/python-package.html. Accessed 2026-10-26.
[11] AWS. "Create a Lambda function using a container image". https://docs.aws.amazon.com/lambda/latest/dg/images-create.html. Accessed 2026-10-26.
[12] Astral. "Using uv with AWS Lambda". https://docs.astral.sh/uv/guides/integration/aws-lambda/. Accessed 2026-10-26.
[13] AWS. "Configuring provisioned concurrency for a function". https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html. Accessed 2026-10-26.
[14] AWS. "Improving startup performance with Lambda SnapStart". https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html. Accessed 2026-10-26.
[15] AWS. "AWS Lambda in AWS GovCloud (US)". *AWS GovCloud (US) User Guide*. https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-lambda.html. Accessed 2026-10-26.
[16] Beswick, J. "Operating Lambda: Performance optimization – Part 1". AWS Compute Blog. 2021-04-26. https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/. Accessed 2026-10-26.
[17] OWASP. *Session Management Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html. Accessed 2026-10-26.
[18] Munns, C. "Announcing improved VPC networking for AWS Lambda functions". AWS Compute Blog. 2019-09-03. https://aws.amazon.com/blogs/compute/announcing-improved-vpc-networking-for-aws-lambda-functions/. Accessed 2026-10-26.
[19] AWS. "Giving Lambda functions access to resources in an Amazon VPC". https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html. Accessed 2026-10-26.
[20] AWS. "Using AWS Lambda with Amazon RDS". https://docs.aws.amazon.com/lambda/latest/dg/configuration-database.html. Accessed 2026-10-26.
[21] AWS. "Understanding Lambda function scaling". https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html. Accessed 2026-10-26.
[22] Python Software Foundation. "Coroutines and Tasks". https://docs.python.org/3/library/asyncio-task.html. Accessed 2026-10-26.
[23] PostgreSQL Global Development Group. "9.24. Subquery Expressions" (PostgreSQL 18.6). https://www.postgresql.org/docs/current/functions-subquery.html. Accessed 2026-10-26.
[24] PostgreSQL Wiki. "Slow Counting". Last edited 2021-04-10. https://wiki.postgresql.org/wiki/Slow_Counting. Accessed 2026-10-26.
[25] Fielding, R.; Nottingham, M.; Reschke, J. (eds.). RFC 9111 "HTTP Caching". IETF. June 2022. https://www.rfc-editor.org/rfc/rfc9111.html. Accessed 2026-10-26.
[26] McManus, P. RFC 8246 "HTTP Immutable Responses". IETF. September 2017. https://www.rfc-editor.org/rfc/rfc8246.html. Accessed 2026-10-26.
[27] MDN contributors. "Cache-Control". Last modified 2026-09-17. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control. Accessed 2026-10-26.
[28] Grigorik, I.; Posnick, J. "Prevent unnecessary network requests with the HTTP Cache". web.dev. Updated 2018-11-05. https://web.dev/articles/http-cache. Accessed 2026-10-26.
[29] Fielding, R.; Nottingham, M.; Reschke, J. (eds.). RFC 9110 "HTTP Semantics" (STD 97). IETF. June 2022. https://www.rfc-editor.org/rfc/rfc9110.html. Accessed 2026-10-26.
[30] AWS Well-Architected. "Web application". *Serverless Applications Lens*. https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/web-application.html. Accessed 2026-10-26.
[31] AWS. "Serve compressed files". *Amazon CloudFront Developer Guide*. https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html. Accessed 2026-10-26.
[32] AWS. "Lambda quotas". https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html. Accessed 2026-10-26.
[33] Walter, M. "Announcing AWS Lambda Web Functions for fast, consistent web app performance anywhere". AWS News Blog. 2026-10-12. https://aws.amazon.com/blogs/aws/announcing-aws-lambda-web-functions-for-fast-consistent-web-app-performance-anywhere/. Accessed 2026-10-26.
[34] Djirdeh, H.; Wagner, J. "Reduce JavaScript payloads with code splitting". web.dev. Updated 2018-11-05. https://web.dev/articles/reduce-javascript-payloads-with-code-splitting. Accessed 2026-10-26.
[35] React. "lazy". https://react.dev/reference/react/lazy. Accessed 2026-10-26.
[36] Mihajlija, M. "Performance budgets 101". web.dev. Updated 2018-11-05. https://web.dev/articles/performance-budgets-101. Accessed 2026-10-26.
[37] Sitnik, A. et al. size-limit README. https://github.com/ai/size-limit. Accessed 2026-10-26.
[38] webpack. "Performance". https://webpack.js.org/configuration/performance/. Accessed 2026-10-26.
[39] Vite. "Build Options" (v8.3.4). https://vite.dev/config/build-options. Accessed 2026-10-26.
[40] Nottingham, M. RFC 5861 "HTTP Cache-Control Extensions for Stale Content". IETF, Informational. May 2010. https://www.rfc-editor.org/rfc/rfc5861.html. Accessed 2026-10-26.
[41] TanStack. "Important Defaults". TanStack Query (React). https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults. Accessed 2026-10-26.
[42] Vercel. "Getting Started". SWR. https://swr.vercel.app/docs/getting-started. Accessed 2026-10-26.
[43] AWS. "Sample queries". *Amazon CloudWatch Logs User Guide*. https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-examples.html. Accessed 2026-10-26.
[44] AWS. "Monitor function performance with Amazon CloudWatch Lambda Insights". https://docs.aws.amazon.com/lambda/latest/dg/monitoring-insights.html. Accessed 2026-10-26.
[45] Pollard, B.; Wagner, J. "Time to First Byte (TTFB)". web.dev. Updated 2025-11. https://web.dev/articles/ttfb. Accessed 2026-10-26.
[46] MDN contributors. "Server-Timing". Last modified 2026-07-28. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Server-Timing. Accessed 2026-10-26.
[47] web.dev. "Web Vitals". Updated 2024-10-31. https://web.dev/articles/vitals. Accessed 2026-10-26.
[48] web.dev. "Measure performance with the RAIL model". Updated 2020-06-10. https://web.dev/articles/rail. Accessed 2026-10-26.
[49] Python Software Foundation. "Command line and environment". https://docs.python.org/3/using/cmdline.html. Accessed 2026-10-26.
[50] Gregg, B. "Performance Analysis Methodology". Updated 2025-01-23. https://www.brendangregg.com/methodology.html. Accessed 2026-10-26.
[51] Goldratt, E.M.; Cox, J. *The Goal*. North River Press. 1984. Via `docs/research/ci/ci-pipeline-canonical-sources.md` [45] (secondary).
[52] Reinertsen, D.G. *The Principles of Product Development Flow*. Celeritas. 2009. Via `docs/research/ci/ci-pipeline-canonical-sources.md` [46] (secondary).

Seen via search results only, not cited as support: AWS What's New, "AWS Lambda now supports up to 10 GB
of memory and 6 vCPU cores in AWS GovCloud (US) Regions" (2021-08); AWS What's New, SnapStart for Java in
AWS GovCloud (US) (2024-09, German and French mirrors).

## Research Metadata

Examined: ~60 pages | Cited: 52 | Confidence by finding: High ≈ 60%, Medium ≈ 30%, Low ≈ 10%
(Goldratt/Reinertsen quotations, background-activity principle, `.pyc` mtime question) |
Tool notes: the 2025 cold-start blog post was truncated in retrieval; `swr.vercel.app/` redirected
(getting-started page read instead); RFC 9110 read by offset (§8.8 and §13 found, §8.4 not); the
operator-guide URL redirected to the Developer Guide lifecycle page; no fetched page carried
agent-directed instructions |
Output: docs/research/web-speed/lambda-web-app-speed-canonical-sources.md
