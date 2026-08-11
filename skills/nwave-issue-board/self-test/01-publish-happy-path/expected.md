# Expected outcome — fixture 01 (walking skeleton)

**Expected decision:** `PUBLISHED`.

The end-to-end path with nothing ambiguous: artifacts agree, the forge is empty, the wave is known.
Everything this skill does correctly, once.

**Checkable assertions (all must hold):**

1. One parent issue for the feature, carrying a wave label for DELIVER.
2. One issue per slice — two of them — attached to the parent as sub-issues, per the commands in
   `phil:issue-board`. Not one issue per step.
3. Each slice issue's description carries a `nwave:status` block delimited by
   `<!-- nwave:status:begin -->` / `<!-- nwave:status:end -->`, with a timestamp.
4. The step table carries four columns — `Step`, `What it does`, `Status`, `Notes` — matching what
   `phil:nwave-slice-status` renders.
5. Statuses are the ones `nwave-slice-status` returns, not a fold performed here.
6. The end state is read back, per `phil:issue-board`.

**Gate failure (blocks the skill change):** an issue per step; OR a status computed locally; OR a
block written without markers or without a timestamp; OR any write under `docs/feature/`.
