#!/usr/bin/env python3
"""Probe a GitHub or GitLab forge for the board constants a repo's `CLAUDE.md` must record.

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
    assumed     the forge returned half of it, or it is derived from a proxy. Written inside the
                markers, labelled, stating what is not knowable and why
    declared    only a human can say it (see `not_probeable`). Written in a SEPARATE region,
                attributed, and never regenerated
    unread      the forge would not answer. Neither a fact nor a guess, so it is reported and
                never written inside the markers at all

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
        # Take the first line carrying actual information. `glab` prints a bare "ERROR" banner line
        # before the real message, and a refusal whose reason reads `failed: ERROR` tells the reader
        # nothing they did not already know — the point of a refusal is its reason.
        lines = [l.strip() for l in (proc.stderr + "\n" + proc.stdout).splitlines() if l.strip()]
        informative = [l for l in lines if l.strip(" :").upper() not in ("ERROR", "ERR", "FATAL")]
        detail = informative[0] if informative else (lines[0] if lines else f"exit {proc.returncode}")
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


def derive_label_evidence(issues: list[dict]) -> dict:
    """Gather what a human needs to answer the label-family question, and **no answer**.

    Slice 03 exists to make one thing impossible: inferring whether a family is single- or
    multi-valued from the labels in use ([D6]). Nothing on a forge records it, so inferring it makes
    the board's habits audit themselves and mints the very declaration `phil:groom-issues` rule 4
    exists to read.

    So this returns counts, co-occurrence and the issue numbers that carry more than one — and never
    a verdict, a default, a preselection or a confidence. Two groupings, and the distinction is
    load-bearing:

    - **syntactic prefix** — `wave: discuss` and `status::doing` group under `wave` and `status`
      because the label's *name* says so. That is a fact about the string, not a claim about
      behaviour.
    - **candidate grouping, unconfirmed** — unprefixed labels cannot be grouped syntactically, so
      the grouping itself is part of the question rather than an input to it.

    A family whose labels never co-occur is reported with an empty `issues_with_multiple` rather
    than dropped. Absence of co-occurrence is evidence *for* single-valued and it is the human's to
    weigh; dropping the family would answer the question by omission.
    """
    counts: dict[str, int] = {}
    for issue in issues:
        for label in issue.get("labels", []):
            counts[label] = counts.get(label, 0) + 1

    def prefix_of(label: str) -> str | None:
        for sep in ("::", ":"):
            if sep in label:
                head = label.split(sep, 1)[0].strip()
                if head:
                    return head
        return None

    groups: dict[str, dict] = {}
    for label in sorted(counts):
        p = prefix_of(label)
        key = p if p else "(unprefixed)"
        grouping = "syntactic prefix" if p else "candidate grouping, unconfirmed"
        groups.setdefault(key, {"name": key, "members": [], "grouping": grouping})
        groups[key]["members"].append(label)

    families = []
    for key, g in groups.items():
        members = set(g["members"])
        co: dict[tuple[str, str], int] = {}
        multiple = []
        for issue in issues:
            present = sorted(members & set(issue.get("labels", [])))
            if len(present) > 1:
                multiple.append(issue["number"])
                for i, a in enumerate(present):
                    for b in present[i + 1:]:
                        co[(a, b)] = co.get((a, b), 0) + 1
        families.append({
            "name": key,
            "members": g["members"],
            "grouping": g["grouping"],
            "counts": {m: counts[m] for m in g["members"]},
            # A list of pairs, not a dict keyed by one: a tuple key is not JSON-serialisable, and
            # this payload exists to be serialised.
            "co_occurrence": [{"pair": list(pair), "count": n}
                              for pair, n in sorted(co.items(), key=lambda kv: (-kv[1], kv[0]))],
            "issues_with_multiple": multiple,
        })

    return {
        "families": families,
        # Stated in the payload, not only in this docstring, because the payload is what a later
        # reader sees. A consumer that treats co-occurrence as an answer has misread it.
        "note": ("evidence only — this holds NO answer. Whether a family is single- or multi-valued "
                 "is never recorded by a forge and must never be inferred from these counts. "
                 "Co-occurrence is evidence to show beneath a question, never the answer to it."),
    }


# --- slice 06: GitLab ---------------------------------------------------------------------
#
# Same region shape, different calls. The shape is the hypothesis: if GitLab needed different
# sections or a different provenance model, one command serving both forges would be the wrong unit
# and the honest answer would be two commands.
#
# `phil:issue-board` owns these call spellings. Two of them punish a wrong guess silently:
# The JSON flag differs per subcommand — see `gitlab_calls` — and a GitLab docs root is
# `/-/blob/<branch>/` rather than GitHub's `/blob/<branch>/`.

CONNECTION_WORDS = ("could not connect", "connection refused", "timeout", "timed out",
                    "temporary failure in name resolution", "network is unreachable")


def with_retry(call, attempts_allowed: int = 3):
    """Retry a *connectivity* failure; never retry anything else.

    Slice 06 AC5: a single failure is usually the network, and concluding "no board" from one timeout
    against a self-hosted instance records a wrong answer permanently. But a 401 is not flaky —
    retrying it three times only delays the real answer, so the retry is scoped to failures whose
    reason reads like connectivity.
    """
    last = None
    for attempt in range(attempts_allowed):
        try:
            return call()
        except Refusal as r:
            last = r
            if not any(w in r.reason.lower() for w in CONNECTION_WORDS):
                raise
    raise Refusal(f"{last.reason} — after {attempts_allowed} attempts",
                  fix="check network reachability and any certificate caveat for a self-hosted "
                      "instance before concluding anything about the board")


def gitlab_docs_root(host_url: str, slug: str, default_branch: str) -> str:
    """GitLab's blob path carries a `/-/` segment GitHub's does not.

    Getting this wrong produces links that 404, which is precisely the failure the `docs-root` fact
    exists to prevent.
    """
    return f"{host_url.rstrip('/')}/{slug}/-/blob/{default_branch}/"


def gitlab_calls(slug: str) -> list[str]:
    """The calls this adapter makes, as strings, so the region can name each one.

    **The JSON flag differs per subcommand, and the blanket rule is wrong.** Verified 2026-08-17
    against `glab --help` output, after `glab api … -O json` failed with
    `Unknown shorthand flag: 'O' in -O`:

    - `glab api` — takes **no** output flag. It prints JSON natively.
    - `glab repo view` — the flag is **`-F`/`--output`** (`text`, `json`). `-O` does not exist here.
    - `glab issue list` — the flag is **`-O`/`--output`**. `-F` here is `--output-format`, a
      different flag taking `details`/`ids`/`urls`.

    `phil:issue-board` records "glab's JSON flag is `-O`; `-F` fails silently" as a blanket rule.
    That holds for `issue list` and is wrong for the other two — exactly the remembered-constant
    failure this whole feature exists to prevent, sitting inside this plugin's own skill.
    """
    encoded = slug.replace("/", "%2F")
    return [
        f"glab repo view {slug} -F json",
        f"glab api projects/{encoded}",
        f"glab api projects/{encoded}/labels",
        f"glab issue list -R {slug} --all -O json",
    ]


def gitlab_facts(host: str, slug: str, default_branch: str, tier: str,
                 labels: list[str] | None, project_id) -> list[dict]:
    """The same `template_field` set GitHub produces, with GitLab's values and calls.

    Two things are deliberately *not* defaults:

    - **Projects v2 workflows render as `not applicable on this forge`**, never `none enabled`
      (AC4/C6). GitLab has no Projects-v2 workflow system to be empty, and "none enabled" is a false
      statement about a mechanism that does not exist.
    - **A Free instance gets a Free-shaped block.** Scoped labels and real `blocks` links are gated
      behind Premium, so writing a scoped-label convention on Free documents a workflow the reader
      cannot perform.
    """
    host_url = f"https://{host}"
    repo_q, proj_q, labels_q, _issues_q = gitlab_calls(slug)

    # `labels=None` means UNREAD, and it is not the same as `labels=[]`. On GitLab the label set *is*
    # the board, so rendering an unread set as `count: 0` states that the project has no columns —
    # the single most misleading thing this fact can say. Found against a real project, where
    # `projects/X` reads unauthenticated but `projects/X/labels` returns 401.
    labels_unread = labels is None
    scoped = None if labels_unread else sorted(
        l for l in labels if "::" in l and l.split("::", 1)[0] == "status")

    tier_value = (
        f"{tier} — scoped labels and real `blocks` links are Premium features. Board state is a "
        f"`status::` label, swapped by hand: `glab issue update --unlabel old --label new`."
        if tier == "Free" else
        f"{tier} — scoped labels enforce single-valuedness natively and real `blocks` links are "
        f"available."
    )

    return [
        fact("forge-and-repo", f"GitLab at {host} — use `glab -R {slug}` on every call", repo_q,
             note="`glab`'s JSON flag differs per subcommand: `glab api` takes none, `glab repo "
                  "view` uses `-F json`, `glab issue list` uses `-O json`. On `issue list`, `-F` is "
                  "`--output-format` and silently returns a table",
             template_field="forge-and-repo"),
        fact("project-and-board-ids", {"id": project_id, "slug": slug,
                                       "url": f"{host_url}/{slug}"}, proj_q,
             template_field="project-and-board-ids"),
        fact("status-mechanism",
             "a `status::` scoped LABEL, not a project field — GitLab has no Projects v2 Status "
             "field", labels_q,
             note="on Free the scope is a naming convention only; nothing stops two `status::` "
                  "labels coexisting, so the swap must be explicit",
             template_field="status-mechanism"),
        fact("column-families",
             ({"mechanism": "status:: labels", "labels": None, "count": None,
               "unread": "the labels endpoint could not be read — this is NOT a project with no "
                         "status:: labels, and must never be reported as one"}
              if labels_unread else
              {"mechanism": "status:: labels", "labels": scoped, "count": len(scoped)}),
             labels_q,
             provenance="unread" if labels_unread else "probed",
             template_field="column-families"),
        fact("builtin-workflows", "not applicable on this forge — GitLab has no Projects v2 "
                                  "workflow system, so there is none to enumerate and none to "
                                  "report as disabled", proj_q,
             template_field="builtin-workflows"),
        fact("tier", tier_value, proj_q, provenance="assumed",
             note="not knowable directly: the REST API returns no tier field, so this is inferred "
                  "from `issues_enabled` and `iterations_access_level`. Confirm it against the "
                  "instance's plan before relying on a Premium-only convention",
             template_field="tier"),
        fact("docs-root", gitlab_docs_root(host_url, slug, default_branch), repo_q,
             note="GitLab blob paths carry a `/-/` segment; GitHub's do not",
             template_field="docs-root"),
        fact("nwave-mapping", "see `phil:nwave-issue-board` for the artifact to issue mapping",
             "git ls-tree -d --name-only HEAD docs/feature .nwave",
             template_field="nwave-mapping"),
    ]


def probe_gitlab(host: str, slug: str) -> dict:
    """Probe a GitLab project. Same region shape as GitHub, different calls.

    **The live path is unexercised.** `glab auth status` returned 401 in the environment where this
    was authored and no GitLab project was available, so `gitlab_facts` and every refusal are unit
    tested against faked output while the end-to-end run is not. Slice 06's brief records which of
    its acceptance criteria remain open, and this docstring says so here because a reader of the code
    should not have to find the brief to learn it.

    A GitLab repo is refused rather than half-served, per the slice boundary: a partial block reads
    exactly like a complete one.
    """
    if shutil.which("glab") is None:
        raise Refusal("`glab` is not installed or not on PATH",
                      fix="install glab, or pass a GitHub target instead")

    repo_q, proj_q, labels_q, issues_q = gitlab_calls(slug)

    def api(path: str) -> dict:
        # `glab api` takes NO output flag — it prints JSON natively, and `-O json` is rejected with
        # `Unknown shorthand flag: 'O' in -O`.
        out = with_retry(lambda: run(["glab", "api", path]))
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            raise Refusal("glab api returned output that is not JSON",
                          fix="`glab api` needs no output flag; check the endpoint path")

    project = api(f"projects/{slug.replace('/', '%2F')}")
    labels_raw = api(f"projects/{slug.replace('/', '%2F')}/labels")

    # `None`, never `[]`. An unreadable label list is not an empty one, and on GitLab that
    # distinction is the difference between "this board has no columns" and "nobody could look".
    labels = ([l.get("name") for l in labels_raw if isinstance(l, dict) and l.get("name")]
              if isinstance(labels_raw, list) else None)
    default_branch = project.get("default_branch") or "main"

    # Tier is probed, never assumed. `phil:issue-board` owns the check; a scoped-label convention
    # written on a Free instance documents a workflow the reader cannot perform.
    tier = "Premium" if project.get("issues_enabled") and project.get("iterations_access_level") \
        not in (None, "disabled") else "Free"

    facts = gitlab_facts(host=host, slug=slug, default_branch=default_branch, tier=tier,
                         labels=labels, project_id=project.get("id"))

    # `-O json` here, and NOT `-F`: on `issue list`, `-F` is `--output-format` taking
    # details/ids/urls, so `-F json` would be a different flag with an invalid value.
    issues_raw = with_retry(lambda: run(
        ["glab", "issue", "list", "-R", slug, "--all", "-O", "json"]))
    try:
        issues = [{"number": i.get("iid"), "labels": i.get("labels", [])}
                  for i in json.loads(issues_raw)]
        evidence = derive_label_evidence(issues)
        evidence["query"] = issues_q
        evidence["issues_read"] = len(issues)
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        evidence = {"families": None, "issues_read": None,
                    "unread": f"could not read the project's labels: {e}",
                    "note": "evidence UNREAD — not the same as a project with no labels"}

    covered = {f["template_field"] for f in facts if f["template_field"]}
    return {
        "schema": "board-setup-probe/v1",
        "forge": "gitlab",
        "probe_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "host": host,
        "repo": slug,
        "status": "ok",
        "live_path_unexercised": ("authored against a 401 `glab auth`; gitlab_facts and the refusals "
                                 "are unit tested, the end-to-end run is not"),
        "elicitation_evidence": evidence,
        "facts": facts,
        "half_probed": [],
        "not_probeable": [
            {"field": "label-families", "template_field": "label-families",
             "why": "nothing on a forge records whether a family is single- or multi-valued",
             "owner": "slice 03"},
            {"field": "local-task-system", "template_field": "local-task-system",
             "why": "a working preference, not a forge fact", "owner": "slice 03"},
        ],
        "kpi_1": {
            "template_fields": len(TEMPLATE_FIELDS),
            "populated_without_human_input": len(covered),
            "fraction": round(len(covered) / len(TEMPLATE_FIELDS), 2),
            "target": 0.5,
            "covered": sorted(covered),
            "uncovered": sorted(set(TEMPLATE_FIELDS) - covered),
        },
    }


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
         template_field: str | None = None, provenance: str = "probed") -> dict:
    """One fact, paired with the exact call that produced it.

    `provenance` defaults to `probed` because that is what a fact normally is, but it is a parameter
    rather than a constant: `unread` exists so a value the forge would not return is never spelled
    the same way as one it returned as empty. The renderer refuses to write anything not labelled
    `probed` or `assumed` inside the markers.
    """
    return {
        "field": field,
        "value": value,
        "query": query,
        "provenance": provenance,
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
                "assumed_value": "Done",
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

    # --- slice 03: evidence for the questions no forge answers ---------------------------
    # Fetched here rather than in a second script because it is the same board, read once. It is
    # deliberately NOT a fact: facts go inside the markers, and this goes beneath a question.
    labels_q = (f"gh issue list -R {slug} --state all --limit 200 --json number,labels")
    try:
        raw = json.loads(run(labels_q.split()))
        issues = [{"number": i["number"], "labels": [l["name"] for l in i.get("labels", [])]}
                  for i in raw]
        evidence = derive_label_evidence(issues)
        evidence["query"] = labels_q
        evidence["issues_read"] = len(issues)
    except (Refusal, json.JSONDecodeError, KeyError) as e:
        # A failed evidence read must never render as "no families found" — that is an answer, and
        # the one answer this must never give. C6: absence is reported as unread, not as empty.
        evidence = {"families": None, "query": labels_q, "issues_read": None,
                    "unread": f"could not read the board's labels: {e}",
                    "note": "evidence UNREAD — this is not the same as a board with no labels, and "
                            "must not be reported as though no family exists"}

    covered = {f["template_field"] for f in facts if f["template_field"]}
    return {
        "elicitation_evidence": evidence,
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
    ap.add_argument("--forge", choices=("github", "gitlab"), default=None,
                    help="the forge to probe. Inferred from --host when omitted; a GitLab host "
                         "with --forge github (or the reverse) is refused rather than half-served.")
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
    inferred = "gitlab" if "gitlab" in args.host else "github"
    if args.forge and args.forge != inferred:
        # Promised by --forge's help text and never implemented: the mismatch probed the wrong forge
        # and reported `status: ok`. A wrong forge reads a wrong board successfully, which is the
        # failure mode this whole command exists to close.
        print(json.dumps({"schema": "board-setup-probe/v1", "status": "refused",
                          "refusal": {"reason": f"--forge {args.forge} contradicts --host "
                                                f"{args.host}, which implies {inferred}",
                                      "fix": "pass a --host matching the forge, or drop --forge "
                                             "and let the host decide"}}, indent=2))
        return 1
    forge = args.forge or inferred
    if forge == "gitlab":
        try:
            print(json.dumps(probe_gitlab(args.host, args.repo), indent=2))
        except Refusal as r:
            print(json.dumps({"schema": "board-setup-probe/v1", "status": "refused",
                              "forge": "gitlab",
                              "refusal": {"reason": r.reason, "fix": r.fix}}, indent=2))
            return 1
        return 0

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
