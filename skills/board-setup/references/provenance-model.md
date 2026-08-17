# Why every line carries its provenance

`SKILL.md` gives the three-category table and the rule that every generated line names its query.
This file is why those exist.

## The evidence is this plugin's own CLAUDE.md

Most of the hazards in its `## Issue board` section were written *after* the thing they document had
already gone wrong — two still carry the date they were learned. Each was paid for by a call that
reported success while doing something else: a `gh issue close -c` that silently dropped its
comment, a commit message whose bare `#22` closed an unrelated card, a near-miss on
`updateProjectV2Field` that would have destatused 25 cards.

A template a human fills in as they get bitten documents the past rather than preventing it.

## Why `assumed` is a category and not a rounding error

`projectV2 { workflows { name enabled } }` returns `Auto-close issue: enabled`, so the hazard is
discoverable. But `ProjectV2Workflow` exposes exactly `createdAt, enabled, fullDatabaseId, id, name,
number, project, updatedAt` — and **no field for the configured trigger statuses**.

So "a status→close workflow is on" is probed, and "`Done` fires it" is assumed. A block saying
*"Auto-close on Done is ENABLED"* is one confident sentence spanning a fact and a guess, and the
whole point of the three categories is that the two must not be spelled the same way.

## The fourth value, which is not a category

`unread` — the forge would not answer. It is **not** a fourth provenance category, because it is not a
kind of knowledge: it is the absence of both a fact and a guess. So it never enters the markers under
any label, and the renderer drops it rather than spelling it as either.

It is not forge-specific in principle, though GitLab is where it first appeared: `projects/<id>` reads
unauthenticated while `projects/<id>/labels` returns 401, so the read failed *partially*. A partial
failure is the kind that renders as a plausible value — `{"labels": [], "count": 0}`, which on GitLab
states the project has no board.

The sentinel is `None`, never `[]`. **An empty collection is an answer and an unread one is not**, and
a codebase whose thesis is that two things must not be spelled the same way cannot afford to spell
these two the same way.

Note the naming collision, which is deliberate but worth knowing: `refresh_region` also refuses with
the word *unread* when handed no rendered region, meaning "I cannot tell you whether anything changed".
Different subject, same honesty.

## Why the probe is a script

AC1 — *no value inside the markers was typed by a human* — is a property code can hold and prose can
only request. In the finished file a remembered id is indistinguishable from a probed one, which is
this feature's own failure mode turned on itself.

The same reasoning extends to `region-place.py`: a region placed one line off still looks placed,
and a reflowed bullet still reads as English.

**A partial block is worse than none.** A block silently missing its Status field id reads exactly
like one whose board has no Status field.

## What the probe reaches, and what it cannot

Measured against `phil:issue-board`'s *Per-project setup* template, which owns the block's content:
the probe reaches every field except **`label-families`** and **`local-task-system`** — both slice
03's, both correctly *declared* rather than guessed. The slice brief owns the KPI-1 reading; the
durable fact is which two fields no forge can answer.

On GitHub the **tier comes out of the probe as *not applicable***. The bullet exists because GitLab
gates scoped labels and real `blocks` links behind Premium and GitHub gates neither, so there is no
GitHub tier call to make and none to invent. When GitLab lands (slice 06) the probe calls
`phil:issue-board`'s tier check rather than restating it.

## Why the five facts with no template field are still written

`default-branch`, `fork`, `project-discovery`, `board-view` and `other-single-select-fields` carry
no `template_field`, and they are not surplus. **How the board was found is itself a constant**: a
repo whose project is unlinked is a repo where `gh project item-add` is the only way a card ever
arrives, and a run that omitted that would leave the next person to discover it by filing a card
that vanishes.
