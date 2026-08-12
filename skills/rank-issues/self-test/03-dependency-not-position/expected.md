# Expected outcome — fixture 03 (a dependency is not an ordering)

"5 is pointless until 8 lands" is not a preference. Position can express that 8 sits above 5; it
cannot express that 5 **cannot start** until 8 is done. Those are different claims.

**Expected decision:** `WRITE-DEPENDENCY` — all three of:

1. the order (8 above 5),
2. the forge's own link (`gh issue edit 5 --add-blocked-by 8`),
3. a `## Chain` line on **both** issues carrying the reason.

**Gate failure:** encoding it as position alone. The board then looks correctly ranked, and the reason
is gone — the next person sees 8 above 5, reads it as taste, and reorders freely. That is the failure
mode this whole repo keeps rediscovering: the *why* dies in the transcript.

Recording the link without the prose reason is also a failure. The forge writes the edge; only the
`## Chain` line says *why you stopped*, and six issues later the edge alone does not tell you.
