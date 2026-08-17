"""Tests for slice 06's GitLab adapter in `scripts/probe-board.py`.

**These are unit tests against faked `glab` output, and that is a stated limitation rather than a
choice.** The brief says "No synthetic data: a real GitLab project", and slice 06's hypothesis —
that the region's *shape* survives a change of forge — is properly tested by diffing a real
GitLab-generated region against a real GitHub one. `glab auth status` returns 401 here and there is
no GitLab project on disk, so that diff has not been run. The slice brief records which ACs remain
open.

What these DO pin is everything that does not need a live instance: the call spellings (where a
wrong flag fails silently), the shape-equality property, and the two refusals whose whole purpose is
to not report a benign default.
"""

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "probe-board.py"


def load():
    spec = importlib.util.spec_from_file_location("probe_board", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pb = load()


# --- the call spellings, where a wrong flag fails SILENTLY ---------------------------------

def test_the_json_flag_is_correct_per_subcommand_not_blanket():
    """`phil:issue-board` records a blanket rule — *"glab's JSON flag is `-O`; `-F` fails silently"*
    — and the binary refutes it. Discovered 2026-08-17 when `glab api … -O json` failed with
    `Unknown shorthand flag: 'O' in -O`, then confirmed against `glab --help`:

    - `glab api` takes **no** output flag; it prints JSON natively.
    - `glab repo view` uses **`-F`/`--output`**; `-O` does not exist there.
    - `glab issue list` uses **`-O`/`--output`**; its `-F` is `--output-format`, taking
      `details`/`ids`/`urls`.

    The blanket rule holds for exactly one of the three. This is the remembered-constant failure the
    whole feature exists to prevent, found inside this plugin's own skill.
    """
    calls = {c.split()[1] + (" " + c.split()[2] if c.split()[1] in ("repo", "issue") else ""): c
             for c in pb.gitlab_calls("group/proj")}

    api = [c for c in pb.gitlab_calls("group/proj") if c.startswith("glab api")]
    assert api, "the adapter must call the REST API"
    for c in api:
        assert " -O" not in c and " -F" not in c, f"`glab api` takes no output flag: {c}"

    view = next(c for c in pb.gitlab_calls("group/proj") if c.startswith("glab repo view"))
    assert " -F json" in view, f"`glab repo view` uses -F: {view}"

    issues = next(c for c in pb.gitlab_calls("group/proj") if c.startswith("glab issue list"))
    assert " -O json" in issues, f"`glab issue list` uses -O: {issues}"
    assert " -F " not in issues, "on `issue list`, -F is --output-format and takes details/ids/urls"


def test_the_docs_root_uses_gitlabs_dash_blob_form():
    """GitHub is `/blob/<branch>/`; GitLab is `/-/blob/<branch>/`. Getting this wrong produces links
    that 404, which is the exact failure the docs-root fact exists to prevent."""
    root = pb.gitlab_docs_root("https://gitlab.com", "group/proj", "main")
    assert root == "https://gitlab.com/group/proj/-/blob/main/"
    assert "/-/blob/" in root


def test_a_self_hosted_host_comes_from_the_remote_not_a_default():
    root = pb.gitlab_docs_root("https://gitlab.example.internal", "team/svc", "trunk")
    assert root.startswith("https://gitlab.example.internal/")


# --- C6: never a benign default -----------------------------------------------------------

def test_projects_v2_facts_render_as_not_applicable_on_this_forge():
    """AC4. `none enabled` and `not applicable on this forge` are different claims, and the first is
    false on GitLab — there is no Projects-v2 workflow system to be empty."""
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="group/proj", default_branch="main",
        tier="Free", labels=["status::doing"], project_id=42)}
    wf = str(facts["builtin-workflows"]["value"]).lower()
    assert "not applicable" in wf
    # The forbidden thing is the CLAIM "none enabled" / "no workflows enabled" — an absent mechanism
    # is not an empty one. Bare "none" is fine in prose explaining the absence, and a first version
    # of this test banned the substring, which condemned the correct wording.
    for false_claim in ("none enabled", "no workflows enabled", "0 enabled", "empty"):
        assert false_claim not in wf, f"reads as a benign default: {false_claim!r}"


def test_a_free_instance_produces_a_free_shaped_block():
    """AC2. Writing a scoped-label convention where scoped labels are a Premium feature documents a
    workflow the reader cannot perform."""
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main",
        tier="Free", labels=["status::doing"], project_id=1)}
    tier = facts["tier"]["value"]
    assert "Free" in tier
    assert "manual" in tier.lower() or "--unlabel" in tier


