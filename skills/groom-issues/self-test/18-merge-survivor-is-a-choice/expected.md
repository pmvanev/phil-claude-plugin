# Expected outcome — fixture 18 (the lower number is not the answer)

Two cards, one piece of work. The older card is thinner; the newer one carries the acceptance criteria
and everything already points at it.

**Expected decision:** `APPLY-MERGE`, with `#34` surviving **because the user said so**, and the three
steps in this order:

```
1. Moved into #34: the reproduction steps from #9, which existed nowhere else.
2. Closed #9 with a comment: "Merged into #34, which carries the acceptance criteria
   and the existing references. Reproduction steps moved there first."
   Status: #9 moved to Done by the project's closed-item workflow. This command holds no
   gh project item-edit and did not place it.
3. Re-pointed the one reference to #9: rewrote #22's "blocked by #9" as "blocked by #34".
```

**Why the survivor is asked and not derived.** The lower number is older, and age correlates with
nothing that matters here — the acceptance criteria, the incoming links, and the better-written body are
all independent of it. Defaulting to `#9` in this fixture discards five acceptance criteria and orphans
three references, and reports success while doing it. The rule holds even when the choice looks obvious:
the run that gets this wrong is the one where the older card was the one worth keeping.

**Why the order is fixed.** Detail moves first because after the close the losing body is still readable
but nobody re-reads a closed card. References are re-pointed last because until the close lands there is
no settled answer to point them at — re-point first and an abandoned merge leaves the board pointing at
a card that was never the survivor.

**Gate failures:**

- Keeping `#9` because it is lower, or offering the merge with a survivor already chosen.
- Closing `#9` before moving the reproduction steps. They exist nowhere else, and a closed card is where
  detail goes to stop being read.
- Leaving `#22` pointing at `#9`. A merge that leaves references on the tombstone has relocated the
  confusion, not removed it, and the next reader of `#22` follows a link to a closed card whose comment
  they must then read to find the live one.
- Posting the reason as a comment after the close. Once the project's workflow has run the issue is
  already closed, and a later comment is silently dropped — use `gh issue close -c` so the reason lands
  with the close.
- Reporting the merge without saying `#9` is now in Done. The user asked for a merge; a card leaving the
  triage queue is a consequence they were not shown.
