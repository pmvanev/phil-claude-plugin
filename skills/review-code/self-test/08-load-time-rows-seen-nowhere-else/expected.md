# Expected outcome — fixture 08 (load-time rows seen nowhere else)

A ledger app on AWS Lambda in `us-gov-west-1`: an API function behind a Function URL, restored by
SnapStart (`app.py`); a function that serves the single-page shell, its assets and a health check
(`web.py`, `paths.py`); their Terraform; and the build script. It holds the six Always-flag rows of
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
6. **LWS-13** — `index.html` (2.2 KB) and the script (2.6 KB) leave with no `Content-Encoding`.

**Hard assertions (any failure blocks the skill change):**

- **No load-time item files a look-alike as its defect:**
  - `assets_route` — static assets routed to the function in GovCloud, where CloudFront is unavailable:
    LWS-16 stays silent.
  - `HEALTH_BODY` — a reply far under 1.4 KiB sent uncompressed.
- **No item asks for SnapStart or provisioned concurrency** where the code has none; both items above
  fault a configuration that exists.
- Every load-time item carries `Priority: 1` and `Route: report only`, names its `LWS-n` id in the
  Smell field, and is counted on the Summary's load-time line.

**Not a failure:** Advisory questions where a file shows their subject; security items, since the
fixture is not hardened (an IAM-authorised Function URL, a `requirements.txt` that hashes one package);
items about structure, naming or tests; line numbers within ±2.
