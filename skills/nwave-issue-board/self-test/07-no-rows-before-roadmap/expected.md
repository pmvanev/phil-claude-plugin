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

## Amended 2026-08-14 — the branch where the roadmap never arrives

This fixture requires the card to **say** its step table arrives with `/nw-roadmap`, because a card carrying
neither a table nor that line reads as a feature with no steps.

**That sentence assumes the roadmap eventually arrives.** In a repo whose build path leaves the nWave waves
— authoring prose with `plugin-dev`, for instance — DELIVER never runs, `roadmap.json` is never written, and
the promise is one nothing will keep. Observed in this plugin's own repo, 2026-08-14.

**Second expected branch.** Where DELIVER will not run, the card states that **the roster is the finest
granularity that will ever exist**, and the roster carries the two-line descriptions the step table would
have carried. Additional gate failures:

- Writing "the step table arrives with the roadmap" in a repo where it will not. A promise nobody will keep
  misinforms every future reader, and it is indistinguishable from a promise that is merely late.
- Silently omitting both sentences. That is the original defect this fixture exists to catch, reached by the
  other route.
- Inventing step ids to fill the gap.
