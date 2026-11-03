# Slice 04 — GitLab, and a run with no card

**Goal (one sentence):** `/phil:done` closes a GitLab card as it closes a GitHub one, and with no
argument checks the session's own work and clears what it left.

Decisions D1–D9, carried to a second forge and to a session no card tracks. Settled in
`feature-delta.md`, *Decisions summary*, 2026-11-03.

## IN scope
- `skills/done/references/gitlab.md`: the `glab` form of every read and write in `SKILL.md` and
  `clear.md`, each read run against a real GitLab instance.
- The GitLab Status write: remove the card's status labels; the closed list is Done.
- `skills/done/references/no-card.md`: no argument runs without a card. The session's asks, its pull
  requests as the conversation shows them, CLEAR's lines alone, and the `FINISHED` outcome.
- Fixtures 39–45.

## OUT of scope
- Retiring a snapshot on resume; issue 76's autopilot.
- Running the GitLab writes from a fixture: the fixtures are model-driven.

## Learning hypothesis
- **Disproves** "the conversation is enough to find the session's work" if a real run without a card
  misses a branch the session made, or lists one it did not.
- **Confirms** it if the next two runs without a card clear exactly the session's branches.

## Acceptance criteria
- On a GitLab forge line, the run reaches CLOSE; it never stops at the forge check.
- Every `glab api` read is a GET, naming the host and the URL-encoded project.
- The card leaves its status label before it closes; no label is added.
- With no argument, nothing touches a card, and a branch the conversation never names stays put.
- A finish holding only the snapshot here asks one question; a finish holding nothing asks none.

## Dependencies
Slice 03.

## Effort estimate
≤1 day.

## Production data
modive issue 21 and its merge requests, read 2026-11-03.

## Dogfood moment
The next GitLab finish on modive, and the next session with no card.
