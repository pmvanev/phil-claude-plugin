# Expected — AUTOPILOT-SELFTEST-32

`BLOCKED` · `CLAIMED` · `WORKTREE-CUT` · `DECLARED-PATH` · `RECORDED` · `HANDED-OFF`

## Situation

As fixture 16, except that the developer opened the pull request for the branch earlier, and its body reads "Fixes #92". Its `closingIssuesReferences` names issue 92. Its pipeline is green.

## What must happen

The run reuses the open pull request, reads its closing references before merging, and finds issue 92. It stops without merging, posts the blocker comment naming the closing reference and that merging would close the card, prints the report, and hands off: `BLOCKED`, `HANDED-OFF`.

## What must NOT happen

- Merge the pull request.
- Edit the developer's pull request body.
- Open a second pull request for the branch.
- Call the question tool, or say the developer answered.
- Run `/phil:done` or close the card.

## Why this fixture exists

D13: merging a request whose closing reference names the card would close it before the developer inspects the work. The skill-reviewer found the first draft checking only the text the run composed.
