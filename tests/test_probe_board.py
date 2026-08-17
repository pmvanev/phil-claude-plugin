"""Tests for `scripts/probe-board.py` — the refusal paths and the board-resolution fallback.

Why these and not a live probe: slice 01's AC4 says a missing `project` scope must produce the
exact fix and write nothing, and the only other way to verify that is to strip the scope from the
operator's real `gh` auth. AC3's two-remote case and the ambiguous-project case are the same
shape — conditions that must refuse, reachable only by faking the forge's answer.

The forge itself is never faked for the *values*: slice 01 runs against the real board by
[D7]/WS-strategy-C. What is faked here is only the shape of a failure.
"""

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "probe-board.py"


def load():
    """Import a module whose filename contains a hyphen."""
    spec = importlib.util.spec_from_file_location("probe_board", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pb = load()


# --- the scope gate (AC4) ----------------------------------------------------------------

def test_missing_project_scope_refuses_with_the_exact_fix(monkeypatch):
    monkeypatch.setattr(pb.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(pb, "run", lambda _: "  - Token scopes: 'gist', 'read:org', 'repo'\n")
    with pytest.raises(pb.Refusal) as e:
        pb.require_project_scope()
    assert e.value.fix == "gh auth refresh -s project"
    assert "project" in e.value.reason


def test_present_project_scope_passes(monkeypatch):
    monkeypatch.setattr(pb.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(pb, "run", lambda _: "  - Token scopes: 'project', 'repo'\n")
    pb.require_project_scope()  # must not raise


def test_unparseable_auth_output_refuses_rather_than_assuming_the_scope(monkeypatch):
    """C6: absent is not benign. No scopes line means unknown, never 'probably fine'."""
    monkeypatch.setattr(pb.shutil, "which", lambda _: "/usr/bin/gh")
    monkeypatch.setattr(pb, "run", lambda _: "not logged in\n")
    with pytest.raises(pb.Refusal) as e:
        pb.require_project_scope()
    assert e.value.fix == "gh auth refresh -s project"


def test_missing_gh_refuses(monkeypatch):
    monkeypatch.setattr(pb.shutil, "which", lambda _: None)
    with pytest.raises(pb.Refusal):
        pb.require_project_scope()


# --- graphql error handling --------------------------------------------------------------

def test_graphql_errors_refuse(monkeypatch):
    monkeypatch.setattr(pb, "run", lambda _: json.dumps({"errors": [{"message": "boom"}]}))
    with pytest.raises(pb.Refusal, match="boom"):
        pb.graphql("{ x }")


def test_graphql_non_json_refuses(monkeypatch):
    monkeypatch.setattr(pb, "run", lambda _: "<html>503</html>")
    with pytest.raises(pb.Refusal, match="not JSON"):
        pb.graphql("{ x }")


def test_graphql_missing_data_refuses(monkeypatch):
    monkeypatch.setattr(pb, "run", lambda _: json.dumps({"extensions": {}}))
    with pytest.raises(pb.Refusal, match="no `data`"):
        pb.graphql("{ x }")


# --- board resolution --------------------------------------------------------------------

def project(number, title, closed=False):
    return {"id": f"PVT_{number}", "number": number, "title": title,
            "url": f"https://x/{number}", "closed": closed}


def fake_graphql(monkeypatch, linked, owned=None, kind="User"):
    """Route the three queries pick_project can issue by their distinguishing substring."""
    def _g(query):
        if "repositoryOwner" in query:
            return {"repositoryOwner": {"__typename": kind}}
        if "repository(owner" in query:
            return {"repository": {"projectsV2": {"nodes": linked}}}
        scope = "user" if kind == "User" else "organization"
        return {scope: {"projectsV2": {"totalCount": len(owned or []), "nodes": owned or []}}}
    monkeypatch.setattr(pb, "graphql", _g)


def test_single_linked_project_is_used_and_the_route_is_recorded(monkeypatch):
    fake_graphql(monkeypatch, linked=[project(7, "board")])
    facts = []
    got = pb.pick_project("github.com", "o", "r", facts)
    assert got["number"] == 7
    assert facts[0]["field"] == "project-discovery"
    assert "linked to the repository" in facts[0]["value"]


def test_empty_repo_link_falls_back_to_the_owner_and_says_so(monkeypatch):
    """This repo's real case: repository.projectsV2 is [] while user project 3 is the board."""
    fake_graphql(monkeypatch, linked=[], owned=[project(3, "phil plugin"), project(1, "old", True)])
    facts = []
    got = pb.pick_project("github.com", "pmvanev", "phil-claude-plugin", facts)
    assert got["number"] == 3
    assert "NOT linked to the repository" in facts[0]["value"]
    assert "gh project item-add" in facts[0]["note"]


def test_closed_projects_are_not_candidates(monkeypatch):
    fake_graphql(monkeypatch, linked=[], owned=[project(1, "old", True)])
    with pytest.raises(pb.Refusal, match="no board"):
        pb.pick_project("github.com", "o", "r", [])


def test_two_open_owner_projects_refuse_rather_than_guess(monkeypatch):
    fake_graphql(monkeypatch, linked=[], owned=[project(3, "a"), project(4, "b")])
    with pytest.raises(pb.Refusal) as e:
        pb.pick_project("github.com", "o", "r", [])
    assert "cannot be probed" in e.value.reason
    # No fix, deliberately: there is no flag that names a board, so any advice here would be
    # advice the product cannot honour. `fix` is nullable precisely so this case can say nothing.
    assert e.value.fix is None


def test_two_linked_projects_refuse_rather_than_guess(monkeypatch):
    fake_graphql(monkeypatch, linked=[project(3, "a"), project(4, "b")])
    with pytest.raises(pb.Refusal, match="human decision"):
        pb.pick_project("github.com", "o", "r", [])


def test_organization_owner_uses_the_organization_scope(monkeypatch):
    fake_graphql(monkeypatch, linked=[], owned=[project(9, "org board")], kind="Organization")
    facts = []
    assert pb.pick_project("github.com", "o", "r", facts)["number"] == 9
    assert "organization's projects" in facts[0]["value"]


# --- CONFIRM: target derivation (AC3's detection half) -----------------------------------

FETCH_PUSH = "{n}\t{u} (fetch)\n{n}\t{u} (push)\n"


def remotes(*pairs):
    return "".join(FETCH_PUSH.format(n=n, u=u) for n, u in pairs)


def test_one_remote_yields_one_target():
    t = pb.derive_targets(remotes(("origin", "git@github.com:pmvanev/phil-claude-plugin.git")))
    assert t == [{"remote": "origin", "host": "github.com", "repo": "pmvanev/phil-claude-plugin"}]


def test_fetch_and_push_of_the_same_url_is_one_target_not_two():
    """The dangerous false positive: every remote prints twice, so naive counting says 'ambiguous'
    for every repo on earth and the question stops meaning anything."""
    assert len(pb.derive_targets(remotes(("origin", "git@github.com:o/r.git")))) == 1


def test_a_fork_yields_two_targets(monkeypatch):
    """AC3's real case. origin and upstream are different repos with different boards, and the
    board that matters is usually not the one you pushed to."""
    t = pb.derive_targets(remotes(
        ("origin", "git@github.com:pmvanev/phil-claude-plugin.git"),
        ("upstream", "https://github.com/someone-else/phil-claude-plugin.git"),
    ))
    assert len(t) == 2
    assert {x["repo"] for x in t} == {"pmvanev/phil-claude-plugin",
                                      "someone-else/phil-claude-plugin"}


def test_two_unrelated_remotes_yield_two_targets():
    t = pb.derive_targets(remotes(("origin", "git@github.com:a/one.git"),
                                  ("mirror", "git@gitlab.com:b/two.git")))
    assert len(t) == 2
    assert {x["host"] for x in t} == {"github.com", "gitlab.com"}


def test_https_and_ssh_spellings_of_one_repo_collapse_to_one_target():
    t = pb.derive_targets(remotes(("origin", "git@github.com:o/r.git"),
                                  ("https", "https://github.com/o/r.git")))
    assert len(t) == 1


def test_no_remotes_yields_no_targets():
    assert pb.derive_targets("") == []


def test_unparseable_and_deep_paths_are_skipped_not_guessed():
    """A GitLab subgroup path is not OWNER/REPO; emitting it as a target would send `gh -R` at a
    slug it cannot address. Skipped, so the human is asked instead."""
    assert pb.derive_targets(remotes(("weird", "file:///srv/git/repo.git"))) == []
    assert pb.derive_targets(remotes(("sub", "git@gitlab.com:group/sub/proj.git"))) == []


# --- KPI-1's denominator is the template, not the probe's reach --------------------------

def test_kpi1_denominator_is_the_ten_template_fields():
    assert len(pb.TEMPLATE_FIELDS) == 10
    assert "label-families" in pb.TEMPLATE_FIELDS
    assert "local-task-system" in pb.TEMPLATE_FIELDS
