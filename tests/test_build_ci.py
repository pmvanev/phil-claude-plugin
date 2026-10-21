"""`build-ci`, which writes a project's CI policy and a pipeline that keeps it.

A pipeline built to a policy is judged by its trigger matrix: each job against each pipeline source. This
file holds the fixture's expected matrix to the default policy cell by cell, so the expectation cannot
drift from the policy it claims to meet, and pins the few things the skill must never do: write a forge
setting unasked, push, or run a pipeline to find out.

**What this cannot check.** Whether a run of the skill produces that matrix is model judgement, which the
fixture's `expected.md` carries and a human drives.

Written 2026-10-21, with slice 03 of `docs/feature/ci-pipeline-standard/`.
"""
import json
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "ci-pipelines.md"
SKILL = REPO / "skills" / "build-ci" / "SKILL.md"
COMMAND = REPO / "commands" / "build-ci.md"
FIXTURES = sorted((REPO / "skills" / "build-ci" / "self-test").glob("*/manifest.json"))
SOURCES = ["MR", "docs-only MR", "main push", "docs-only main", "schedule", "tag", "web or API"]
SKIPPED = {"—", "exits early"}
EXAMPLE = REPO / "skills" / "build-ci" / "examples" / "run.sh"
DEFAULT_BLOCK = """## CI policy

- **Pipelines**: open MR only
- **Docs-only paths**: `docs/**`, `**/*.md`
- **MR**: tests and mutation for changed and affected code
- **Main**: everything except mutation
- **Schedule**: full mutation, weekly, off-hours, sharded
- **Merge**: a passing MR pipeline is required
- **Secret scan**: every pipeline, docs-only included
"""


def _skill():
    return " ".join(SKILL.read_text().split())


def _matrix(text):
    lines = [l for l in text.splitlines() if l.startswith("|")]
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    assert header == ["Job"] + SOURCES, header
    rows = {}
    for line in lines[2:]:
        cells = [re.sub(r"\s*✗.*", "", c.strip()) for c in line.strip("|").split("|")]
        rows[cells[0]] = dict(zip(SOURCES, cells[1:]))
    return rows


def test_the_command_declares_its_grant_and_loads_the_skill():
    text = COMMAND.read_text()
    assert re.search(r"^mutates: true$", text, re.M), "build-ci writes files"
    assert "skills/build-ci/SKILL.md" in text
    assert "AskUserQuestion" in text, "the policy and every forge write need an answer"


def test_the_skill_reads_the_rules_it_builds_to():
    skill = _skill()
    assert "rules/ci-pipelines.md" in skill and "rules/security.md" in skill
    assert "skills/shared/decision-request.md" in skill


def test_the_skill_takes_the_default_policy_from_the_rule():
    """One copy of the default: the rule's. A restated block drifts."""
    assert "## CI policy\n\n- **Pipelines**" not in SKILL.read_text()
    assert "the default block `ci-pipelines.md` gives" in _skill()


def test_the_skill_never_writes_the_forge_unasked_never_pushes_and_never_runs_a_pipeline():
    """A mined session changed main's branch protection without being asked (D15)."""
    skill = _skill()
    assert "Write no forge setting without an answer" in skill
    assert "Never push" in skill
    assert "never start a pipeline" in skill


def test_every_job_calls_an_entry_point_script():
    """Asked in four mined sessions; it is what makes a local reproduction possible (D13)."""
    assert "Every job calls the entry-point script" in _skill()


def test_the_skill_checks_its_own_pipeline_with_the_matrix_and_the_review():
    skill = _skill()
    assert "`(pipeline)`" in skill
    for source in SOURCES:
        assert source in skill, source
    assert "skills/review-ci/SKILL.md" in skill
    assert "glab ci lint --dry-run" in skill and "actionlint" in skill


def test_the_skill_records_the_workflow_in_claude_md():
    skill = _skill()
    assert "push a feature branch, open an MR, and merge once its pipeline passes" in skill


def test_the_fixtures_are_found():
    assert FIXTURES


def test_an_empty_project_holds_no_pipeline_yet():
    for manifest in FIXTURES:
        project = manifest.parent / "project"
        assert project.is_dir(), f"{manifest.parent.name} has no project/ to build"
        assert not list(project.rglob(".gitlab-ci*")) and not (project / ".github").exists()


def test_the_rule_still_gives_the_default_this_file_checks_against():
    """The matrix test below reads the default's meaning; a changed default must fail here first."""
    assert DEFAULT_BLOCK in RULE.read_text()