def test_a_premium_instance_says_so():
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main",
        tier="Premium", labels=["status::doing"], project_id=1)}
    assert "Premium" in facts["tier"]["value"]


def test_an_unread_label_set_is_not_an_empty_one():
    """C6, and a defect found in this adapter's own first run against a real project.

    `projects/X` reads unauthenticated but `projects/X/labels` returns 401, and the facts rendered
    `{"labels": [], "count": 0}` — indistinguishable from a project that genuinely has no `status::`
    labels. On GitLab the label set *is* the board, so "no columns" and "could not read the columns"
    are the two most different answers this fact can give, and the first is false.
    """
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main", tier="Free",
        labels=None, project_id=1)}
    cols = facts["column-families"]
    assert cols["value"]["labels"] is None
    assert "unread" in str(cols["value"]).lower()
    assert cols["provenance"] != "probed", "an unread value is not a probed one"


def test_a_genuinely_empty_label_set_says_empty_not_unread():
    """The other side: a project with no `status::` labels is a real, reportable state."""
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main", tier="Free",
        labels=[], project_id=1)}
    cols = facts["column-families"]["value"]
    assert cols["labels"] == []
    assert "unread" not in str(cols).lower()


def test_the_status_label_set_is_reported_as_the_column_family():
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main", tier="Free",
        labels=["status::doing", "status::done", "bug"], project_id=1)}
    cols = facts["column-families"]["value"]
    assert "status::doing" in str(cols) and "status::done" in str(cols)
    assert "bug" not in str(cols), "an unscoped label is not a board column"


# --- AC1: the shape is identical across forges --------------------------------------------

def test_the_field_set_matches_githubs():
    """AC1 stated mechanically: the same `template_field` set on both forges. If GitLab needed a
    different set, one command serving both forges would be the wrong unit and the honest answer
    would be two."""
    gl = {f["template_field"] for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main", tier="Free",
        labels=["status::doing"], project_id=1) if f["template_field"]}
    expected = {"forge-and-repo", "project-and-board-ids", "status-mechanism", "column-families",
                "builtin-workflows", "tier", "docs-root", "nwave-mapping"}
    assert gl == expected, f"shape differs from GitHub's: {gl ^ expected}"


def test_every_gitlab_fact_carries_a_query_and_a_legitimate_provenance():
    """Every fact names the call that produced it, and carries one of the three real provenances.

    `probed` is not universal here and must not be asserted as such: `tier` is derived from two
    proxies rather than returned, so it is `assumed`, and an unread label set is `unread`. A test
    demanding `probed` everywhere would forbid the honesty this feature is built on."""
    for f in pb.gitlab_facts(host="gitlab.com", slug="g/p", default_branch="main",
                             tier="Free", labels=[], project_id=1):
        assert f["query"], f
        assert f["provenance"] in ("probed", "assumed", "unread"), f
        if f["provenance"] != "probed":
            assert f["note"], f"a non-probed fact must say what is not knowable: {f['field']}"


# --- AC5: a network failure is not a conclusion -------------------------------------------

def test_a_connection_failure_is_retried_before_anything_is_concluded():
    """AC5. A single failure is usually the network, and concluding `no board` from one timeout on a
    self-hosted instance is how a wrong answer gets recorded permanently."""
    attempts = []

    def flaky(argv):
        attempts.append(argv)
        if len(attempts) < 2:
            raise pb.Refusal("could not connect to gitlab.example.internal")
        return json.dumps({"ok": True})

    out = pb.with_retry(lambda: flaky(["glab", "api", "x"]), attempts_allowed=3)
    assert json.loads(out)["ok"] is True
    assert len(attempts) == 2, "it retried rather than concluding"


def test_a_persistent_connection_failure_refuses_and_names_it_as_connectivity():
    def always(argv):
        raise pb.Refusal("could not connect to gitlab.example.internal")

    with pytest.raises(pb.Refusal) as e:
        pb.with_retry(lambda: always(["glab", "api", "x"]), attempts_allowed=3)
    assert "connect" in e.value.reason.lower()


def test_retry_does_not_swallow_a_non_connection_refusal():
    """A 401 is not a flaky network, and retrying it three times just delays the real answer."""
    calls = []

    def unauthorized(argv):
        calls.append(argv)
        raise pb.Refusal("401 Unauthorized")

    with pytest.raises(pb.Refusal):
        pb.with_retry(lambda: unauthorized(["glab", "api", "x"]), attempts_allowed=3)
    assert len(calls) == 1, "an auth failure is not retried"


