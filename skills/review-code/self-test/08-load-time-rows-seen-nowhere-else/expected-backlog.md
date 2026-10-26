# Refactoring Backlog — load-time items expected

Scope: .

## Backlog

### [R001] LWS-5 — bytecode compiled by Python 3.11 for functions that run Python 3.12

- **File**: `build.sh`
- **Lines**: 9
- **Priority**: 1
- **Smell**: LWS-5
- **Refactoring**: Compile in the build with the runtime's own Python version, or ship no `.pyc` — here: compile with `python3.12 -m compileall`, the runtime both functions declare
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS Python `.zip` packaging docs; Python tutorial §6.1.3
- **Status**: pending

### [R002] LWS-8 — SnapStart on a Python function in AWS GovCloud (US)

- **File**: `main.tf`
- **Lines**: 15-17
- **Priority**: 1
- **Smell**: LWS-8
- **Refactoring**: Drop the incompatible option; in GovCloud, keep warm another way or not at all — here: remove the `snap_start` block from `aws_lambda_function.api`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS SnapStart docs; AWS GovCloud (US) User Guide, Lambda, read 2026-10-26
- **Status**: pending

### [R003] LWS-10 — a Lambda Function URL in an AWS GovCloud (US) stack

- **File**: `main.tf`
- **Lines**: 26-30
- **Priority**: 1
- **Smell**: LWS-10
- **Refactoring**: API Gateway or an Application Load Balancer — here: route the API through `aws_apigatewayv2_api.ledger` and remove `aws_lambda_function_url.api`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS GovCloud (US) User Guide, Lambda, read 2026-10-26
- **Status**: pending

### [R004] LWS-7 — provisioned concurrency on the `live` alias, while the integration invokes the unqualified function

- **File**: `main.tf`
- **Lines**: 63
- **Priority**: 1
- **Smell**: LWS-7
- **Refactoring**: Point the integration at the alias that holds the provisioned concurrency — here: set `integration_uri` to `aws_lambda_alias.web_live.invoke_arn`
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS provisioned concurrency docs
- **Status**: pending

### [R005] LWS-9 — a unique id generated at INIT in a function SnapStart restores

- **File**: `app.py`
- **Lines**: 7
- **Priority**: 1
- **Smell**: LWS-9
- **Refactoring**: Generate unique values after restore; revalidate or reopen connections in an after-restore hook or on first use — here: generate `INSTANCE_ID` on first use, or in an after-restore hook, so each restored environment gets its own
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — AWS SnapStart, "Compatibility considerations"
- **Status**: pending

### [R006] LWS-13 — the 2.2 KiB HTML shell sent with no `Content-Encoding`

- **File**: `web.py`
- **Lines**: 49-54
- **Priority**: 1
- **Smell**: LWS-13
- **Refactoring**: Precompress static files at build time and compress dynamic text in the server, serving `br` or `gzip` with `Vary: Accept-Encoding`; behind CloudFront, store precompressed objects or set `compress = true` — here: gzip `SHELL_HTML` once at module scope, and return it base64-encoded (`isBase64Encoded: true`) with `Content-Encoding: gzip` and `Vary: Accept-Encoding` when the request accepts gzip
- **Route**: report only
- **Rationale**: lambda-web-app-speed.md — Chrome Lighthouse, "Enable text compression"; RFC 9110 §8.4; CloudFront, "Serve compressed files"
- **Status**: pending
