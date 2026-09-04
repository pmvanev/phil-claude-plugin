# Expected outcome — fixture 01 (the clause carries what the edge cannot)

**Safety core, and it is the same discriminator `phil:nwave-issue-board` uses one tier up:** the forge
records the **edge**, and the clause after the dash records **why you stopped**. The edge is rendered by
the forge; the clause is composed by whoever pivoted. **The prose standard reaches the clause and never
the edge** — there is nothing to compose in a link.

**Why the clause is load-bearing.** `SKILL.md`: *"Six issues deep, the edge alone tells you what blocked
but not what you were in the middle of."* And on GitHub, where the reverse edge is written for you, it
*"writes only the edge, never the reason, so the prose line goes on both issues either way."*

**Expected decision:** `CHAIN-COMPOSED`.

**Checkable assertions (all must hold):**

1. **Both ends written.** A line in 12's description naming 47 as the blocker, and the mirror in 47's
   naming 12. The forge writing the reverse edge does not discharge the mirror.
2. **Under the fixed `## Chain` heading, in the description — never a comment.** Descriptions are what a
   reader sees on landing; a comment scrolls away and has to be hunted for.
3. **Written before work starts on 47**, not after it finishes. The rule exists because the reasoning is
   only in someone's head at the moment of the pivot.
4. **The clause says why the work stopped, and does not restate the edge.** `Blocked by 47 — blocked by
   issue 47` is the degenerate failure: it satisfies the shape and carries nothing the link did not.
5. **Composed against `rules/writing.md`.** All three `enumerable_facts` present; no expletive
   construction (`there is`, `it should be noted that`, `what this does is`); active voice; the emphatic
   word last. Concision is one of the standard's eleven principles, not the whole of it.
6. **No word count is asserted anywhere in this fixture**, and none may be introduced to satisfy it.
7. **The chain is not hand-maintained as blockers close.** The linked issue is authoritative about its
   own state, so nothing here promises to update the line later.

**Gate failure (blocks the skill change):** an edge with no clause; OR a clause that only restates the
edge; OR a line written as a comment rather than into the description; OR one end written and not the
other on the ground that GitHub mirrors the edge; OR any construction named in assertion 5; OR a word
ceiling introduced.

**Why no candidate text is supplied.** `SKILL.md:456` ships a real, tight example — *"Blocked by #47 —
token refresh must land first or the retry test can't be written"*. Offering it beside a padded variant
would test **selection**, and selection is passed by "publish the shorter string", which is the word
ceiling `board-prose-standard` [D5] refuses. The shipped example is the reference for what good looks
like; it is not an option to pick. This is the correction `plugin-dev:skill-reviewer` finding C2 forced
on slice 01's fixtures, applied here before the same mistake could be repeated.
