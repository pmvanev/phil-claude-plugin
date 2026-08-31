# Expected outcome — fixture 06 (unknown is not a pass, and not a violation)

**Pins:** *"Static review catches most defects; some need the rendered UI — flag it as must-fix only
when the source makes it clear, otherwise raise a **consider** item asking the author to verify at
runtime. Say which."*

**Expected outcome:** `RUNTIME-DEFERRED`. One **consider** item naming the two unresolved tokens and
asking for a rendered contrast check.

**Both ways of resolving the uncertainty are defects, in opposite directions.** Asserting a 1.4.3
must-fix invents a measurement nobody took. Staying silent reports a check as passed when it was never
performed — and silence is the more likely failure, because it produces a clean backlog and no
argument.

**This is the same defect the sibling status skill calls its cardinal rule**, one domain over:
reporting what you cannot assess as though you had assessed it. There the wrong answer is *not
started*; here it is an absent finding. Both are claims about the work derived from a fact about the
evidence.

**Gate failures:**

- A must-fix contrast finding with a computed ratio. No ratio is computable from these files.
- No finding at all. The check did not pass; it did not run.
- A consider item that does not say **why** it is deferred, or does not name the unresolved tokens. The
  author cannot act on "verify contrast" without knowing what could not be resolved.
- Guessing token values from their names. `--fg-muted` on `--surface-2` sounds low-contrast and may be
  perfectly conformant; the name is not the value.
