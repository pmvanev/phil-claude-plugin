# Expected outcome — fixture 01 (all-checkable intent → off-ramp) · WALKING SKELETON

Every expectation in this intent is something an nwave acceptance test can assert directly
(stdout content, filesystem unchanged, exit code). The engine's own oracle already satisfies EDD's
criteria for these; there is no qualitative residue.

**Pins:** slice-01, AC1.1, KPI zero-ceremony — *"When every expectation is engine-checkable, phil:edd
recommends the engine and exits, adding no ceremony."* This is the single **walking-skeleton**
scenario: the front-door end-to-end (capture → classify → recommend → exit).

**Expected decision:** `OFF-RAMP`. The tool shows a classification table (each expectation → the
engine + its native oracle), recommends running that engine directly (naming the command, e.g.
`/nw-...` for user-facing behaviour), and **exits** — it commissions no evidence, creates no
`agents/edd-evidence-producer` run, and opens **no** `docs/edd/<slug>/` trail.

**Gate failure (blocks the skill change):** the tool commissions evidence, builds a gate, or opens a
`docs/edd/<slug>/` trail for an intent whose expectations are all engine-checkable. That is exactly
the ceremony EDD is supposed to avoid; if it fires here, phil:edd becomes the bureaucratic overhead
the article warns EDD can degenerate into, and Avery stops reaching for it. (Observable as a
filesystem fact: any trail file created here = fail.)
