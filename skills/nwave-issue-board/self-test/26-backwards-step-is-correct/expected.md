# Expected outcome — fixture 26 (the label steps backwards, and that is right)

**Pins:** *"it is therefore NOT monotonic, and that is correct output rather than a bug … say so in the
block, every time."*

**Expected:** `wave: design` is swapped for **`wave: discuss`**, the routing line becomes
`Work this with: /nw-discuss · feature saved-sessions`, and the block carries the clause — that a new
feature starts at the beginning, so a story card's wave moves backwards at every feature boundary.

**This fixture exists because the correct output is indistinguishable from a regression.** Anyone whose
mental model is the feature card — where the wave only advances — reads `design → discuss` as a bug,
and the obvious repair is to hold the label at its furthest-reached value. That repair is monotonic,
plausible, and **reintroduces accumulation the moment a third feature starts**, because "furthest
reached" over four members is four values.

**Without the explanatory clause the fixture is not enough.** A fixture prevents a *rule* from being
changed; only the clause in the block prevents a *human* from "correcting" the card by hand. The rule
and its explanation ship together, and the explanation is generated, not typed, so it cannot drift from
the label it explains.

**The forward half is real, the backwards half is not observable here.** In this plugin's own story both
members finished DISCUSS before the card was built, so the backwards step was reconstructed from two
recorded states rather than watched. That is why this case needs a fixture and why the slice brief says
so — a dogfood claim must name what it actually exercised.

**Gate failures:**

- Holding the label at `wave: design` because DESIGN is further than DISCUSS. The plausible repair, and
  the one that reintroduces accumulation.
- Carrying both labels through the transition.
- Emitting the new label with no explanatory clause. The card is then correct and unbelievable.
- Treating the backwards step as a condition to report to `phil:groom-issues`. It is normal operation,
  not a defect; reporting it trains a reader to ignore real findings.
- Leaving the routing line pointed at `chat-in-web-ui` after it is done.
