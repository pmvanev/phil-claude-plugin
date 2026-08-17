#!/usr/bin/env python3
"""Probe a GitHub forge for the board constants a repo's `CLAUDE.md` must record.

Emits JSON on stdout: every value paired with the exact query that produced it, in a fixed
field order. Nothing here interprets, places, or writes — `skills/board-setup/SKILL.md` owns
that half. This script's only job is to make the values in a generated region provably
un-typed by a human.

Why a script and not prose in the skill: slice 01's AC1 says no value inside the markers was
typed by a human, and KPI-3 says a second run writes zero bytes. Both are properties code can
HOLD. Prose can only ask a model to honour them, and in the finished file a remembered value
is indistinguishable from a probed one — which is the exact failure this feature exists to
close, turned on the feature itself.

Three provenance categories, per feature-delta [D5]:

    probed      the forge returned it
    assumed     the forge returned half of it (see `half_probed`) — NEVER written by slice 01
    declared    only a human can say it (see `not_probeable`) — slice 03 elicits these

A refusal writes nothing. `status: refused` with a `fix` is always better than a partial block:
a block that is silently missing its Status field id reads exactly like one whose board has no
Status field.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

# The ten fields of `phil:issue-board`'s *Per-project setup* template. This list is the
# denominator of KPI-1, so it is the template's shape and not this script's coverage —
# adding a field here because the probe happens to reach it would make the KPI measure itself.
TEMPLATE_FIELDS = [
    "forge-and-repo",
    "project-and-board-ids",
    "tier",
    "status-mechanism",
    "column-families",
    "label-families",
    "builtin-workflows",
    "docs-root",
    "nwave-mapping",
    "local-task-system",
]


class Refusal(Exception):
    """A condition under which no block may be written. Carries the fix, never a default."""

    def __init__(self, reason: str, fix: str | None = None):
        super().__init__(reason)
        self.reason = reason
        self.fix = fix


def run(argv: list[str]) -> str:
    """Run a command and return stdout, or refuse. Never shell=True; no interpolation."""
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        raise Refusal(f"`{argv[0]}` is not installed or not on PATH")
    except subprocess.TimeoutExpired:
        raise Refusal(f"`{' '.join(argv[:2])}` timed out after 60s")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).strip().splitlines()
        detail = err[0] if err else f"exit {proc.returncode}"
        raise Refusal(f"`{' '.join(argv[:3])}` failed: {detail}")
    return proc.stdout


def graphql(query: str) -> dict:
    """Run a GraphQL read and return `data`.

    A transient 503 from the projects API was observed on 2026-08-17 and succeeded on retry,
    so this refuses rather than retries: a probe that quietly retries can mask a forge that is
    genuinely unwell, and the caller is a human who can run the command again.
    """
    out = run(["gh", "api", "graphql", "-f", f"query={query}"])
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        raise Refusal("the forge returned output that is not JSON")
    if payload.get("errors"):
        raise Refusal(f"GraphQL error: {payload['errors'][0].get('message', 'unknown')}")
    if "data" not in payload:
        raise Refusal("the forge returned no `data`")
    return payload["data"]


GIT_URL = re.compile(
    r"^(?:git@(?P<h1>[^:]+):|(?:https?|ssh)://(?:[^@/]+@)?(?P<h2>[^/:]+)(?::\d+)?/)"
    r"(?P<slug>[^\s]+?)(?:\.git)?$"
)


def derive_targets(remote_output: str) -> list[dict]:
    """Turn `git remote -v` output into distinct forge targets, newest-name-first.

    CONFIRM must never *infer* a target — issue `#12` exists in every repo, so an inferred remote
    reads the wrong board successfully. But whether a repo is ambiguous is a fact about its
    remotes, and a fact is testable. So detection lives here and the asking stays with the human:
    this returns the candidates and says nothing about which to pick.

    A fork is the case that matters and the one a single-remote check misses: `origin` plus
    `upstream` are two different repos with two different boards, and the board that matters is
    usually not the one you pushed to.
    """
    seen: dict[tuple[str, str], dict] = {}
    for line in remote_output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        name, url = parts[0], parts[1]
        m = GIT_URL.match(url)
        if not m:
            continue
        host = m.group("h1") or m.group("h2")
        slug = m.group("slug")
        if slug.count("/") != 1:
            continue
        key = (host, slug)
        if key not in seen:
            seen[key] = {"remote": name, "host": host, "repo": slug}
        elif name == "origin":
            seen[key]["remote"] = name
    return list(seen.values())


def require_project_scope() -> None:
    """Slice 01 AC4: a missing `project` scope names the exact fix and writes nothing."""
    if shutil.which("gh") is None:
        raise Refusal("`gh` is not installed", fix="install the GitHub CLI")
    out = run(["gh", "auth", "status"])
    scopes = re.search(r"Token scopes:\s*(.+)", out)
    if not scopes:
        raise Refusal(
            "`gh auth status` reported no token scopes — the board cannot be read",
            fix="gh auth refresh -s project",
        )
    if "'project'" not in scopes.group(1):
        raise Refusal(
            "`gh auth` is missing the `project` scope, so the Status field and its option ids "
            "cannot be read",
            fix="gh auth refresh -s project",
        )


def pick_project(host: str, owner: str, repo: str, facts: list[dict]) -> dict:
    """Resolve the board, preferring the repo link and falling back to the owner's projects.

    On this plugin's own board `repository.projectsV2` is EMPTY — user project 3 is not linked
    to the repository — so the fallback is the path that actually runs, not a safety net. Both
    routes are recorded, because *how* the board was found is itself a constant worth writing:
    a repo with no project link is a repo where `gh project item-add` is the only way a card
    ever reaches the board.
    """
    linked_q = (
        '{ repository(owner:"%s", name:"%s"){ projectsV2(first:20){ nodes '
        "{ id number title url closed } } } }" % (owner, repo)
    )
    linked = graphql(linked_q)["repository"]["projectsV2"]["nodes"]
    open_linked = [p for p in linked if not p["closed"]]
    if len(open_linked) == 1:
        facts.append(
            fact("project-discovery", "linked to the repository", linked_q,
                 "the repository's own project link resolved to exactly one open project")
        )
        return open_linked[0]
    if len(open_linked) > 1:
        raise Refusal(
            f"the repository links {len(open_linked)} open projects "
            f"({', '.join('#%d %s' % (p['number'], p['title']) for p in open_linked)}) — which "
            f"one is the board is a human decision",
            # No fix is offered because none exists yet: there is no flag to name a board, and
            # inventing advice the product cannot honour is worse than admitting the gap.
            fix=None,
        )

    type_q = '{ repositoryOwner(login:"%s"){ __typename } }' % owner
    kind = graphql(type_q)["repositoryOwner"]["__typename"]
    scope = "user" if kind == "User" else "organization"
    owner_q = (
        '{ %s(login:"%s"){ projectsV2(first:50){ totalCount nodes '
        "{ id number title url closed } } } }" % (scope, owner)
    )
    all_owned = graphql(owner_q)[scope]["projectsV2"]["nodes"]
    open_owned = [p for p in all_owned if not p["closed"]]
    if not open_owned:
        raise Refusal(
            f"no open project belongs to {owner} and none is linked to {owner}/{repo} — this "
            f"repo has no board",
            fix="creating one is a decision with a duplicate-board failure mode; out of scope",
        )
    if len(open_owned) > 1:
        raise Refusal(
            f"{owner} owns {len(open_owned)} open projects and none is linked to the repository "
            f"({', '.join('#%d %s' % (p['number'], p['title']) for p in open_owned)}) — which one "
            f"is this repo's board cannot be probed",
            fix=None,  # see above: no flag names a board
        )
    facts.append(
        fact("project-discovery",
             f"NOT linked to the repository; found via the {scope}'s projects",
             f"{linked_q}  # returned [] — then: {owner_q}",
             f"`repository.projectsV2` was empty, so the board was resolved from the {scope}'s "
             f"one open project; a card reaches this board only via an explicit "
             f"`gh project item-add`")
    )
    return open_owned[0]


def fact(field: str, value, query: str, note: str | None = None,
         template_field: str | None = None) -> dict:
    return {
        "field": field,
        "value": value,
        "query": query,
        "provenance": "probed",
        "note": note,
        "template_field": template_field,
    }


def probe(host: str, slug: str) -> dict:
    owner, repo = slug.split("/", 1)
    facts: list[dict] = []

    require_project_scope()

    # --- forge and repo -------------------------------------------------------------------
    # `gh repo view` takes the target POSITIONALLY; it has no `-R`, unlike `gh issue` and
    # `gh api`. Passing -R here failed loudly on 2026-08-17 rather than writing a partial block.
    repo_q = f"gh repo view {slug} --json nameWithOwner,defaultBranchRef,isFork,isPrivate"
    meta = json.loads(run(
        ["gh", "repo", "view", slug, "--json",
         "nameWithOwner,defaultBranchRef,isFork,isPrivate"]
    ))
    default_branch = (meta.get("defaultBranchRef") or {}).get("name")
    if not default_branch:
        raise Refusal(f"{slug} has no default branch — the docs root cannot be derived")
    facts.append(fact(
        "forge-and-repo",
        f"GitHub at {host} — use `gh -R {meta['nameWithOwner']}` on every call",
        repo_q,
        "issue #12 exists in every repo, so an inferred remote mutates the wrong one successfully",
        template_field="forge-and-repo",
    ))
    facts.append(fact("default-branch", default_branch, repo_q))
    if meta.get("isFork"):
        facts.append(fact("fork", True, repo_q,
                          "a fork's board may belong to the upstream; confirm the target"))

    # --- tier ----------------------------------------------------------------------------
    # C6: absent is not benign. GitLab's Premium/Free split gates scoped labels and real
    # `blocks` links; GitHub gates neither, so the honest value is `not applicable` and never
    # a plausible default. This mirrors S6 AC4 in the opposite direction.
    facts.append(fact(
        "tier",
        "not applicable on GitHub",
        repo_q,
        "the tier bullet exists because GitLab gates scoped labels and `blocks` links behind "
        "Premium; GitHub gates neither, so no tier-dependent convention applies here",
        template_field="tier",
    ))

    # --- the board -----------------------------------------------------------------------
    project = pick_project(host, owner, repo, facts)
    number = project["number"]
    facts.append(fact(
        "project-and-board-ids",
        {"id": project["id"], "number": number, "title": project["title"],
         "url": project["url"]},
        "(see project-discovery)",
        template_field="project-and-board-ids",
    ))

    # --- status field and options --------------------------------------------------------
    owner_kind = graphql('{ repositoryOwner(login:"%s"){ __typename } }' % owner)
    scope = "user" if owner_kind["repositoryOwner"]["__typename"] == "User" else "organization"
    fields_q = (
        '{ %s(login:"%s"){ projectV2(number:%d){ fields(first:50){ nodes { __typename '
        "... on ProjectV2SingleSelectField { id name options { id name } } "
        "... on ProjectV2Field { id name dataType } } } } } }" % (scope, owner, number)
    )
    nodes = graphql(fields_q)[scope]["projectV2"]["fields"]["nodes"]
    single_selects = [n for n in nodes if n.get("__typename") == "ProjectV2SingleSelectField"]
    status = next((n for n in single_selects if n["name"] == "Status"), None)
    if status is None:
        raise Refusal(
            "this project has no single-select field named `Status` — every status write in "
            "`phil:issue-board` addresses one by id, and guessing which field is the status "
            "field would move cards in a column nobody chose"
        )
    facts.append(fact(
        "status-mechanism",
        f"a project single-select FIELD named `Status` (id {status['id']}), not a label",
        fields_q,
        "an issue must be `gh project item-add`ed before any field can be set; editing one "
        "that was never added does nothing",
        template_field="status-mechanism",
    ))
    facts.append(fact(
        "column-families",
        {"field_id": status["id"],
         "option_count": len(status["options"]),
         "options": [{"name": o["name"], "id": o["id"]} for o in status["options"]]},
        fields_q,
        f"`updateProjectV2Field`'s `singleSelectOptions` is a FULL REPLACEMENT — omitting any "
        f"of these {len(status['options'])} ids drops that option and every card's assignment "
        f"to it, with a call that reports success",
        template_field="column-families",
    ))
    others = [n["name"] for n in single_selects if n["name"] != "Status"]
    if others:
        facts.append(fact("other-single-select-fields", others, fields_q,
                          "one board's status field holds one enum; a second family sharing it "
                          "makes every card sort against all of them"))

    # --- views ---------------------------------------------------------------------------
    views_q = ('{ %s(login:"%s"){ projectV2(number:%d){ views(first:20){ nodes '
               "{ number name layout } } } } }" % (scope, owner, number))
    views = graphql(views_q)[scope]["projectV2"]["views"]["nodes"]
    boards = [v for v in views if v["layout"] == "BOARD_LAYOUT"]
    facts.append(fact(
        "board-view",
        [{"number": v["number"], "name": v["name"], "url":
          f"https://{host}/{'users' if scope == 'user' else 'orgs'}/{owner}/projects/{number}"
          f"/views/{v['number']}"} for v in boards] or "none — this project has no board view",
        views_q,
        "the LAYOUT is probed; which view a human calls `the kanban` is not",
    ))

    # --- built-in workflows --------------------------------------------------------------
    wf_q = ('{ %s(login:"%s"){ projectV2(number:%d){ workflows(first:50){ nodes '
            "{ name enabled } } } } }" % (scope, owner, number))
    workflows = graphql(wf_q)[scope]["projectV2"]["workflows"]["nodes"]
    enabled = [w["name"] for w in workflows if w["enabled"]]
    facts.append(fact(
        "builtin-workflows",
        {"enabled": enabled,
         "disabled": [w["name"] for w in workflows if not w["enabled"]]},
        wf_q,
        "a status write is also an issue write when one of these is on, and the reverse",
        template_field="builtin-workflows",
    ))

    # --- docs root -----------------------------------------------------------------------
    facts.append(fact(
        "docs-root",
        f"https://{host}/{slug}/blob/{default_branch}/",
        repo_q,
        "GitHub emits relative paths verbatim in issue bodies and they 404",
        template_field="docs-root",
    ))

    # --- nWave-ness ----------------------------------------------------------------------
    tracked = run(["git", "ls-tree", "-d", "--name-only", "HEAD", "docs/feature", ".nwave"])
    present = [p for p in tracked.split() if p]
    facts.append(fact(
        "nwave-mapping",
        (f"nWave repo — {', '.join(present)} present; see `phil:nwave-issue-board` for the "
         f"artifact to issue mapping" if present else
         "not an nWave repo — neither `docs/feature/` nor `.nwave/` is tracked"),
        "git ls-tree -d --name-only HEAD docs/feature .nwave",
        template_field="nwave-mapping",
    ))

    # --- half probed: written by NOBODY in slice 01 --------------------------------------
    half: list[dict] = []
    for name in ("Auto-close issue", "Item closed"):
        if name in enabled:
            half.append({
                "field": "workflow-trigger-status",
                "known": f"`{name}` is enabled on this project",
                "unknown": "which Status option fires it",
                "why": "`ProjectV2Workflow` exposes createdAt, enabled, fullDatabaseId, id, "
                       "name, number, project, updatedAt — and no field for the configured "
                       "trigger statuses",
                "query": wf_q,
                "assumption_slice_04_would_write": "Done",
            })

    # --- not probeable at all ------------------------------------------------------------
    not_probeable = [
        {
            "field": "label-families",
            "template_field": "label-families",
            "why": "nothing on a forge records whether a family is single- or multi-valued. The "
                   "labels in use are evidence, never the answer — inferring one would make the "
                   "board's habits audit themselves and mint the very declaration "
                   "`phil:groom-issues` rule 4 exists to read",
            "owner": "slice 03",
        },
        {
            "field": "local-task-system",
            "template_field": "local-task-system",
            "why": "whether a local task file owns in-flight work is a working preference, not a "
                   "forge fact",
            "owner": "slice 03",
        },
    ]

    covered = {f["template_field"] for f in facts if f["template_field"]}
    return {
        "schema": "board-setup-probe/v1",
        "probe_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "host": host,
        "repo": slug,
        "status": "ok",
        "facts": facts,
        "half_probed": half,
        "not_probeable": not_probeable,
        "kpi_1": {
            "template_fields": len(TEMPLATE_FIELDS),
            "populated_without_human_input": len(covered),
            "fraction": round(len(covered) / len(TEMPLATE_FIELDS), 2),
            "target": 0.5,
            "covered": sorted(covered),
            "uncovered": sorted(set(TEMPLATE_FIELDS) - covered),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Probe a GitHub board for the constants a repo's CLAUDE.md must record.")
    ap.add_argument("--repo", metavar="OWNER/REPO",
                    help="the forge target, CONFIRMED with the human before this runs")
    ap.add_argument("--host", default="github.com")
    ap.add_argument("--list-targets", action="store_true",
                    help="enumerate candidate forge targets from the git remotes and exit; makes "
                         "no forge call. Run this at CONFIRM, before --repo is known.")
    args = ap.parse_args()

    if args.list_targets:
        try:
            targets = derive_targets(run(["git", "remote", "-v"]))
        except Refusal as r:
            print(json.dumps({"schema": "board-setup-targets/v1", "status": "refused",
                              "refusal": {"reason": r.reason, "fix": r.fix}}, indent=2))
            return 1
        print(json.dumps({
            "schema": "board-setup-targets/v1",
            "status": "ok" if len(targets) == 1 else "ambiguous" if targets else "none",
            "targets": targets,
            # An explicit instruction, because the dangerous branch is the one that looks fine:
            # a fork yields two plausible targets and picking either silently is the failure.
            "confirm_required": True,
            "note": ("exactly one candidate — still confirm it with the human before any call"
                     if len(targets) == 1 else
                     "more than one candidate: ASK which board, never pick" if targets else
                     "no parseable git remote — ask for the target"),
        }, indent=2))
        return 0

    if not args.repo:
        print(json.dumps({"status": "refused", "schema": "board-setup-probe/v1",
                          "refusal": {"reason": "--repo is required unless --list-targets is given",
                                      "fix": None}}, indent=2))
        return 2
    if "/" not in args.repo:
        print(json.dumps({"status": "refused", "schema": "board-setup-probe/v1",
                          "refusal": {"reason": "--repo must be OWNER/REPO", "fix": None}},
                         indent=2))
        return 2
    try:
        print(json.dumps(probe(args.host, args.repo), indent=2))
        return 0
    except Refusal as r:
        print(json.dumps({
            "schema": "board-setup-probe/v1",
            "status": "refused",
            "host": args.host,
            "repo": args.repo,
            "refusal": {"reason": r.reason, "fix": r.fix},
        }, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
