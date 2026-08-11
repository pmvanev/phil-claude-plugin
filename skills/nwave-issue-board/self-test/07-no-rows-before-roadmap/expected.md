# Expected outcome — fixture 07 (step ids do not exist yet)

**Where it fails silently.** The slice files describe scope in enough detail that plausible steps can
be written from them. Those steps would have invented ids, match nothing in any later
`execution-log.json`, and never update again — a table that looks like a plan and tracks nothing.

**Expected decision:** `NO-ROWS-BEFORE-ROADMAP`.

**Checkable assertions (all must hold):**

1. A parent issue and three slice issues are opened; the roster is known at this stage.
2. The wave label reads DESIGN.
3. No step table is published in any slice issue. No step ids are invented from slice prose.
4. Each slice issue says the step table arrives with the roadmap, rather than leaving an empty table
   that reads as "no steps".

**Gate failure (blocks the skill change):** any step row published before `roadmap.json` exists; OR
slice issues withheld because the roadmap is missing, which delays the half that is knowable.
