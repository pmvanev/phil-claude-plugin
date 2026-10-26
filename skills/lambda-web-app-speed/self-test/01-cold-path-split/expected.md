# Expected outcome — fixture 01 (cold path split)

`events.json` holds 31 platform lines that the AWS CLI's `filter-log-events` returned on 2026-10-26 for
one function's web API, trimmed to six of its log streams and renamed `reports-api`. Every line is
real; the trimming kept each stream's order.

| Stream | Lines kept | What happened |
|---|---|---|
| `2026/10/21/…a8d02d90…` | 9 `REPORT` | a cold start (INIT 1.15 s, first invoke 4.87 s); three warm invokes; a warm invoke that timed out at 29 s; a suppressed init that also timed out; a suppressed init of 5.24 s; two warm invokes |
| `2026/10/24/…733dd363…` | `INIT_REPORT` + 6 `REPORT` | INIT timed out at 10 s; the first invoke held the retried INIT (2.00 s); five warm |
| `2026/10/24/…e03e44d2…` | `INIT_REPORT` + 4 `REPORT` | INIT timed out at 10 s; the first invoke held the retried INIT (1.72 s); three warm |
| `2026/10/24/…b6bdbe01…` | 4 `REPORT` | a cold start (INIT 8.07 s, first invoke 0.13 s); three warm |
| `2026/10/24/…2baedb94…` | 2 `REPORT` | a cold start (INIT 8.94 s, first invoke 0.13 s); one warm |
| `2026/10/24/…1f5a9fd5…` | 4 `REPORT` | a cold start (INIT 2.20 s, first invoke 0.11 s); three warm |

**Expected**, pinned by `tests/test_lambda_cold_path.py`:

- 29 invokes; 8 cold starts: 4 with `Init Duration`, 2 after a failed INIT, 2 suppressed inits.
- 2 failed INITs, both timeouts; 2 failed invokes; 21 warm invokes.
- Look inside INIT, because INIT reached its 10 s ceiling 2 times.
- INIT p50 2.20 s and p95 8.94 s, nearest rank over 1152.56, 2199.98, 8066.70 and 8936.06 ms.
- First invoke p50 0.13 s and p95 4.87 s, over 111.51, 127.53, 134.62 and 4874.40 ms.
- INIT owns the cold path: 40.36 s — the four recorded INITs and the two 10 s timeouts — against the
  first invokes' 5.25 s. The 37.96 s of the four unsplit cold starts counts to neither.
- The memory change from 1024 MB to 1769 MB is named.

**The two hard assertions.** No unsplit cold start may count as warm: the suppressed init that timed
out would put 29 s among the warm invokes as a slow request, and hide a cold start. And the owner comes
from recorded splits alone.
