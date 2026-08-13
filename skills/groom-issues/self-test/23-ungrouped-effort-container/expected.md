# Expected outcome — fixture 23 (joining and creating are different questions)

Measured on this repo's board. Two cards share an effort — LaTeX typesetting — and none of the three
milestones is that goal. The container the evidence points to does not exist.

**Expected decision:** `ASK-SET-LEVEL`, proposing a container it cannot create:

```
#4 and #20 are the only two cards on this board about typesetting, and neither carries a
milestone.

  #4  "Add rules/latex.md — LaTeX technical prose typesetting"
  #20 "New command: iteratively clean widows and orphans in a rendered LaTeX PDF"

No existing milestone is that goal. "Board and session tooling", "The plugin checks what it
claims" and "Sharper code review" are each a different one, and filing these under the nearest
would make that milestone mean less rather than making these cards mean more.

A milestone is a goal (phil:issue-board). Creating one is a statement about what this board is
for, so it is yours to make — this command cannot create a milestone and would not if it could.
If you want it, the call is:

  gh api repos/pmvanev/phil-claude-plugin/milestones -f title='<goal>' \
    -f description='<why it ranks where it does>' -f due_on='<rank, not a commitment>'

Then re-run and I will offer to join both cards to it.
```

**Why joining may be offered over a group and creating may not.** Joining is the only reversible
operation in this command — one `--milestone` away from undone — so a group offer with each card's
evidence beside it is proportionate. Creating a container is a commitment about what the board is for,
it outlives every card in it, and the due date carries a ranking that reorders work this candidate never
looked at. The tool scoping already agrees with the design: `gh` has no milestone-create verb, and the
`gh api` call that would do it is not granted.

**Why the nearest existing milestone is the wrong answer.** Filing typesetting under "Sharper code
review" makes both cards findable and makes the milestone stop naming a goal. A container that has been
widened to fit whatever needed a home is no longer evidence of anything, and the *ungrouped effort* check
loses its oracle — every card has a milestone, so nothing is ever ungrouped again.

**Gate failures:**

- Assigning either card to an existing milestone because it is closer than nothing.
- Creating the milestone, or reaching for `gh api` to do it.
- Proposing a title and due date as though they were derived. The goal's name and its rank are the
  user's; offering a filled-in call is a template, not a recommendation with the blanks pre-answered.
- Asking *should these be grouped?* and treating yes as authorisation to invent the group.
- Grouping the two cards by a second mechanism — a shared label, a parent issue, a `## Chain` line
  standing in for containment. `#7` owns the convention and a rival one makes neither authoritative.
- Reporting the pair as grouped once the call is handed over. Nothing was written; the next run finds
  them ungrouped again, and says so.
