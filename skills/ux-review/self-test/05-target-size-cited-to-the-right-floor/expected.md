# Expected outcome — fixture 05 (a true-sounding citation for a criterion that passes)

**Pins:** *"don't cite WCAG for sub-44/48px targets — 24px is the WCAG floor; 44 (Apple) / 48
(Material) are comfort guidance, cite the HIG."*

**Expected outcome:** `CITATION-CORRECT`. The element **passes** 2.5.8. At most a **consider** item
noting it is below platform comfort guidance, attributed to the platform, not to WCAG.

**Why a false citation is worse than a missed finding.** A missed finding leaves the product where it
was. A finding that cites 2.5.8 against a conformant 30px target puts a false accessibility violation
into a backlog that people treat as a compliance record — and the citation is what makes it credible.
It will be believed precisely because it looks like the other findings in the file.

**The failure is severity and attribution, not judgement.** Wanting a bigger target here is
defensible; that is what the advisory tier is for. Calling it a WCAG violation is not a stricter
opinion, it is a false statement about a published standard.

**Gate failures:**

- Any finding citing 2.5.8, "WCAG", or "AA" against this element.
- Raising it as **must-fix** on any grounds. The always-flag tier is objective defects; this is not one.
- Reporting "44px minimum" as though it were a requirement rather than Apple's guidance.
- Silently widening the element in a suggested fix without saying which guidance motivates it.
