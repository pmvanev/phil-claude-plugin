# Blocking links, sub-issue edges and a parent's count

Part of the `issue-board` skill. Read it before writing or reading a blocking link or a sub-issue edge, reading a parent's completion count, or closing an issue that has a parent — setting Done included. Its `SKILL.md` governs this file too.

## Dependencies depend on the tier

- **GitLab Premium and above**: real link types — `blocks`, `is_blocked_by` — enforced by GitLab
  and rendered with backlinks on both sides. Prefer these. Created via
  `glab api --method POST "projects/<id>/issues/<iid>/links" -f target_project_id=<id> -f target_issue_iid=<iid> -f link_type=blocks`
  *(command form unverified — check whether your `glab` exposes a subcommand for this).*
- **GitLab Free**: only `relates_to` is available; `blocks` and `is_blocked_by` are Premium and
  above. Use `relates_to` and carry the direction in a `Blocked by #N` line in the description.
- **GitHub**: native `blocked by` / `blocking` links and sub-issues, exposed as first-class flags.
  These are recent — older guidance says GitHub has none, so check `gh --version` before believing
  it. Verified on `gh` 2.97.0:

  ```sh
  gh issue edit 123 -R owner/repo --add-blocked-by 200 --add-blocking 300,301
  gh issue edit 100 -R owner/repo --add-sub-issue 123,124   # or: --parent 100 on the child
  gh issue edit 100 -R owner/repo --remove-sub-issue 123    # or: --remove-parent on the child
  ```

  **The edge can be removed as well as added** — `--remove-sub-issue` / `--remove-parent`, and GraphQL
  `removeSubIssue`. Verified on `gh` 2.97.0, 2026-08-14. This matters because *removing* the edge is the only
  way to stop a child counting toward its parent's completion; see *A parent's "N of M done" counts different things on each forge* below.

  Each flag takes an issue number or a URL, so links cross repositories. It is one edge read from
  both ends — `blockedBy` and `blocking` are both fields on `Issue` in GraphQL — so the reverse side
  needs no second write.

### Writing a sub-issue edge is a flag; READING one is GraphQL

The asymmetry costs an hour if you assume the flags imply a field. **`gh issue list --json` and
`gh issue view --json` expose no `parent` and no `subIssues`, and no flag adds them** — `--json` rejects
both names outright. The edge is readable only through GraphQL:

```sh
gh api graphql -f query='query($o:String!,$r:String!){ repository(owner:$o,name:$r){
  issues(first:100,states:OPEN){ nodes { number
    parent { number }
    subIssues(first:50){ nodes { number } } } } } }' -f o=<owner> -f r=<repo>
```

**One whole-board call, not one per issue.** The nesting returns every edge in a single response, so a
tool that walks issues individually to find parents has bought an N+1 for nothing.

**Reading it costs a guarantee.** `gh api graphql` accepts a mutation document, so a command that can
read an edge can also write one. A read-only tool either goes without this edge or downgrades its
read-only claim to a promise in prose, as `phil:groom-issues` does.

**GitLab has no stable equivalent to read.** Epics are Premium and the work-item hierarchy that would
carry an issue-to-issue parent is an *Experiment* — see the next section. A cross-forge tool keyed on
parent edges is a GitHub-only check, and should say so rather than reporting the GitLab half clean.

## A parent's "N of M done" counts different things on each forge

Both forges render a completion count on a parent issue, and the two are backed by unrelated
mechanisms. Reading the wrong field returns a real number that counts something else — the
characteristic failure of this whole area, since nothing errors.

**GitHub carries two independent rollups on one issue.** Sub-issues are real issues, so the children
are also cards; the parent's bar comes from `subIssuesSummary`. A markdown task list that references
issues is counted separately, by `trackedIssues`. The two do not fall back to each other.

```sh
gh api graphql -f query='query{ repository(owner:"<o>",name:"<r>"){ issue(number:9){
  subIssuesSummary{ total completed percentCompleted }
  trackedIssues(first:1){ totalCount } } } }'
```

Verified on `gh` 2.97.0, 2026-08-12: a parent with three open sub-issues and no checkboxes in its
body returned `{total: 3, completed: 0, percentCompleted: 0}` alongside `trackedIssues.totalCount: 0`.

**`completed` counts CLOSED children, and closing one is what increments it.** Measured 2026-08-14 on a live
parent: adding an open child gave `{1, 0, 0}`, **closing that child** gave `{1, 1, 100}`, and **removing the
edge** gave `{0, 0, 0}`. Two consequences worth having before you rely on the number:

- **A child closed for any reason counts as completed.** A won't-build close and a shipped close are the same
  value here. Observed on `pmvanev/phil-claude-plugin`: parent #9 reads `3/3 · 100%` while one of its three
  children was deliberately **not** built and closed anyway. The counter is doing what it documents; the
  difference survives only in prose elsewhere.
- **To stop a child counting, remove the edge — closing it does the opposite.** Anything that consolidates
  children into a parent must un-parent before closing, or it renders the parent complete while the work
  continues.
What the issue page renders when *both* counters are non-zero is unverified — check it before relying
on either to be the one displayed.

**GitLab's stable *parent-issue* rollup counts checkboxes, not issues.**

| Mechanism | Field | Children are | Status |
|---|---|---|---|
| Checklist | `taskCompletionStatus {count, completedCount}`; REST `task_completion_status {count, completed_count}` | markdown `- [ ]` in the description | Free, stable — **verified** |
| Child work items | `WorkItemWidgetHierarchy.rolledUpCountsByType` → `countsByState {all, opened, closed}` | real issues and tasks | **Experiment**, added 17.3 — 18.9.1-ee schema only, not run |
| Milestone | `MilestoneStats {closedIssuesCount, totalIssuesCount}` | real issues | Free, stable |

`task_completion_status` needs no widget and no tier, and appeared on every issue observed in the
REST payload — which makes it the one to reach for:

```sh
glab api "projects/<id>/issues/<iid>" | jq .task_completion_status   # {"count":6,"completed_count":1}
```

Verified against an 18.9.1-ee instance by parsing checkboxes out of raw descriptions and comparing:
counts matched on twelve issues, including partials (`1/6`, `2/6`) and complete (`5/5`).

**`WorkItemWidgetProgress` is not this.** Despite the name it carries
`startValue` / `currentValue` / `endValue` / `progress` for OKR key results — a manually set
percentage, not a count of finished children. It answers, and the answer is unrelated.

The asymmetry decides the design: **GitHub's parent rollup counts things that are cards; GitLab's
stable parent rollup counts things that are not.** A GitLab parent whose children must also cross
board columns has no project-scoped, non-experimental count of them.

A milestone is the one GitLab rollup that is both stable and counts real issues, so grouping those
children under one *would* buy the count — but **do not**. The milestone slot is singular and is
spent on the goal (see *A milestone is a goal*, in `references/ordering.md`), and trading the backlog's only durable ordering for
a progress bar is a bad exchange. Accept that GitLab has no reliable feature-level count, and read
the children's live states instead of a summed one.
