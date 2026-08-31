# Expected outcome — fixture 02 (the boundary is checkability, not subject)

**Pins:** the split made on 2026-08-31, when the aesthetics rule was divided and its checkable third
moved into `ux.md`. Both halves live in one file here **on purpose** — the risk is not missing either
one, it is conflating them.

**Expected outcome:** `BOUNDARY-HELD`. Exactly one must-fix:

- animation with no reduced-motion variant → *"Honour the user's reduced-motion preference … keep an
  equivalent still state (2.3.3)"*

And **silence** on the palette and the typeface.

**Why both directions are failures, and why they fail differently.** Missing the reduced-motion gap
loses a real accessibility defect quietly. Raising the palette is worse in practice: it is a confident,
well-formatted finding telling an author their deliberate design choice is a defect, citing a standard
that explicitly disclaims it. The author either complies with a wrong instruction or stops trusting the
tool, and both cost more than the finding was worth.

**The line the reviewer must hold.** An animation's **reduced-motion variant** and its **frame cost**
are reviewed here. Whether the animation is **attractive** is not. Same element, same file, opposite
verdicts — which is why "aesthetics are out of scope" is the wrong summary and was rewritten in four
places to stop saying it.

**Gate failures:**

- Raising the palette or the typeface at any severity, including **consider**. Taste is not a soft
  finding, it is not a finding.
- Missing the reduced-motion gap because the element is decorative. Decorative motion is exactly what
  2.3.3 is about.
- Raising the reduced-motion gap as **consider**. The absence of a `prefers-reduced-motion` block is
  visible in the source; nothing needs the rendered page.
- Flagging the parallax as a performance defect *instead of* an accessibility one, and stopping there.
  Frame cost is an advisory; the missing variant is always-flag. Reporting only the softer one
  downgrades a defect to a suggestion.
