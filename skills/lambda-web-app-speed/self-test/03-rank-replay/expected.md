# Expected outcome — fixture 03 (ranking replay)

Two candidate files replay beatrix's cold `GET /` from its issue 254, each figure from a measurement
taken before the fix it describes, each cited by the issue note that recorded it. The real gains, by
size: building during INIT, with smaller changes alongside, cut first byte 5.3 s (13.40 → 8.14 s,
note 14438); concurrent startup checks with Bedrock moved to first chat took 2.3–2.4 s off INIT (5.13–5.42
→ 2.83–3.04 s, note 14650); memory from 512 to 1769 MB 1.2–1.5 s (note 14438); compiled bytecode
0.69–0.86 s off imports (1.53–1.91 → 0.84–1.05 s, note 14498).

Both files follow Step 5's definitions: `now_ms` is the cold wait, INIT plus the first invoke, at the
middle of its recorded range; `noise_ms` is the spread of the repeated cold starts behind it; and
`target_ms` is `null`, since beatrix stated no cold-path budget.

**`before-init-move.json`** — at 512 MB, INIT 2.28–3.05 s and the first invoke 8.45–9.47 s over five cold
starts, with no timing line yet, so Step 4 would propose one and Step 5 would rank nothing. **Expected:**
nothing ranked; memory then the INIT move listed as experiments, cheapest first. Both changed the machine,
and both made the largest gains.

**`after-memory.json`** — at 1769 MB, after the INIT move, with the per-phase line (note 14480) and the
per-call timings (note 14518). **Expected:** the checks (2.13–2.47 s, from Bedrock's 1.20–1.25 s plus
canaries summing 1.21–1.32 s with the slowest at 0.10–0.285 s) ranked above bytecode (0.74–1.02 s, from
imports of 1.53–1.91 s scaled by the person's local measurement, note 14494); more memory an
experiment; the module trim and the Secrets Manager read inside the 0.32 s noise; and no stopping line.

**The pass test (D17).** Where the measurement divides the time, the largest real gain ranks first:
2.3 s above 0.7 s. Bytecode's real gain, 0.69–0.86 s, sits at the bottom of its estimate. Where a fix
changes the machine, the ranking claims nothing and lists it to try.

**What this does not show.** The replay is after the fact — D17 was chosen knowing this record — and
ranks only two fixes, so no near-tie or standard tie-break is exercised on real figures. A held-out case
waits for a project that measures before it fixes.
