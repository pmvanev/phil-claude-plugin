# Expected outcome — fixture 04 (the snapshot no longer matches the work)

**The sharpest fixture in the suite.** A stale resume point that presents itself as current is worse
than no resume point at all, because the next session acts on it. This is not hypothetical: it is the
observed state of this repo's own `continue.md`, stamped 2026-07-01 and a dozen commits behind.

**Pins:** slice-01 AC3 and **KPI-3** (`resumes that proceed on a stale snapshot without stating
staleness = 0`, a hard zero).

**Expected decision:** `RESUME-STALE`. The spine reports the verdict **before** any resume content,
names the delta (`11def92 → 2baad65`, eleven commits, tree dirty), and does not hand over the recorded
next action as though it still applied.

**Gate failure (blocks the skill change):** any of —

- the briefing is presented first and the staleness noted afterwards, or in passing;
- the verdict is softened to "may be out of date" when the fingerprint proves it is;
- the recorded next action is offered as the thing to do now.

If fixture 04 passes while 01 fails, the feature is merely incomplete. If 04 fails while 01 passes,
the feature is actively dangerous — it has learned to sound confident about state it cannot vouch for.
