# Slice 04 — Start a card on GitLab

**Goal (one sentence):** on a GitLab repo, `/phil:start <card>` claims the card by its status label,
cuts or enters its worktree and recommends a route, with the terminals and report lines it has on
GitHub.

Story 5 · Decisions D12–D21 · Issue 98.

## IN scope
- `skills/start/references/gitlab.md`, holding each GitLab call in place of its `gh` call, the way
  `skills/done/references/gitlab.md` does for `/phil:done`. Every rule and outcome in `SKILL.md` stands.
- RESOLVE through `glab api`: the card by number, the search across every page, and the developer as
  `user`'s `username`. Filing uses `glab issue create`.
- CHECK: a closed card, a status label that reads blocked or done, another person's card, and a card
  underway through the developer's open merge requests.
- CLAIM as a label swap: add the In Progress label, remove every other status label, then assign with
  `--assignee +<login>`, reading back the labels and the assignees.
- WORKTREE: the remote's head from GitLab, and merge requests in place of pull requests. The fetch, the
  cut and the entry stay as they are.
- `commands/start.md` grants `glab api`, `jq`, `glab issue create` and `glab issue update`, and its
  prose limits each one.
- Drop the GitHub-only `CANNOT-RUN` from the skill's inputs and its outcome list, and add GitLab to
  the command's description.
- Fixtures 48–55, listed in `feature-delta.md` under Story 5.

## OUT of scope
- A declared label mapping in `phil:board-setup` (D12: start matches the name and asks when the
  match is unclear).
- Reordering the card within its column. `/phil:start` sets no position on either forge.
- GitLab epics and `blocks` links. `/phil:start` reads neither.

## Learning hypothesis
- **Disproves** "the GitHub steps translate to GitLab call for call, and only the claim changes
  shape" if a GitLab path needs a step, an outcome or a report line the GitHub skill lacks.
- **Confirms** it if `references/gitlab.md` adds no outcome token and the GitLab fixtures reuse the
  GitHub terminals.

## Acceptance criteria
AC5.1–AC5.9 in `feature-delta.md`.

## Dependencies
Slices 01–03, shipped in 1.26.0.

## Effort estimate
≤1 day. Reference class: `/phil:done`'s GitLab support, which landed on 2026-11-03 as one reference
file and three fixtures.

## Settle at authoring
- Whether `glab issue create --description '' --yes` files with an empty body and opens no editor. Run
  `glab issue create --help`, and record the answer in `feature-delta.md`.
- How the search counts matches across pages. A paginated `glab api` prints one array per page, so
  `length` counts each page separately (`skills/done/references/gitlab.md`).

## Production data
modive (`basetwin/modive` on `gitlab.intaptai.dev`), whose block lists `status::to-do`,
`status::in-progress` and `status::blocked`, and no Done label.

## Dogfood moment
The same day, run `/phil:start` on modive's top `status::to-do` card from its main checkout, then run it
again. The second run should enter the same worktree and name `/phil:resume`.
