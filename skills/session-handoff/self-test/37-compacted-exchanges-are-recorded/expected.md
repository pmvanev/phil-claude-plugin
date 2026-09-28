# Expected — 37 (a compacted exchange is copied, not rebuilt)

**Expected decision:** `CAPTURE`.

## What must be in `.session-handoff.md`

Inside the markers: the compacted exchange **word for word**, then the intact one, then the handoff's
own — all three copied by `record` from the transcript, which keeps every record across a compaction.
None of the summary's words.

## What must be in the report

The counting line says three exchanges will be recorded. There is no compacted count: nothing was lost.

## Why this changed

Until 2026-09-28 a compacted exchange was counted and left out, because the session held only the
summary and could not honestly reproduce what was said. That reason belonged to a session doing the
copying. The script reads the transcript instead, where the words survive, so the exchange is recorded
like any other — and the summary is still never what was said.

## Gate failures

- **Recording the summary, or rebuilding the exchange from it.** A summary is this session's paraphrase;
  filed between the markers it would be read later as what was said.
- **Leaving it out because this session cannot see it.** The record is the transcript, not the context.
