# Expected outcome — fixture 01 (walking skeleton: the table, from agreeing sources)

Every source agrees, so this is the thinnest end-to-end proof: resolve the slice → read the
artifacts → render → stop.

**Expected decision:** `STATUS-TABLE`.

The output carries, in order:

1. An intent line taking its goal from `slices/slice-03-triage-feed.md` — the `**Goal.**` sentence,
   not the phase name, because the slice file is present.
2. A table with one row per step: `03-01` and `03-02` `done`, `03-03` `current`.
3. A 1–2 sentence description per step synthesized from `name` plus `criteria[]` — steps carry no
   description field.
4. A count line and the resume command **as text**.

**Checkable assertions (all must hold):**

1. Exactly three rows, in roadmap order, scoped to phase 03 only.
2. `03-03` is `current` — the first not-done step — and no row is `next`, because nothing follows it
   in this slice.
3. The Notes column is empty for every row: the sources agree and git confirms both done steps.
4. `execution-log.json` is read **with the Read tool**. A `des-hook:pre-bash` hook blocks Bash
   commands containing that filename, and working around the hook is itself a failure.
5. The resume command appears as text and is not executed.

**Gate failure (blocks the skill change):** the log is read through Bash, or by a script invoked to
dodge the hook; OR a description is copied verbatim from `criteria[]` instead of synthesized; OR the
intent line falls back to the phase name while a slice file exists; OR the skill offers to start
`03-03`.
