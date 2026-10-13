# Applying the mechanical column — `/phil:groom-fix`

Part of the `groom-issues` skill. `SKILL.md` governs this command as much as this file does: the
standard, the scan, the defect table, the cross-issue candidates, reporting, the decision outcomes and
the invariants all apply here.

**Mechanical is a claim about the fix, never about the consent.** It says the content is derivable and
invents nothing — a relative path has one correct absolute form, a one-sided chain's missing half is
written on the other issue. It says nothing about whether the user wants their board edited now.

**Scope first, and write nothing before the answer.** The user picks a defect class, a subset of
issues, or everything — the tool picks nothing, not even the safest fix. Group the offer by class, because that is the unit a class-level answer selects; a flat list
makes the user do the grouping the report should have done.

**Scale the offer to the population, and never the consent.** Over one finding, a
class/subset/everything menu is ceremony, and people learn to click through ceremony. One finding gets
one confirmation naming it. Nothing gets applied because it was trivially small.

**Report the checks that ran and found nothing.** "One defect" over five silent checks reads as a thin
scan. Naming the passes separates *this board is clean* from *this tool looked at one thing*. Report them
as passed: they had an oracle and ran, which is stronger than `REPORT-UNEVALUATED`.

**Every change carries the reason it needed no judgement**, per change, not per run:

```
#31 — rewrote ./docs/adr/ADR-013.md as <absolute URL>. No judgement: GitHub emits relative
      paths verbatim so the original 404s for every reader; target confirmed on origin/main;
      nothing invented.
```

The reason is the deliverable: it makes the mechanical claim falsifiable. "Applied 2 fixes" cannot be
contradicted by a reader; the sentence above can.

**This command settles what the scan could not, and must actually do it.** The scan reports an unlinked
path as an unverified *candidate* because confirming the target needs `git`, which its `Bash` scoping
withholds. `/phil:groom-fix` holds `git ls-tree`, and that grant exists for exactly this: run
`git ls-tree origin/<default-branch> -- <path>` on every candidate in scope, and the confirmed ones
become findings you may fix. A candidate that will not confirm **stays unfixed and stays reported**,
with the check that failed named.

Read the scan's *unverified* as a statement about its tools, not about the link. Carried across, it
would make this command refuse its most common correct edit.

**The scope is a line, not a hint.** A mechanical defect outside the chosen scope stays untouched — and
stays *mentioned*. Out of scope means untouched, not unmentioned; a defect that disappears from the
output reads as fixed.

**The column is a property of the defect, not of the card that holds it.** An issue carrying one
mechanical and one semantic defect gets one of each treatment in the same pass. Skipping the card
because it also has a semantic defect would empty the mechanical column by proximity.

**Re-read before every write**, per `SKILL.md`, and act on no copy from the scan. A body that moved is
refused even where the defect survives: the surrounding text is unassessed, and the user agreed to a
scope over the board as reported.

**Refuse a generated region even when the content is right.** A fix inside `nwave:status` markers is
destroyed on the next refresh and disagrees with its source until then. Refuse with the reason and point
at the generator. Leave the bytes just outside the markers alone too: a "nearly right" edit there leaves
the region wrong and hides it. Mechanical governs the content, ownership governs the bytes, and both
must pass.

**This is not a bulk fixer.** On this repo's board on 2026-08-13, six mechanical checks found **one**
defect, made by the maintainer minutes earlier. Its value is catching the defect its author just made;
build no ceremony for a full queue.
