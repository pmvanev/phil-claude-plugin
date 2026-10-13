# Expected outcome — fixture 01 (generated region left untouched)

**Situation.** A `CLAUDE.md` holds a region between `<!-- board-tool:v1:begin -->` and
`<!-- board-tool:v1:end -->`. Inside it sits a bullet whose explanation the checklist's
"no long explanations" item would otherwise cut.

**Pass.** Every byte from the begin marker through the end marker is identical before and after the
run. The report names the region as found and left unchanged.

**Fail.** Any change inside the markers: a reworded bullet, a dropped id, a reflowed line, a moved
marker. The region's owner reads these ids back; a silent edit corrupts its data.

**Wound.** `board-setup` recorded that `/phil:claude-md` could compress or delete probed ids, and
asked users to re-run it after every pass (fold-back 2026-10-13, 0.101.0).
