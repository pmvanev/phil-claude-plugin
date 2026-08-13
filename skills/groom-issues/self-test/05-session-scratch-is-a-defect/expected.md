# Expected outcome — fixture 05 (session state does not belong on a board)

The body carries a working note: where the last session stopped, at which commit, and what is next.

**Expected decision:** `REPORT-DEFECT`, classified **semantic** — removing someone's note is not a
call this tool makes unasked.

Cite the rule: session state belongs in the git-ignored local surface (ADR-013), because a board is
world-readable and this content is in-flight scratch rather than a description of the work.

**Gate failure:** passing over it because it is plausible-looking prose in a body, which is exactly
what it is. The defect is not that the text is malformed — it is that it is *misplaced state*, and a
grooming pass that only checks shape will never see it.

Classifying it mechanical is also a failure: deleting it unasked destroys the only copy of something
the author may still want.
