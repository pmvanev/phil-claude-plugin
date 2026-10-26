# Refactoring Backlog — load-time items expected

Scope: .

## Backlog

### [R001] LWS-17 — the production build runs with no size budget that fails it

- **File**: `.github/workflows/ci.yml`
- **Lines**: 20
- **Priority**: 1
- **Smell**: LWS-17
- **Refactoring**: A budget that fails the CI build: a `size-limit` step, or webpack `performance.hints: "error"` — here: add a `size-limit` step after `npm run build`, and drop `chunkSizeWarningLimit: 4000` from `vite.config.ts`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — web.dev performance budgets; size-limit; webpack and Vite build docs
- **Status**: pending

### [R002] LWS-4 — startup check counts every report to test for none

- **File**: `handler.py`
- **Lines**: 20-21
- **Priority**: 1
- **Smell**: LWS-4
- **Refactoring**: `EXISTS (…)`, or `LIMIT 1` — here: `SELECT EXISTS (SELECT 1 FROM reports)` in `_check_database`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — PostgreSQL docs §9.24.1
- **Status**: pending

### [R003] LWS-3 — three startup checks run one after another

- **File**: `handler.py`
- **Lines**: 29-31
- **Priority**: 1
- **Smell**: LWS-3
- **Refactoring**: Run them concurrently — a `ThreadPoolExecutor`, with every boto3 client built before the threads start, or an `asyncio.TaskGroup` in async code — and batch the calls to one service (`coding.md` §15) — here: run `_check_bucket`, `_check_database` and `_check_user_pool` concurrently, building the Cognito client before the threads start
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — Python `concurrent.futures` and `asyncio` docs; boto3 guide, "Clients", on multithreading
- **Status**: pending

### [R004] LWS-1 — Cognito client built on every request

- **File**: `handler.py`
- **Lines**: 41
- **Priority**: 1
- **Smell**: LWS-1
- **Refactoring**: Build it at module scope, so INIT builds it once per environment; build lazily only what a rare path uses — here: build the Cognito client once at module scope; every request calls `get_user`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS Lambda lifecycle, "Optimizing static initialization"; AWS provisioned concurrency docs
- **Status**: pending

### [R005] LWS-2 — the shell function runs at the 128 MB default

- **File**: `main.tf`
- **Lines**: 19-25
- **Priority**: 1
- **Smell**: LWS-2
- **Refactoring**: Size memory by measurement; at 1,769 MB a function has the equivalent of one vCPU — here: set `memory_size` on `aws_lambda_function.shell` from a measurement
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS "Configure Lambda function memory"
- **Status**: pending

### [R006] LWS-16 — assets routed to a Lambda in a commercial Region

- **File**: `main.tf`
- **Lines**: 55-59
- **Priority**: 1
- **Smell**: LWS-16
- **Refactoring**: S3 behind CloudFront, with Lambda behind the API path only — here: serve `/assets/*` and the shell from S3 behind CloudFront, leaving Lambda behind `/api` only
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS Serverless Applications Lens, web application; Lambda 6 MB payload quota
- **Status**: pending

### [R007] LWS-6 — pytest installed into every production zip

- **File**: `requirements.txt`
- **Lines**: 4
- **Priority**: 1
- **Smell**: LWS-6
- **Refactoring**: Install the production dependency set and copy the production modules only — here: move `pytest` to a dev requirements file the zip never installs
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS Lambda lifecycle; AWS, "Understanding and Remediating Cold Starts" (2025)
- **Status**: pending

### [R008] LWS-18 — lazy() called inside the Admin component

- **File**: `src/Admin.tsx`
- **Lines**: 4
- **Priority**: 1
- **Smell**: LWS-18
- **Refactoring**: Call `lazy` at module top level, and wrap the component in `<Suspense>` with a fallback — here: move `const UsageChart = lazy(...)` to module top level
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — React `lazy` reference
- **Status**: pending

### [R009] LWS-19 — the router imports all four pages statically

- **File**: `src/routes.tsx`
- **Lines**: 3-6
- **Priority**: 1
- **Smell**: LWS-19
- **Refactoring**: Load every view but the landing one with `lazy` and a dynamic `import()`, under a `<Suspense>` with a fallback — here: load `Reports`, `Settings` and `Admin` with `lazy` and `import()`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — web.dev code splitting; React `lazy` reference
- **Status**: pending

### [R010] LWS-14 — one strong ETag for the gzip and identity bodies

- **File**: `web_shell.py`
- **Lines**: 17-18
- **Priority**: 1
- **Smell**: LWS-14
- **Refactoring**: A distinct strong `ETag` per coding, or a weak `ETag` — here: send the ETag weak, or hash the gzipped bytes for the gzip body
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — RFC 9110 §8.8.3
- **Status**: pending

### [R011] LWS-15 — the shell hashes each file on every request

- **File**: `web_shell.py`
- **Lines**: 17
- **Priority**: 1
- **Smell**: LWS-15
- **Refactoring**: Precompress and compute `ETag`s at build time, and serve the stored results — here: compute each file's ETag at build time and serve it from a manifest
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — RFC 9110 §8.8.3; AWS Lambda billing per millisecond
- **Status**: pending

### [R012] LWS-12 — HTML shell cached for ten minutes

- **File**: `web_shell.py`
- **Lines**: 20
- **Priority**: 1
- **Smell**: LWS-12
- **Refactoring**: `Cache-Control: no-cache` — here: send `no-cache` for `index.html`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — RFC 9111 §4.2.2, §5.2.2.4; MDN `Cache-Control`
- **Status**: pending

### [R013] LWS-11 — hashed assets cached for an hour

- **File**: `web_shell.py`
- **Lines**: 22
- **Priority**: 1
- **Smell**: LWS-11
- **Refactoring**: `Cache-Control: max-age=31536000, immutable`; add `public` only where requests carry `Authorization` — here: send `max-age=31536000, immutable` for `assets/`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — RFC 8246; MDN `Cache-Control`; web.dev HTTP cache
- **Status**: pending

### [R014] LWS-15 — the shell gzips each file on every request

- **File**: `web_shell.py`
- **Lines**: 23-25
- **Priority**: 1
- **Smell**: LWS-15
- **Refactoring**: Precompress and compute `ETag`s at build time, and serve the stored results — here: write each file's `.gz` into `dist/` at build time and serve it
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — RFC 9110 §8.8.3; AWS Lambda billing per millisecond
- **Status**: pending
