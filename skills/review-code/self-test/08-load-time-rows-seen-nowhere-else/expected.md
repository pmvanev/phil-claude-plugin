# Expected outcome — fixture 08 (load-time rows seen nowhere else)

A ledger app on AWS Lambda in `us-gov-west-1`: an API function configured for SnapStart, behind a
Function URL on its `live` alias (`app.py`); a function that serves the single-page shell from a template
in its code, its assets from `dist/` and a health check (`web.py`, `paths.py`); their Terraform; and the
build script. It holds the six Always-flag rows of
`rules/lambda-web-app-speed.md` that fixture 07 plants nothing for, beside two look-alikes the rule
clears. `test_paths.py` is green.

**Pins:** each of LWS-5, LWS-7, LWS-8, LWS-9, LWS-10 and LWS-13 is found where it is planted and named by
its id, with the row's Preferred form as the fix — so every Always-flag row now has a fixture a review
must pass.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this directory
(`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the six items in `expected-backlog.md`, each matched on
the Smell and on a Refactoring that is the row's Preferred form verbatim, alone or followed by
` — here: ` and this code's one change. Order is not checked.

1. **LWS-5** — `build.sh` compiles with Python 3.11 for functions declaring `python3.12`.
2. **LWS-8** — SnapStart on a Python function in GovCloud, which offers none.
3. **LWS-10** — a Function URL in GovCloud, which offers none.
4. **LWS-7** — provisioned concurrency on the `live` alias, while the integration invokes the function
   unqualified.
5. **LWS-9** — `INSTANCE_ID` generated at INIT, so every restored environment shares one.
6. **LWS-13** — `SHELL_HTML`, 2.2 KiB, leaves with no `Content-Encoding`. Its size is in `web.py`, which
   the review reads; the assets' sizes sit in `dist/`, which the review skips.

LWS-8 and LWS-9 are two items: the code could drop SnapStart and keep the id at INIT, or move the id to
first use and keep SnapStart.

**Hard assertions (any failure blocks the skill change):**

- **No load-time item files a look-alike as its defect:**
  - `assets_route` — static assets routed to the function in GovCloud, where CloudFront is unavailable:
    LWS-16 stays silent.
  - `HEALTH_BODY` — a reply far under 1.4 KiB sent uncompressed.
  - `LEDGER` — a boto3 client built at INIT under SnapStart; it opens no connection, so LWS-9's
    connection clause stays silent.
- **No item asks for SnapStart or provisioned concurrency** where the code has none; both items above
  fault a configuration that exists.
- Every load-time item carries `Priority: 1` and `Route: report only`, names its `LWS-n` id in the
  Smell field, and is counted on the Summary's load-time line.

**Not a failure:** Advisory questions where a file shows their subject, and questions on a row whose
fact the files leave unsettled — LWS-13 on the S3 object `app.py` returns and on the assets in `dist/`,
LWS-17 on the build behind `dist/`; security items, since the fixture is not hardened (a request path read straight into an S3
key, an unhashed `requirements.txt`); items about error handling, structure, naming or tests; line
numbers within ±2.

**Driven 2026-10-26**, before the shell moved into `web.py`, against this working tree's `SKILL.md` by a
fresh agent that read only the fixture, the rules and the skill: all six items, neither look-alike. It
read `dist/` for the shell's size, which the gather skips; the shell moved into the code so a review
that keeps to the gather can file LWS-13. `tests/test_lambda_web_app_speed_rule.py` fails without this
fixture, naming the six rows it plants.

**Driven again 2026-10-26**, after the shell moved, by a fresh agent held to the gather: it read `dist/`
not at all, and filed all six items with their rows' Preferred forms, neither look-alike, and LWS-13 on
the assets and on the S3 body, and LWS-17, as questions naming the unread source — as the rule asks.
