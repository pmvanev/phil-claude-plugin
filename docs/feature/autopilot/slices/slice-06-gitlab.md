# Slice 06 — GitLab

**Goal (one sentence):** `/phil:autopilot` carries a card on GitLab as it does on GitHub, merge request
in place of pull request.

Story 6 · Decision D10.

## IN scope
- `skills/autopilot/references/gitlab.md`, giving each GitHub call its `glab` form from
  `phil:issue-board`, as `/phil:start`'s and `/phil:done`'s GitLab references do.
- The merge request, its pipeline, the status labels and the card comments on GitLab.
- Removing slice 01's GitLab stop.
- Fixtures: no GitLab run stops for the forge (AC6.1); every call follows the GitLab mechanics (AC6.2).

## OUT of scope
- Anything that differs from GitHub beyond the forge mechanics.

## Learning hypothesis
- **Disproves** "the GitHub run ports with only forge mechanics changed" if a GitLab run needs a
  decision the GitHub run never made.
- **Confirms** it if a modive card lands with the same report lines.

## Acceptance criteria
AC6.1–AC6.2 in `feature-delta.md`.

## Dependencies
Slices 01–05.

## Effort estimate
≤1 day. Reference class: `start-work` slice 04, GitLab.

## Production data
A modive card.

## Dogfood moment
The same day on modive, naming the plugin version it ran against.