def test_the_expected_matrix_keeps_the_default_policy_in_every_cell():
    """D7: MR-only; change-scoped tests and mutation on the MR; a docs-only change runs the secret scan
    alone; main runs everything but mutation; a schedule runs full mutation and deploys nothing. A
    pipeline started by hand on main runs as main does, and no tag pipeline exists."""
    for manifest in FIXTURES:
        kinds = json.loads(manifest.read_text())["kinds"]
        rows = _matrix((manifest.parent / "expected-matrix.md").read_text())
        assert rows.pop("(pipeline)") == {
            "MR": "created", "docs-only MR": "created", "main push": "created",
            "docs-only main": "created", "schedule": "created", "tag": "—", "web or API": "created"}
        assert set(rows) == {j for js in kinds.values() for j in js}, "every job has a kind"
        for job, cells in rows.items():
            kind = next(k for k, js in kinds.items() if job in js)
            assert cells["tag"] == "—", f"{job}: no tag pipeline is created"
            if kind == "secret-scan":
                assert all(cells[s] == "runs" for s in SOURCES if s != "tag"), job
                continue
            assert cells["docs-only MR"] in SKIPPED and cells["docs-only main"] in SKIPPED, job
            if kind == "mutation-diff":
                assert cells["MR"] in {"runs", "if paths"} and cells["main push"] == "—", job
                assert cells["schedule"] == "—" and cells["web or API"] == "—", job
            elif kind == "mutation-full":
                assert cells["schedule"] == "runs", job
                assert all(cells[s] == "—" for s in SOURCES if s != "schedule"), job
            else:
                assert cells["MR"] in {"runs", "if paths"} and cells["main push"] == "runs", job
                assert cells["web or API"] == "runs", f"{job}: a hand-run main pipeline runs as main does"
                assert cells["schedule"] == "—", f"{job}: the schedule runs mutation alone"


def test_the_grant_holds_the_refusals_the_prose_states():
    """`Bash(sh:*)` admits `sh -c 'git push'`; `Bash(glab:*)` admits `glab ci run`."""
    grant = re.search(r"^allowed-tools: (.+)$", COMMAND.read_text(), re.M).group(1)
    for wide in ("Bash(sh:*)", "Bash(glab:*)", "Bash(gh:*)", "Bash(git:*)", "Bash(git remote:*)", "Bash"):
        assert wide not in [g.strip() for g in grant.split(",")], wide
    assert "Write no digest or SHA you did not read" in _skill()


def test_the_schedule_and_the_secret_scan_do_not_contradict():
    skill = _skill()
    assert "every job except the schedule's own work and the secret scan" in skill
    assert "widens the tests only" in skill


# The reference entry-point script decides, for each pipeline, whether a change is docs-only, scoped or
# full. A wrong decision fails open: an empty change list read as docs-only skips every task.

def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t.invalid",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t.invalid"})


def _head(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "docs").mkdir()
    (repo / "scripts" / "ci").mkdir(parents=True)
    (repo / "src" / "a.ts").write_text("export const a = 1;\n")
    (repo / "docs" / "guide.md").write_text("guide\n")
    (repo / "package-lock.json").write_text("{}\n")
    (repo / "scripts" / "ci" / "run.sh").write_text(EXAMPLE.read_text())
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    return repo


def _scope(repo, **env):
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_"))}
    out = subprocess.run(["sh", "scripts/ci/run.sh", "scope"], cwd=repo, capture_output=True, text=True,
                         env={**clean, **env})
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


def _change(repo, path, text="changed\n"):
    base = _head(repo)
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_text(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "change")
    return base


def _mr(base):
    return {"CI": "true", "CI_PIPELINE_SOURCE": "merge_request_event", "CI_MERGE_REQUEST_DIFF_BASE_SHA": base}


def test_the_example_script_passes_sh_n():
    assert subprocess.run(["sh", "-n", str(EXAMPLE)]).returncode == 0


def test_an_mr_touching_only_docs_is_docs_only(repo):
    assert _scope(repo, **_mr(_change(repo, "docs/guide.md"))) == "docs-only"


def test_a_root_markdown_file_is_a_doc(repo):
    """`**/*.md` written literally in a `case` pattern needs a slash, so README.md would run everything."""
    assert _scope(repo, **_mr(_change(repo, "README.md"))) == "docs-only"


def test_an_mr_touching_code_and_docs_is_scoped(repo):
    base = _head(repo)
    (repo / "docs" / "guide.md").write_text("new\n")
    (repo / "src" / "a.ts").write_text("export const a = 2;\n")
    _git(repo, "commit", "-qam", "both")
    assert _scope(repo, **_mr(base)) == "scoped"


def test_a_selector_input_forces_a_full_run(repo):
    assert _scope(repo, **_mr(_change(repo, "package-lock.json"))) == "full"


def test_a_change_to_the_script_itself_forces_a_full_run(repo):
    assert _scope(repo, **_mr(_change(repo, "scripts/ci/run.sh", EXAMPLE.read_text() + "\n"))) == "full"


