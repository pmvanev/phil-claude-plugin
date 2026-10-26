# Expected outcome — fixture 07 (load-time findings cite an LWS row)

A small reports web app served from AWS Lambda in `us-east-1`: an API function (`handler.py`), a
function that serves the single-page app's shell and assets (`web_shell.py`), an S3-triggered
thumbnailer, their Terraform, the build script, a CI workflow, and a Vite and React front end. It holds
fourteen load-time defects, each on a line an Always-flag row of `rules/lambda-web-app-speed.md`
describes, beside six look-alikes that a row's own scope or the Do-not-flag list clears.
`test_routing.py` is green.

**Pins:** `review-code` reads the load-time rule in a repository that deploys to Lambda, applies it to
every gathered file — the build, dependency and CI files included — names each finding by the row's
`LWS-n` id, and takes the row's Preferred form as its fix. Before the rule existed, no rule or skill in
the plugin named any of these defects.

**How to drive it:** drive this working tree's `skills/review-code/SKILL.md` by hand over this
directory (`/phil:review-code` runs the released copy).

**Expected:** a `.refactoring-backlog.md` holding the fourteen items in `expected-backlog.md`, matched
on the Smell and on a Refactoring that is the row's Preferred form verbatim, alone or followed by
` — here: ` and this code's one change. Order is not checked.

1. **LWS-17** — CI builds the production bundle and no size budget fails it; Vite's raised
   `chunkSizeWarningLimit` is the evidence.
2. **LWS-4** — `_check_database` counts every report to learn whether there are none.
3. **LWS-3** — the three startup checks run one after another at INIT.
4. **LWS-1** — `handler` builds a Cognito client on every request, and every request uses it.
5. **LWS-2** — the shell function leaves `memory_size` at the 128 MB default.
6. **LWS-16** — `/assets/*` routes to a Lambda in a commercial Region, where CloudFront exists.
7. **LWS-6** — `requirements.txt` installs `pytest` into every production zip.
8. **LWS-18** — `Admin` calls `lazy()` inside its body.
9. **LWS-19** — the router imports all four pages statically.
10. **LWS-14** — the strong ETag hashes the identity bytes and goes out with the gzip body too.
11. **LWS-15** — `serve` hashes the file on every request.
12. **LWS-12** — the HTML shell goes out with `max-age=600` and no `no-cache`.
13. **LWS-11** — hashed assets go out with `max-age=3600` and no `immutable`.
14. **LWS-15** — `serve` gzips the file on every request: a second missing protection under the same row.

**Hard assertions (any failure blocks the skill change):**

- **No load-time item files a look-alike as its defect:**
  - `textract` — a client built in the handler on the export path alone, which AWS recommends.
  - `report_count` — a `count(*)` whose number the API returns.
  - `S3_CLIENT` — a client already built at module scope.
  - `reports-thumbnailer` — `memory_size` unset on a function an S3 event starts, which no person waits on.
  - `--no-compile` in `build.sh` — a zip with no `.pyc`, which AWS recommends.
  - `SettingsHelp` — `lazy` at module top level, under a `<Suspense>`.
- **No item asks for provisioned concurrency, SnapStart or a warming ping**, and none flags the API
  function's VPC attachment. Both are on the Do-not-flag list.
- **The Cognito client is one LWS-1 item**, never also a `coding.md` §8 item.
- **LWS-15 is two items**, one per missing protection; the ETag shared across codings is LWS-14 and a
  third item.
- Every load-time item carries `Priority: 1` and `Route: report only`, names its `LWS-n` id in the
  Smell field, and is counted on the Summary's load-time line, not under Priority 1 (Correctness).

**Not a failure:** security items, since the fixture is not hardened beyond the path join (an unhashed
`pip install`, an unchecked export location); a `coding.md` §8 item on the module-scope
`psycopg.connect`, which is one connection rather than a pool; items about error handling, structure,
naming or tests; line numbers within ±2.

**Driven 2026-10-26** against this working tree's `SKILL.md` before the backtest revisions, by a fresh
agent that read only the fixture, the rules and the skill: all fourteen items then expected, no
look-alike, with LWS-15 filed twice — now expected — and a CWE-22 item on a path join since guarded.
