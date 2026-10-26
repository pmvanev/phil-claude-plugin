# Expected outcome — fixture 04 (warmth prices)

`prices-us-gov-west-1.json` is AWS's public Lambda price list for us-gov-west-1, whole;
`prices-us-east-1.json` keeps the six prices `warmth.py` reads from us-east-1's. Both were published
2026-10-22 and fetched 2026-10-26. `traffic-14d.json` is what `cold-path.py --json` reported for one web
API's fourteen days: 7,876 invokes, 105 cold starts, 40 active hours, a peak of four environments in a
minute, and 933.9 s of invoke time.

**Expected**, for 1,769 MB and `python3.12`, scaled from fourteen days to a 730-hour month (×2.1726),
every figure pinned by `tests/test_lambda_warmth.py` from AWS's pricing page, read 2026-10-26:

- us-gov-west-1, provisioned concurrency, one environment: 1.7275 GB × 2,628,000 s × $0.0000052729,
  less the invoke time's change from on-demand to provisioned duration: $23.92 a month, at least $0.10
  for each cold start it removes (228 a month in all).
- The peak of four environments: $95.74.
- SnapStart: not available for Python or .NET in AWS GovCloud (US), and the price list holds no
  SnapStart price there.
- A heartbeat, one request a minute held 50 ms during the 87 active hours a month: $0.0085.
- us-east-1, SnapStart: the cache, 1.7275 GB × 2,628,000 s × $0.0000015046, plus 228 restores ×
  1.7275 GB × $0.0001397998: about $6.89. For `java21`, in either Region: available, and no charge.
- An `arm64` function reads the `-ARM` prices: provisioned concurrency $0.0000033334 a GB-second in
  us-gov-west-1, against $0.0000052729.

The free tier is ignored, and every price is the first tier's.