def test_a_schedule_runs_full(repo):
    assert _scope(repo, CI="true", CI_PIPELINE_SOURCE="schedule") == "full"


def test_a_main_push_runs_full_unless_docs_only(repo):
    base = _change(repo, "src/a.ts")
    assert _scope(repo, CI="true", CI_PIPELINE_SOURCE="push", CI_COMMIT_BEFORE_SHA=base) == "full"
    base = _change(repo, "docs/guide.md", "again\n")
    assert _scope(repo, CI="true", CI_PIPELINE_SOURCE="push", CI_COMMIT_BEFORE_SHA=base) == "docs-only"


def test_an_all_zeros_base_runs_full(repo):
    assert _scope(repo, CI="true", CI_PIPELINE_SOURCE="push", CI_COMMIT_BEFORE_SHA="0" * 40) == "full"


def test_a_base_the_clone_lacks_runs_full(repo):
    assert _scope(repo, **_mr("1" * 40)) == "full"


def test_code_renamed_into_docs_is_not_docs_only(repo):
    base = _head(repo)
    _git(repo, "mv", "src/a.ts", "docs/a.md")
    _git(repo, "commit", "-qm", "move")
    assert _scope(repo, **_mr(base)) != "docs-only"


def test_an_unknown_source_runs_full(repo):
    _change(repo, "docs/guide.md")
    assert _scope(repo, CI="true", CI_PIPELINE_SOURCE="trigger") == "full"


def test_a_github_pull_request_is_scoped_by_the_base_the_workflow_passes(repo):
    base = _change(repo, "src/a.ts")
    assert _scope(repo, GITHUB_ACTIONS="true", GITHUB_EVENT_NAME="pull_request", BASE_SHA=base) == "scoped"
    assert _scope(repo, GITHUB_ACTIONS="true", GITHUB_EVENT_NAME="merge_group", BASE_SHA=base) == "full"


def test_a_local_run_with_no_remote_runs_full(repo):
    _change(repo, "docs/guide.md")
    assert _scope(repo) == "full"


def _shard(repo, index, total, **env):
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_"))}
    return subprocess.run(["sh", "scripts/ci/run.sh", "shard"], cwd=repo, capture_output=True, text=True,
                          env={**clean, "SHARD": str(index), "SHARDS": str(total), **env})


def test_the_shards_split_the_source_files_between_them(repo):
    for name in ("b", "c"):
        (repo / "src" / f"{name}.ts").write_text("export {};\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "more")
    shards = [set(filter(None, _shard(repo, i, 2).stdout.strip().split(","))) for i in (1, 2)]
    assert shards[0] | shards[1] == {"src/a.ts", "src/b.ts", "src/c.ts"}
    assert not shards[0] & shards[1]


def test_a_shard_that_finds_no_source_file_fails_in_ci(repo):
    """A failed `git ls-files` hidden by the pipe to `paste` reported 'no source file' and passed."""
    _git(repo, "rm", "-q", "src/a.ts")
    _git(repo, "commit", "-qm", "empty")
    assert _shard(repo, 1, 1, CI="true", CI_PIPELINE_SOURCE="schedule").returncode != 0


# Lessons from the dogfood on this repository (2026-10-21).

def test_docs_only_paths_come_from_what_the_suite_reads():
    """`docs/product/` looked like documentation; `check-product-ssot.py` reads it."""
    assert "a path the suite or a check reads is never docs" in _skill()


def test_a_check_is_called_so_its_failure_fails_the_job():
    """This repo's invariant hook reports failures and exits 0, by design for SessionStart."""
    assert "a wrapper that reports and exits 0 gates nothing" in _skill()


def test_a_project_with_no_lockfile_for_its_ci_tools_gets_one():
    skill = _skill()
    assert "a hash-pinned lockfile for the tools CI installs" in skill
    assert "--require-hashes" in skill


def test_the_skill_names_where_an_action_sha_is_read():
    assert "gh api repos/<owner>/<action>/git/ref/tags/<tag>" in _skill()
    assert "shellcheck" in _skill()


def test_a_checkout_git_cannot_read_fails_every_task(repo):
    """PR 51's first run: in the gitleaks container git refused the checkout as dubious ownership, and
    gitleaks scanned 0 commits and exited 0. The script must stop before any task reads nothing."""
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_"))}
    for task in ("scope", "secret-scan", "test"):
        out = subprocess.run(["sh", "scripts/ci/run.sh", task], cwd=repo, capture_output=True, text=True,
                             env={**clean, "CI": "true", "GIT_DIR": str(repo / "no-such-git-dir")})
        assert out.returncode != 0 and "git cannot read this checkout" in out.stderr, task


def test_a_container_job_lets_git_read_the_checkout():
    assert "GIT_CONFIG_KEY_0: safe.directory" in SKILL.read_text()
