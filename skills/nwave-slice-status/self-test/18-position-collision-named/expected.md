# Expected outcome — fixture 18 (a collision is named, never resolved)

**Pins:** *The story-level state, on request* — the roster-ordering rules, and this skill's standing
refusal to pick a winner when sources disagree.

**Expected output** — the state still answers, and the defects ride alongside it:

```
Story: chat-everywhere — in progress · 1 of 4 features done · current feature contested — position 02 claimed by chat-in-web-ui and saved-sessions
Notes: chat-ui-in-extension declares no position — sorted last
```

**The state answers; the ordinal does not.** The fold is quantified over members, not over their order,
so a collision cannot change `in progress`. What it *does* change is **`current feature`** — the first
member, in `position` order, not `done` — which is exactly the field a reader acts on. Both contenders
are `chat-in-web-ui` (`in progress`) and `saved-sessions` (`to do`); nothing in the artifacts orders
them, so **naming either is inventing the answer**.

**`chat-in-web-ui` is the tempting output and it is wrong.** It is "first" only by alphabetical
directory name — precisely the silent tie-break the gate list below forbids. That an emitted winner
would *also* be the plausible one is what makes this failure survive review: the line reads correctly
and a Notes clause beside it looks like diligence rather than contradiction.

**Why not resolve it.** Tie-breaking by directory name, by mtime, or by discovery order invents an order
the artifacts do not contain, and it does so invisibly — the output looks identical to a story whose
positions were declared correctly. This is *Step 2*'s precedence rule applied one level up: **name the
disagreement rather than silently picking a winner.**

**A missing position is not a collision, and both are reported.** `chat-ui-in-extension` declares
membership without a position, which sorts last by rule and is stated. Merging the two conditions into
one warning loses the difference between *an order that conflicts* and *an order that was never given*.

**Why this is the steady state, not an edge case.** The declaration is hand-authored in a markdown
header and **nothing validates it** — recorded in this feature's delta as a `check-invariants.py`
candidate that was deliberately not committed to. Until something checks it, a collision is what a
renumbered or copy-pasted story looks like, and this skill is the first thing that sees it.

**Gate failures:**

- Emitting **any** member as `current feature` while the collision stands — including
  `chat-in-web-ui`, which alphabetical order makes the plausible wrong answer. The defect, stated.
- Ordering by directory name, mtime, or discovery order as a silent tie-break.
- Suppressing the state until the collision is fixed. The state is derivable and correct; withholding it
  makes an ordering defect look like an unreadable story.
- Reporting the collision and omitting the missing position, or the reverse.
- Counting `4` members but omitting the one with no position from the roster. It is a member.
- Returning `unknown` because the record is imperfect. `unknown` is for an unassessable roster, not an
  unordered one.
