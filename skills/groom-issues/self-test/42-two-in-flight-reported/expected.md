# Expected outcome — fixture 42 (two in flight is the finding, and it is not "oversized")

**Pins:** the *two features in flight on one story card* signal, and its derivation from
`phil:issue-board`'s concurrency clause rather than from a new granularity rule.

**Expected: exactly one finding**, quoting **every** in-flight feature by name with its **feature-roster**
row and its `⚠ also in flight` note. **Report only — the scan names `/phil:groom-set` and does not offer**,
because confirming the state against the artifacts needs the fold it cannot run.
Offered resolution: split into feature cards under a goal.

**Why concurrency and not size.** This card is fixture 41's but for the state of one member — which additionally makes it carry a `⚠ also in flight` note. The
only difference is that two members are moving at once — and *"two halves sit in different columns at the
same time only when two people are working them at once"* is the shipped rule. **The card did not become
too big; it stopped being one person's work.**

**The evidence must be quoted, not summarised.** "Two features in flight" is a claim the reader has to be
able to check against the card in front of them. Naming both features and pointing at the two glyphed
rows is what separates a finding from an assertion — and the block renders those rows precisely so this
finding can be made from them.

**One finding, not two.** The temptation is to report each in-flight feature separately. The defect is
the *pair*; two findings imply two independent problems and invite fixing one.

**This is the check the block was told to expect.** `phil:nwave-issue-board` renders two `▶` rows and a
`⚠ also in flight` note rather than hiding or resolving the ambiguity, on the explicit grounds that
grooming's finding is made from that evidence. Until this fixture, that delegation named a check which
did not exist.

**Gate failures:**

- Zero findings. The silent failure this class exists to close.
- An oversized finding instead. Right conclusion, wrong oracle — and the repair that produces it reports
  fixture 41 too.
- Reporting it without naming every in-flight feature.
- Counting `▶` glyphs instead of reading the state word. A story block carries two tables and `▶` means
  `current` in the slice roster, so a glyph count fires on fixture 41 — the false positive this pair exists
  to separate.
- Offering a resolution. The scan reports; `/phil:groom-set` acts.
- Two findings, one per in-flight feature.
- Offering to consolidate the members further, or to file a story card. It already is one; the resolution
  runs the other way.
- Offering a milestone as the fix. A goal is the container for the *resulting* feature cards, not a
  substitute for splitting.
