# Expected outcome — fixture 16 (one finding, and it still needs an answer)

Six mechanical checks ran with a real oracle. Five found nothing. One found one thing.

**Expected decision:** `SCOPE-FIRST`, proportionate — a single confirmation naming the single change:

```
One mechanical defect, board-wide:

  #22 — `.claude-plugin/plugin.json` is named in prose but not linked. Target confirmed on
        origin/main; the absolute URL is derivable and invents nothing.

Apply it? (5 other mechanical checks ran and found nothing: relative links, wrapped issue
refs, accumulated labels, one-sided chains, 19 absolute links all resolving.)
```

**Both halves of that are load-bearing.** The scoping step scales *down* to the population, because a
class/subset/everything menu offered over one finding is ceremony — and a step that feels like ceremony
is the step people learn to click through, which is how the consent gate stops working on the run where
it matters. But consent itself does not scale away: one trivial finding is still someone's board.
`SCOPE-FIRST` is the same decision as fixture `11`, rendered at the size of the problem.

**Why the five empty checks are reported and not omitted.** "One defect found" over a silent five reads
as a thin scan. Naming the checks that ran and found nothing is what distinguishes *this board is clean*
from *this tool looked at one thing* — the same distinction fixture `09` pins for rules that could not
run at all. Here the checks had oracles and passed, which is a stronger statement than `REPORT-UNEVALUATED`
and must not be blurred into it.

**Gate failures:**

- Offering the three-way scoping menu for one finding. Proportionality is the fix; ceremony is the defect.
- Applying it without asking because one is trivially few. The population is not the permission.
- Reporting `1 mechanical defect` without the five passing checks, so a clean board is indistinguishable
  from a shallow scan.
- Reporting the five as unevaluated. They had oracles and they ran. Conflating *passed* with *dark*
  understates the board in the opposite direction and cheapens the `REPORT-UNEVALUATED` signal.

**Provenance — this is a measurement, not a hypothetical.** Run against this repo's real board on
2026-08-13, after slice 01 had been dogfooded twice and its findings fixed by hand. The mechanical column
held exactly one defect, and it had been created by the maintainer **that same session**, minutes after
re-reading the rule it breaks — an unlinked path in the body of the issue filed about stale plugin caches.

That is the same provenance fixture `10` records for one-sided chains, and it says something the brief
did not anticipate. Slice 02's learning hypothesis offered two outcomes: the boundary is real, or it is
empty because every mechanical fix turns out to need a question. Neither happened. The boundary is real
and the fixes need no question — **and the population on a maintained board is about one per grooming
cycle, authored by whoever last read the rules.** This slice is therefore not a bulk fixer. Its value is
catching the defect its own author just made, which is why the scoping step had to learn to be small.
