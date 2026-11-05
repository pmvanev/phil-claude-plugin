# Expected — HTP-SELFTEST-15

`WROTE` · `VOICE-SKIPPED` · `SLIPS-SKIPPED`

## What must happen

- The tells pass runs as in fixture 01.
- `VOICE-SKIPPED` says no profile named *memo* exists and lists *formal* and *essay*.
- The voice and slip passes are skipped, and `SLIPS-SKIPPED` says the 2 slips asked for had no profile
  to draw from.

## What must NOT happen

- The run does not fall back to another profile.
- No slip is added: without a profile there are no kinds to draw from.
- No profile is built on the spot.

## Why this fixture exists

A missing profile is the likeliest typo. Falling back would reword toward a voice the author did not
choose.