# --- the seam: gitlab_facts -> render_region ----------------------------------------------
#
# The defect this section exists for: `gitlab_facts` was called eight times above and its result was
# never fed to the renderer, while the renderer's own tests used only GitHub-shaped facts. Both halves
# green, the join broken, and `--host gitlab.com` could not complete at all — a KeyError before a
# single byte rendered. A test per component is not a test of the pipeline.

def _render_block():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "render_block", SCRIPT.parent / "render-block.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def gitlab_probe(labels=("status::doing", "status::done", "bug")):
    return {"status": "ok", "forge": "gitlab",
            "facts": pb.gitlab_facts(host="gitlab.com", slug="g/p", default_branch="main",
                                     tier="Free", labels=list(labels), project_id=42),
            "half_probed": [], "not_probeable": []}


def test_a_gitlab_probe_renders_end_to_end():
    rb = _render_block()
    out = rb.render_region(gitlab_probe(), "2026-08-17T21:00Z")
    assert "phil:board-setup:v1:begin" in out
    assert "status::doing" in out and "status::done" in out
    assert "gitlab.com" in out


def test_every_gitlab_fact_line_carries_exactly_one_provenance():
    rb = _render_block()
    out = rb.render_region(gitlab_probe(), "2026-08-17T21:00Z")
    head = out.split("**Queries**")[0]
    for line in [l for l in head.splitlines() if l.startswith("- ")]:
        n = ("(probed ·" in line) + ("(assumed ·" in line)
        assert n == 1, f"line carries {n} provenance labels: {line}"


def test_the_rendered_gitlab_region_has_the_same_shape_as_a_github_one():
    """AC1, at the level that matters: the rendered *field labels* match, not just the field keys."""
    rb = _render_block()
    gh = {"status": "ok", "facts": [
        {"field": f, "value": "x", "query": "Q", "provenance": "probed", "note": None,
         "template_field": f}
        for f in ("forge-and-repo", "project-and-board-ids", "status-mechanism", "column-families",
                  "builtin-workflows", "tier", "docs-root", "nwave-mapping")],
        "half_probed": [], "not_probeable": []}

    def labels(region):
        head = region.split("**Queries**")[0]
        return [l.split(":")[0] for l in head.splitlines() if l.startswith("- ")]

    assert labels(rb.render_region(gitlab_probe(), "S")) == \
           labels(rb.render_region(gh, "S"))


def test_a_gitlab_project_with_no_status_labels_renders_none_defined_not_a_blank():
    rb = _render_block()
    out = rb.render_region(gitlab_probe(labels=("bug",)), "2026-08-17T21:00Z")
    assert "none defined on this project" in out


def test_an_unread_gitlab_label_set_never_reaches_the_region():
    rb = _render_block()
    probe = {"status": "ok", "forge": "gitlab",
             "facts": pb.gitlab_facts(host="gitlab.com", slug="g/p", default_branch="main",
                                      tier="Free", labels=None, project_id=42),
             "half_probed": [], "not_probeable": []}
    out = rb.render_region(probe, "2026-08-17T21:00Z")
    assert "unread" not in out.lower()
    assert "Columns" not in out, "the unread column fact must be absent, not blank"


def test_the_forge_and_repo_note_does_not_carry_the_refuted_blanket_flag_rule():
    """The worst finding of the release: the note that propagates into a consumer's CLAUDE.md carried
    verbatim the blanket rule this release refuted — and it was attached to a fact whose own query
    uses `-F`. A remembered constant, written down as a probed fact, by the feature built to prevent
    exactly that."""
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main", tier="Free",
        labels=[], project_id=1)}
    for f in facts.values():
        note = (f.get("note") or "").lower()
        assert "`-f` fails silently" not in note, f"refuted blanket rule in {f['field']}: {note}"
        assert not ("json flag is `-o`" in note), f"refuted blanket rule in {f['field']}: {note}"


def test_gitlab_tier_is_not_claimed_as_probed():
    """Tier is derived from `issues_enabled` plus `iterations_access_level` — a proxy, not a returned
    tier. Claiming `probed` for an inference is the category error this feature exists to prevent."""
    facts = {f["field"]: f for f in pb.gitlab_facts(
        host="gitlab.com", slug="g/p", default_branch="main", tier="Free",
        labels=[], project_id=1)}
    assert facts["tier"]["provenance"] == "assumed"
    assert facts["tier"]["note"], "an assumed value must say what is not knowable and why"
