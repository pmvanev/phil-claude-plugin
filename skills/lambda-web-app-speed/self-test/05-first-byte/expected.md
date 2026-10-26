# Expected outcome — fixture 05 (first byte)

One real GET of a production page's landing route on 2026-10-26, its client timings rounded as `curl`
reported them, and the one `REPORT` the function logged for it, renamed. The function had been idle, so
the request met a cold start.

**Expected**, pinned by `tests/test_lambda_first_byte.py`: first byte 4.21 s, split into the network —
DNS 61 ms, TCP 56 ms, TLS 150 ms, 0.27 s in all — the function, INIT 3.31 s and the invoke 0.02 s, 3.33 s
in all, and the front door and placement, the 0.62 s neither the client nor the `REPORT` times.

The split also holds where the `REPORT` is stamped before the GET began: a later warm load of the same
page was stamped 285 ms early, since the client's clock and AWS's differ.
