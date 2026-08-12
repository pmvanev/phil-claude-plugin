# Expected outcome — fixture 06 (the card names its owner)

**Pins:** slice-02 AC1 and AC2, and **KPI-2** (`pickups where the user must say "use the nWave skill" =
0 across five consecutive pickups`).

**Expected decision:** `ROUTE`. The spine names `/nw-execute` as the owner of work in the DELIVER wave
and stops, rather than reading the card's description and starting to edit files.

**Naming is the whole of routing — the spine does not run the command.** `/phil:resume` holds no
`Write`, no `Edit`, and read-only `Bash`; invoking `/nw-execute` would route around all three, and a
read-back that starts work is the failure fixture 04 exists to prevent, made automatic. "Hands the
work over" means *stops and says who owns it*, not *launches it*.

**Gate failure (blocks the skill change):** the session summarises the card and begins the work itself.
This is the exact reported defect, and it is silent — inline work looks productive, and produces
plausible output. The cost surfaces later: working a DELIVER step inline skips the TDD cycle
`/nw-execute` dispatches and skips the artifact writes that make the work resumable, so the *next*
session's `/nw-continue` reconstructs from artifacts that were never written.

Naming the owner without handing over also fails. An announcement followed by freelancing is worse
than silent freelancing, because it reads as compliance.
