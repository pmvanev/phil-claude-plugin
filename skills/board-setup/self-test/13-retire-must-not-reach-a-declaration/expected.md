# Expected — BS-SELFTEST-13

`UNCHANGED`, with the declared region absent from the drift report entirely.

## What must happen

The drift report is computed over the hand-written prose only. Both generated regions are excised
first, so a declared line cannot appear in any bucket, cannot be offered, and cannot shift the line
numbers the report cites.

`retire_line` refuses any line inside the declared markers even when explicitly asked.

## What must NOT happen

No declared line filed as `contradicts`. No offer. **No deletion, on any answer.**

## Why this fixture exists

This was a real, reachable data-loss path, not a hypothetical. `_excise()` removed only the probed
region, so declared lines were fed to the differ as though they were hand-written prose. A declared
line carrying a docs-root URL or an id-shaped token that did not match the probe was therefore filed as
`contradicts` — which made it **retire-eligible**, and the retire offer would have deleted it.

That is the worst outcome this command can produce. Everything else it writes can be regenerated from
the forge; a declaration cannot. It is the answer to a question no forge records, obtained by asking a
person, and if it is deleted the only recovery is to ask again — assuming anyone notices, which the
drift report gives them no reason to.

Two guards, deliberately redundant: the differ cannot see the region, and the deleter refuses the
range. Either alone would have prevented the loss; a value with no second copy anywhere deserves both.
