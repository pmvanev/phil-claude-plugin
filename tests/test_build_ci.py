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
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "ci-pipelines.md"
SKILL = REPO / "skills" / "build-ci" / "SKILL.md"
COMMAND = REPO / "commands" / "build-ci.md"
FIXTURES = sorted((REPO / "skills" / "build-ci" / "self-test").glob("*/manifest.json"))
BUILDS = [m for m in FIXTURES if json.loads(m.read_text())["mode"] == "build"]
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
- **Andon**: a failed main pipeline notifies the whole team
- **Notify**: a failure or a warning names whoever started the pipeline
"""


def _skill():
    """The skill and the references it sends each pass to."""
    texts = [SKILL.read_text()] + [p.read_text() for p in sorted((SKILL.parent / "references").glob("*.md"))]
    return " ".join(" ".join(texts).split())


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
    assert BUILDS, "no fixture builds a pipeline"
    for manifest in BUILDS:
        project = manifest.parent / "project"
        assert project.is_dir(), f"{manifest.parent.name} has no project/ to build"
        assert not list(project.rglob(".gitlab-ci*")) and not (project / ".github").exists()


def test_the_rule_still_gives_the_default_this_file_checks_against():
    """The matrix test below reads the default's meaning; a changed default must fail here first."""
    assert DEFAULT_BLOCK in RULE.read_text()


# Each job kind's cells under the default policy, per forge. A GitLab pipeline started by hand on main
# runs as main does; GitHub's default gives no hand-run trigger. Neither creates a tag pipeline. The
# schedule runs full mutation and the secret scan; on GitHub the andon job watches it too.
CHECK = {"MR": {"runs", "if paths"}, "docs-only MR": SKIPPED, "main push": {"runs"},
         "docs-only main": SKIPPED, "schedule": {"—"}, "tag": {"—"}}
EXPECTED = {
    "gitlab": {
        "(pipeline)": {"MR": {"created"}, "docs-only MR": {"created"}, "main push": {"created"},
                       "docs-only main": {"created"}, "schedule": {"created"}, "tag": {"—"},
                       "web or API": {"created"}},
        "secret-scan": {**{s: {"runs"} for s in SOURCES}, "tag": {"—"}},
        "check": {**CHECK, "web or API": {"runs"}},
        "mutation-diff": {**{s: {"—"} for s in SOURCES}, "MR": {"runs", "if paths"}, "docs-only MR": SKIPPED},
        "mutation-full": {**{s: {"—"} for s in SOURCES}, "schedule": {"runs"}},
        "tell-author": {**{s: {"on failure"} for s in SOURCES}, "schedule": {"—"}, "tag": {"—"}},
        # A project that deploys: one image and a staging deploy on every main commit, after the gates;
        # a docs-only commit builds nothing (PIPE-24); production waits for a person. Nothing deploys
        # from an MR or the schedule.
        "image": {**{s: {"—"} for s in SOURCES}, "main push": {"runs"}, "docs-only main": {"exits early"},
                  "web or API": {"runs"}},
        "deploy": {**{s: {"—"} for s in SOURCES}, "main push": {"runs"}, "docs-only main": {"exits early"},
                   "web or API": {"runs"}},
        "deploy-manual": {**{s: {"—"} for s in SOURCES}, "main push": {"manual"},
                          "docs-only main": {"manual"}, "web or API": {"manual"}},
    },
    "github": {
        "(pipeline)": {"MR": {"created"}, "docs-only MR": {"created"}, "main push": {"created"},
                       "docs-only main": {"created"}, "schedule": {"created"}, "tag": {"—"},
                       "web or API": {"—"}},
        "secret-scan": {**{s: {"runs"} for s in SOURCES}, "tag": {"—"}, "web or API": {"—"}},
        "check": {**CHECK, "web or API": {"—"}},
        "mutation-diff": {**{s: {"—"} for s in SOURCES}, "MR": {"runs", "if paths"}, "docs-only MR": SKIPPED},
        "mutation-full": {**{s: {"—"} for s in SOURCES}, "schedule": {"runs"}},
        "andon": {**{s: {"—"} for s in SOURCES}, "main push": {"on failure"}, "docs-only main": {"on failure"},
                  "schedule": {"on failure"}},
        "tell-author": {**{s: {"on failure"} for s in SOURCES}, "schedule": {"—"}, "tag": {"—"},
                        "web or API": {"—"}},
        # Production deploys from a dispatch that names a commit, in a workflow of its own.
        "image": {**{s: {"—"} for s in SOURCES}, "main push": {"runs"}, "docs-only main": {"exits early"}},
        "deploy": {**{s: {"—"} for s in SOURCES}, "main push": {"runs"}, "docs-only main": {"exits early"}},
        "deploy-manual": {**{s: {"—"} for s in SOURCES}, "web or API": {"manual", "runs"}},
    },
}
KIND_ALIASES = {"test": "check", "build": "check"}
DEPLOY_KINDS = {"image", "deploy", "deploy-manual"}  # only a project that deploys has them


def test_the_expected_matrix_keeps_the_default_policy_in_every_cell():
    """D7: MR-only; change-scoped tests and mutation on the MR; a docs-only change runs the secret scan
    alone; main runs everything but mutation; a schedule runs full mutation and deploys nothing; a
    failure on any MR or main pipeline names whoever started it, and on GitHub a red main pulls the
    andon from the pipeline."""
    for manifest in BUILDS:
        spec = json.loads(manifest.read_text())
        want = EXPECTED[spec.get("forge", "gitlab")]
        rows = _matrix((manifest.parent / "expected-matrix.md").read_text())
        pipeline = rows.pop("(pipeline)")
        assert all(pipeline[s] in want["(pipeline)"][s] for s in SOURCES), pipeline
        kinds = spec["kinds"]
        assert set(rows) == {j for js in kinds.values() for j in js}, "every job has a kind"
        have, every = set(KIND_ALIASES.get(k, k) for k in kinds), set(want) - {"(pipeline)"}
        assert every - DEPLOY_KINDS <= have <= every, \
            f"{manifest.parent.name}: the kinds the default policy needs on this forge"
        for job, cells in rows.items():
            kind = KIND_ALIASES.get(next(k for k, js in kinds.items() if job in js), None)
            kind = kind or next(k for k, js in kinds.items() if job in js)
            for source in SOURCES:
                assert cells[source] in want[kind][source], f"{manifest.parent.name}: {job} × {source}: {cells[source]}"


def test_the_grant_holds_the_refusals_the_prose_states():
    """`Bash(sh:*)` admits `sh -c 'git push'`; `Bash(glab:*)` admits `glab ci run`."""
    grant = re.search(r"^allowed-tools: (.+)$", COMMAND.read_text(), re.M).group(1)
    for wide in ("Bash(sh:*)", "Bash(glab:*)", "Bash(gh:*)", "Bash(git:*)", "Bash(git remote:*)", "Bash"):
        assert wide not in [g.strip() for g in grant.split(",")], wide
    assert "Write no digest or SHA you did not read" in " ".join(SKILL.read_text().split())


def test_the_schedule_and_the_secret_scan_do_not_contradict():
    skill = _skill()
    assert "every job except the schedule's own work, the secret scan and the andon" in skill
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


# Slice 04: the speed and rework passes.
TIMINGS = REPO / "skills" / "build-ci" / "scripts" / "pipeline-timings.py"


def test_the_command_offers_both_passes_and_can_run_the_timing_script():
    text = COMMAND.read_text()
    assert "--speed" in text and "--rework" in text
    grant = re.search(r"^allowed-tools: (.+)$", text, re.M).group(1)
    assert "Bash(python3:*)" in [g.strip() for g in grant.split(",")]


def test_the_speed_pass_measures_before_it_ranks_and_says_where_it_stops():
    """D11. Goldratt: only the critical path shortens the pipeline; queue wait belongs to the runners."""
    skill = _skill()
    assert "skills/build-ci/scripts/pipeline-timings.py" in skill
    assert "only from jobs on the critical path" in skill
    assert "Queue wait is mostly the runners' time" in skill
    assert "a wait that gates is no candidate" in skill
    assert "runner-up" in skill
    assert "The stopping line" in skill
    assert "re-measure" in skill


def test_the_rework_pass_lists_every_artifacts_producers():
    """D12. A package built in test and again in deploy is the mined case."""
    skill = _skill()
    assert "each artifact's producing jobs" in skill
    assert "An artifact with two producers" in skill


def _fixture(name):
    return next(m for m in FIXTURES if m.parent.name == name)


def test_the_rework_fixture_expects_an_artifact_built_twice_by_jobs_it_holds():
    manifest = _fixture("02-rework")
    ci = (manifest.parent / "project" / ".gitlab-ci.yml").read_text()
    rows = [l for l in (manifest.parent / "expected-producers.md").read_text().splitlines()
            if l.startswith("| ") and not l.startswith("| Artifact") and not l.startswith("|---")]
    twice = [r for r in rows if "✗" in r]
    assert twice, "the fixture seeds no artifact built twice"
    for row in rows:
        producers = [c.strip() for c in row.strip("|").split("|")][1]
        for job in re.findall(r"`([^`]+)`", producers):
            assert f"\n{job}:" in ci, f"{job} is not a job in the fixture"


def test_the_speed_fixture_traces_to_the_path_it_expects():
    """The script's reading of the fixture's history is the ground the expected ranking stands on."""
    manifest = _fixture("03-speed")
    want = json.loads(manifest.read_text())
    files = sorted(str(p) for p in (manifest.parent / "project" / "history").glob("pipeline-*.json"))
    out = subprocess.run([sys.executable, "-I", str(TIMINGS), "--forge", "gitlab", "--json", "--latest-shape",
                          "--exclude", "release", *files], capture_output=True, text=True, check=True)
    summary = json.loads(out.stdout)
    assert summary["commonest_path"] == want["critical_path"]
    assert (summary["median_wall"], summary["median_queue"]) == (757, 90), "expected.md states 12:37 and 1:30"
    for decoy in want["off_path"]:
        assert summary["jobs"][decoy]["on_path"] == 0, decoy


# The andon. GitLab pulls the cord with its Pipeline status emails integration, a forge setting; GitHub
# tells only the user who triggered the run, so a job pulls it through the entry-point script.

def test_the_skill_pulls_the_andon_cord_on_both_forges():
    skill = _skill()
    assert "integrations/pipelines-email" in skill, "read the GitLab setting before asking"
    assert "Email these addresses when main's pipeline fails?" in skill
    assert "./scripts/ci/run.sh andon" in skill
    assert "issues: write" in skill and "contents: read" in skill, "a job's permissions replace the top's"
    assert "A red main stops the line" in skill
    assert "nothing merges but the fix or its revert" in skill, "continuous-delivery.md owns the response"
    assert "revert it first" not in skill


def test_the_skill_wires_only_what_each_forge_carries_out():
    """The skill review found Step 2 offering channels Steps 5 and 7 could not wire (2026-10-22)."""
    skill = _skill()
    assert "glab api -X PUT projects/:id/integrations/pipelines-email" in skill, "glab api POSTs given fields"
    assert "--jq .has_issues" in skill, "an andon issue in a repository with Issues off fails unheard"
    assert "gh api -X PATCH repos/{owner}/{repo} -F has_issues=true" in skill, "-f sends the string \"true\""
    assert "github.event.workflow_run.event == 'push'" in skill, "a failed MR run must not pull the cord"
    assert "red-main alert" in COMMAND.read_text().split("\n---", 1)[0], "the command says what the skill does"
    assert "not wired" in skill, "a channel the build cannot carry out is reported, not guessed at"
    assert "On GitLab, drop the `andon` and `promote`" in skill
    assert "ANDON_MENTION" not in skill, "unverified: whether a bot's @-mention reaches a team"


def test_the_workflow_run_form_reports_the_failed_run():
    """In a workflow_run run, GITHUB_RUN_ID and GITHUB_SHA are the andon's own, not the failed run's."""
    skill = _skill()
    for form in ("types: [completed]", "github.event.workflow_run.conclusion == 'failure'",
                 "ANDON_RUN_URL: ${{ github.event.workflow_run.html_url }}",
                 "ANDON_SHA: ${{ github.event.workflow_run.head_sha }}"):
        assert form in skill, form


def test_the_empty_project_fixture_lists_the_andon_setting_unread():
    expected = " ".join((REPO / "skills" / "build-ci" / "self-test" / "01-empty-project" / "expected.md").read_text().split())
    assert "Pipeline status emails integration" in expected


def _andon(repo, tmp_path, open_issue="", **env):
    """Run the andon task with a fake `gh` that logs its arguments and answers the issue search."""
    bin_ = tmp_path / "bin"
    bin_.mkdir(exist_ok=True)
    log = tmp_path / "gh.log"
    (bin_ / "gh").write_text(f"""#!/bin/sh
echo "$*" >> {log}
case "$1 $2" in "issue list") printf '%s' "{open_issue}" ;; esac
""")
    (bin_ / "gh").chmod(0o755)
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_"))}
    out = subprocess.run(["sh", "scripts/ci/run.sh", "andon"], cwd=repo, capture_output=True, text=True,
                         env={**clean, "PATH": f"{bin_}:{os.environ['PATH']}", **env})
    return out, (log.read_text().splitlines() if log.exists() else [])


GITHUB_RUN = {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push", "GITHUB_REPOSITORY": "acme/tally",
              "GITHUB_SERVER_URL": "https://github.com", "GITHUB_RUN_ID": "42", "GITHUB_SHA": "abc123"}


def test_a_red_main_opens_an_andon_issue(repo, tmp_path):
    out, calls = _andon(repo, tmp_path, **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    created = [c for c in calls if c.startswith("issue create")]
    assert len(created) == 1, calls
    assert "main is red" in created[0] and "https://github.com/acme/tally/actions/runs/42" in created[0]
    assert "--label andon" in created[0], "found again by its label, not a title a human might reuse"
    assert calls.index(next(c for c in calls if c.startswith("label create andon"))) < calls.index(created[0])
    assert "Close this issue once main is green." in "\n".join(calls), "the team resets the cord"


def test_a_red_main_with_an_andon_open_comments_on_it(repo, tmp_path):
    out, calls = _andon(repo, tmp_path, open_issue="7", **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    assert not [c for c in calls if c.startswith("issue create")], "one andon, not one per red run"
    assert any(c.startswith("issue comment 7") for c in calls), calls
    assert any(c.startswith("issue list") and "--label andon" in c for c in calls), calls


def test_a_workflow_run_andon_names_the_failed_run_not_its_own(repo, tmp_path):
    out, calls = _andon(repo, tmp_path, ANDON_RUN_URL="https://github.com/acme/tally/actions/runs/7",
                        ANDON_SHA="def456", **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    created = next(c for c in calls if c.startswith("issue create"))
    assert "def456: https://github.com/acme/tally/actions/runs/7" in created
    assert "runs/42" not in created and "abc123" not in created


def test_the_andon_never_pulls_outside_github_actions(repo, tmp_path):
    """A local run must not open an issue, and on GitLab the integration pulls the cord."""
    out, calls = _andon(repo, tmp_path)
    assert out.returncode != 0 and not calls
    assert "Pipeline status emails" in out.stderr


def test_the_grant_covers_every_command_the_skill_runs():
    """The plugin validator found three the skill named and the grant refused, from 1.5.0 and 1.5.1
    (2026-10-22): a run that cannot write the lockfile it promises installs from none."""
    grant = [g.strip() for g in re.search(r"^allowed-tools: (.+)$", COMMAND.read_text(), re.M).group(1).split(",")]
    skill = _skill()
    for command, granted in (("shellcheck -s sh", "Bash(shellcheck:*)"),
                             ("uv pip compile --generate-hashes", "Bash(uv pip compile:*)"),
                             ("npm install --package-lock-only", "Bash(npm install --package-lock-only:*)"),
                             ("git rev-parse --verify -q refs/heads/", "Bash(git rev-parse --verify:*)")):
        assert command in skill, command
        assert granted in grant, granted


# The author tier. `tell-author` names whoever started the pipeline on its MR, PR or commit; `inform`
# runs a check that gates nothing and tells them when it fails, in place of allow_failure or
# continue-on-error, which tell nobody.

def test_the_skill_tells_whoever_started_the_pipeline():
    skill = _skill()
    for form in ("./scripts/ci/run.sh tell-author", "./scripts/ci/run.sh inform", "`when: on_failure`",
                 "`.post`", "`pull-requests: write`", "PR_NUMBER: ${{ github.event.pull_request.number }}",
                 "`NOTIFY_TOKEN`"):
        assert form in skill, form
    assert "never passes through this run" in skill, "the user creates the token; its value stays out"
    assert "Under a Notify field: a failure or a warning names you" in skill


def _task(repo, tmp_path, *args, gh_out="", **env):
    """Run a task with a fake `gh` and `curl` that log their arguments; `gh api` answers `gh_out`."""
    bin_ = tmp_path / "bin"
    bin_.mkdir(exist_ok=True)
    log = tmp_path / "calls.log"
    for tool in ("gh", "curl"):
        (bin_ / tool).write_text(f"""#!/bin/sh
echo "{tool} $*" >> {log}
case "$1" in api) printf '%s' "{gh_out}" ;; esac
""")
        (bin_ / tool).chmod(0o755)
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_", "GITLAB_"))}
    out = subprocess.run(["sh", "scripts/ci/run.sh", *args], cwd=repo, capture_output=True, text=True,
                         env={**clean, "PATH": f"{bin_}:{os.environ['PATH']}", **env})
    return out, (log.read_text() if log.exists() else "")


GITLAB_RUN = {"CI": "true", "GITLAB_CI": "true", "CI_PIPELINE_SOURCE": "merge_request_event",
              "CI_API_V4_URL": "https://gitlab.example.invalid/api/v4", "CI_PROJECT_ID": "12",
              "CI_PIPELINE_URL": "https://gitlab.example.invalid/acme/tally/-/pipelines/88",
              "CI_COMMIT_SHA": "abc123", "GITLAB_USER_LOGIN": "bob", "NOTIFY_TOKEN": "t0ken"}


def test_a_failed_pr_pipeline_names_whoever_started_it(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "tell-author", PR_NUMBER="5", GITHUB_TRIGGERING_ACTOR="alice", **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    assert "gh pr comment 5 --body @alice: the pipeline failed: https://github.com/acme/tally/actions/runs/42" in calls


def test_a_failed_main_run_names_its_starter_on_the_merged_pr(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "tell-author", gh_out="9", GITHUB_TRIGGERING_ACTOR="alice", **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    assert "gh api repos/acme/tally/commits/abc123/pulls" in calls and "gh pr comment 9 " in calls


def test_a_failed_mr_pipeline_comments_on_the_mr_naming_its_starter(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "tell-author", CI_MERGE_REQUEST_IID="3", **GITLAB_RUN)
    assert out.returncode == 0, out.stderr
    assert "/projects/12/merge_requests/3/notes" in calls and "body=@bob: the pipeline failed" in calls
    assert "PRIVATE-TOKEN: t0ken" in calls


def test_a_failed_main_pipeline_on_gitlab_comments_on_the_commit(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "tell-author", **{**GITLAB_RUN, "CI_PIPELINE_SOURCE": "push"})
    assert out.returncode == 0, out.stderr
    assert "/projects/12/repository/commits/abc123/comments" in calls and "note=@bob: " in calls


def test_gitlab_without_its_token_fails_rather_than_lose_the_message(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "tell-author", CI_MERGE_REQUEST_IID="3", **{**GITLAB_RUN, "NOTIFY_TOKEN": ""})
    assert out.returncode != 0 and "NOTIFY_TOKEN" in out.stderr and not calls


def test_tell_author_never_runs_outside_ci(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "tell-author")
    assert out.returncode != 0 and not calls
    assert "tell-author runs in CI" in out.stderr


def test_a_check_that_informs_tells_its_starter_and_passes(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "inform", "no-such-task", PR_NUMBER="5", GITHUB_TRIGGERING_ACTOR="alice",
                       **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    assert "gh pr comment 5 --body @alice: warning: `no-such-task` failed; it gates nothing" in calls


def test_a_check_that_informs_and_passes_tells_nobody(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "inform", "scope", PR_NUMBER="5", **GITHUB_RUN)
    assert out.returncode == 0, out.stderr
    assert "pr comment" not in calls



def test_the_alert_wiring_is_written_out_where_it_cannot_be_misread():
    """Two reviews found the table's prose read as a needs cycle and as job-level `when:` beside
    `rules:`, which GitLab rejects; the forms now live as YAML in references/alerts.md (2026-10-22)."""
    ref = (SKILL.parent / "references" / "alerts.md").read_text()
    assert "Read `${CLAUDE_PLUGIN_ROOT}/skills/build-ci/references/alerts.md` whole" in _skill()
    assert '    - if: $CI_PIPELINE_SOURCE == "schedule"\n      when: never\n    - when: on_failure\n' in ref
    assert "every job but tell-author" in ref and "every job but the andon" in ref
    for fact in ("masked, not protected", "Premium or Ultimate", "365 days", "fork", "Dependabot",
                 "a `workflow_run` notifier cannot use `tell-author`", "a schedule has no author"):
        assert fact.lower() in " ".join(ref.split()).lower(), fact


def test_a_declined_token_leaves_the_warning_under_allow_failure():
    skill = _skill()
    assert "On a no, leave the Notify field out of the block" in skill
    assert "into `./scripts/ci/run.sh inform <task>`" in skill, "an existing pipeline's informational jobs convert"


def test_a_warning_that_cannot_be_delivered_still_gates_nothing(repo, tmp_path):
    """Both reviews: `inform` failed its job when the comment could not post, so a warning gated."""
    out, calls = _task(repo, tmp_path, "inform", "no-such-task", "extra", CI_MERGE_REQUEST_IID="3",
                       **{**GITLAB_RUN, "NOTIFY_TOKEN": ""})
    assert out.returncode == 0, out.stderr
    assert "warning not delivered" in out.stderr and "`no-such-task`" in out.stderr


def test_a_warning_names_one_task_on_one_line(repo, tmp_path):
    out, calls = _task(repo, tmp_path, "inform", "no-such-task", "extra", PR_NUMBER="5",
                       GITHUB_ACTOR="alice", **GITHUB_RUN)
    assert "warning: `no-such-task` failed; it gates nothing" in calls


def test_the_command_says_what_the_author_tier_does():
    head = COMMAND.read_text().split("\n---", 1)[0]
    assert "names whoever started a failed pipeline" in head
    assert "names whoever started a failed pipeline" in SKILL.read_text().split("\n---", 1)[0]


# Deploying what passed: a deploy waits for every gate and ships the one image the build pushed, by
# digest, with each environment's settings injected at deploy time (PIPE-27 to PIPE-31, 2026-10-22).

DIGEST = "registry.example.invalid/acme/tally@sha256:" + "ab" * 32


def _deploy(repo, tmp_path, *args, **env):
    """Run a deploy task against a stand-in for the project's deploy command, which logs its arguments."""
    log = tmp_path / "deploy.log"
    deploy = repo / "scripts" / "deploy.sh"
    deploy.write_text(f'#!/bin/sh\necho "$*" >> {log}\n')
    deploy.chmod(0o755)
    out, _ = _task(repo, tmp_path, *args, **env)
    return out, (log.read_text().splitlines() if log.exists() else [])


GITLAB_MAIN = {"CI": "true", "GITLAB_CI": "true", "CI_PIPELINE_SOURCE": "push"}


def test_a_deploy_ships_the_digest_the_build_pushed(repo, tmp_path):
    out, calls = _deploy(repo, tmp_path, "deploy", "staging", IMAGE=DIGEST, **GITLAB_MAIN)
    assert out.returncode == 0, out.stderr
    assert calls == [f"staging {DIGEST}"]


def test_a_deploy_refuses_a_reference_a_later_push_can_move(repo, tmp_path):
    """PIPE-30: `:latest` or a branch tag can name an image no pipeline tested."""
    for image in ("registry.example.invalid/acme/tally:latest", "registry.example.invalid/acme/tally:main", ""):
        out, calls = _deploy(repo, tmp_path, "deploy", "production", IMAGE=image, **GITLAB_MAIN)
        assert out.returncode != 0 and "digest" in out.stderr, image
        assert calls == [], image


def test_a_deploy_names_one_environment(repo, tmp_path):
    out, calls = _deploy(repo, tmp_path, "deploy", IMAGE=DIGEST, **GITLAB_MAIN)
    assert out.returncode == 2 and calls == []


def test_a_docs_only_main_commit_deploys_nothing(repo, tmp_path):
    """PIPE-24 names a build on a docs-only change, so the image job builds none and the deploy has
    nothing new to ship; the environment keeps the image it runs."""
    base = _change(repo, "docs/guide.md")
    out, calls = _deploy(repo, tmp_path, "deploy", "staging", IMAGE=DIGEST,
                         **{**GITLAB_MAIN, "CI_COMMIT_BEFORE_SHA": base})
    assert out.returncode == 0 and calls == []
    assert "staging keeps the image it runs" in out.stdout


def test_a_deploy_refuses_another_repositorys_image(repo, tmp_path):
    """A manual job's variables outrank the dotenv report, so a person could hand it any digest."""
    out, calls = _deploy(repo, tmp_path, "deploy", "staging", IMAGE="evil.invalid/x@sha256:" + "ab" * 32,
                         IMAGE_REPO="registry.example.invalid/acme/tally", **GITLAB_MAIN)
    assert out.returncode != 0 and calls == []


def _gh_runs(tmp_path, run_id="", ref=DIGEST, artifact=True):
    """A stand-in for gh: `run list` answers run_id, and `run download` writes the run's image record."""
    bin_ = tmp_path / "bin"
    bin_.mkdir(exist_ok=True)
    (bin_ / "gh").write_text(f"""#!/bin/sh
echo "gh $*" >> {tmp_path / "gh.log"}
case "$1 $2" in
  "run list") printf '%s' "{run_id}" ;;
  "run download")
    dir=.; prev=; for arg; do [ "$prev" = --dir ] && dir=$arg; prev=$arg; done
    {{download}} ;;
esac
""".replace("{download}", f'printf "%s\\n" "{ref}" > "$dir/image.ref"' if artifact
            else 'echo "no artifact matches any of the names provided" >&2; exit 1'))
    (bin_ / "gh").chmod(0o755)


COMMIT = "c0ffee" * 6 + "c0ff"
GITHUB_DISPATCH = {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "workflow_dispatch",
                   "GITHUB_REPOSITORY": "acme/tally"}


def test_a_promotion_ships_the_image_a_green_main_run_built(repo, tmp_path):
    """A typed digest let a production dispatch ship what no gate passed (skill-reviewer C1, 2026-10-22).
    The dispatch names a commit; the image comes from that commit's green default-branch run."""
    log = tmp_path / "deploy.log"
    (repo / "scripts" / "deploy.sh").write_text(f'#!/bin/sh\necho "$*" >> {log}\n')
    (repo / "scripts" / "deploy.sh").chmod(0o755)
    _gh_runs(tmp_path, run_id="4242")
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_", "GITLAB_"))}
    out = subprocess.run(["sh", "scripts/ci/run.sh", "promote", "production", COMMIT], cwd=repo,
                         capture_output=True, text=True,
                         env={**clean, "PATH": f"{tmp_path / 'bin'}:{os.environ['PATH']}", **GITHUB_DISPATCH})
    assert out.returncode == 0, out.stderr
    assert log.read_text().splitlines() == [f"production {DIGEST}"]
    listed = next(l for l in (tmp_path / "gh.log").read_text().splitlines() if l.startswith("gh run list"))
    for flag in (f"--commit {COMMIT}", "--status success", "--event push", "--branch main"):
        assert flag in listed, flag


def test_a_commit_no_green_run_built_is_never_promoted(repo, tmp_path):
    log = tmp_path / "deploy.log"
    (repo / "scripts" / "deploy.sh").write_text(f'#!/bin/sh\necho "$*" >> {log}\n')
    _gh_runs(tmp_path, run_id="")
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_", "GITLAB_"))}
    for commit in (COMMIT, "main", "abc123"):
        out = subprocess.run(["sh", "scripts/ci/run.sh", "promote", "production", commit], cwd=repo,
                             capture_output=True, text=True,
                             env={**clean, "PATH": f"{tmp_path / 'bin'}:{os.environ['PATH']}", **GITHUB_DISPATCH})
        assert out.returncode != 0, commit
    assert not log.exists()


def _buildah(tmp_path, digest="sha256:" + "cd" * 32):
    """A stand-in for buildah whose push writes the digest it was asked for."""
    bin_ = tmp_path / "bin"
    bin_.mkdir(exist_ok=True)
    (bin_ / "buildah").write_text(f"""#!/bin/sh
echo "buildah $*" >> {tmp_path / "buildah.log"}
if [ "$1" = push ]; then
  for arg; do case "$arg" in --digestfile=*) printf '%s' "{digest}" > "${{arg#--digestfile=}}" ;; esac; done
fi
""")
    (bin_ / "buildah").chmod(0o755)
    return digest


def test_the_image_task_pushes_once_and_hands_on_the_digest(repo, tmp_path):
    digest = _buildah(tmp_path)
    out, _ = _task(repo, tmp_path, "image", IMAGE_REPO="registry.example.invalid/acme/tally",
                   CI_COMMIT_SHA="abc123", REGISTRY_USER="ci", REGISTRY_PASSWORD="s3cret", **GITLAB_MAIN)
    assert out.returncode == 0, out.stderr
    assert (repo / "image.env").read_text() == f"IMAGE=registry.example.invalid/acme/tally@{digest}\n"
    pushes = [l for l in (tmp_path / "buildah.log").read_text().splitlines() if l.startswith("buildah push")]
    assert len(pushes) == 1 and "registry.example.invalid/acme/tally:abc123" in pushes[0]
    calls = (tmp_path / "buildah.log").read_text()
    assert "buildah login --username ci --password-stdin registry.example.invalid" in calls
    assert "s3cret" not in calls, "the password goes through stdin, never the command line"


def test_a_docs_only_main_commit_builds_no_image(repo, tmp_path):
    _buildah(tmp_path)
    base = _change(repo, "docs/guide.md")
    out, _ = _task(repo, tmp_path, "image", IMAGE_REPO="registry.example.invalid/acme/tally",
                   CI_COMMIT_SHA="abc123", **{**GITLAB_MAIN, "CI_COMMIT_BEFORE_SHA": base})
    assert out.returncode == 0, out.stderr
    assert not (repo / "image.env").exists() and not (tmp_path / "buildah.log").exists()


def test_on_github_the_digest_is_a_job_output(repo, tmp_path):
    digest = _buildah(tmp_path)
    output = tmp_path / "github_output"
    out, _ = _task(repo, tmp_path, "image", IMAGE_REPO="ghcr.io/acme/tally", GITHUB_ACTIONS="true",
                   GITHUB_EVENT_NAME="push", GITHUB_SHA="abc123", GITHUB_OUTPUT=str(output))
    assert out.returncode == 0, out.stderr
    assert output.read_text() == f"image=ghcr.io/acme/tally@{digest}\n"
    assert (repo / "image.ref").read_text() == f"ghcr.io/acme/tally@{digest}\n", "the record a promotion reads"


def test_the_skill_shapes_every_deploy_to_the_deploy_rows():
    skill = _skill()
    for row in ("PIPE-27", "PIPE-28", "PIPE-29", "PIPE-30", "PIPE-31"):
        assert row in skill, row
    assert "reports: dotenv" in skill, "GitLab hands the digest on as a dotenv report"
    assert "needs.build-image.outputs.image" in skill, "GitHub hands it on as a job output"
    assert "scoped to its environment" in skill, "settings are injected at deploy time, never built in"
    assert "Rollback environment" in skill, "GitLab's own rollback reruns an earlier deploy job"
    assert "ci_forward_deployment_rollback_allowed" in skill, "a setting that can hide that rollback"
    assert "no `allow_failure`" in skill and "blocked" in skill, "a failed production deploy stops the line"
    assert "./scripts/ci/run.sh promote production <commit>" in skill, "GitHub promotes a commit, not a digest"
    assert "drop the `image`, `deploy` and `promote` tasks" in skill, "a project that deploys nothing"
    assert "Every job's image holds `git`" in skill, "run.sh stops where git cannot read the checkout"


def test_the_skill_builds_around_no_deploy_that_breaks_a_row():
    """build-ci writes no Dockerfile or deploy script, so a build that bakes an environment in is reported."""
    skill = _skill()
    assert "write no deploy job around it" in skill


@pytest.mark.parametrize("name", ["05-deploy", "06-github-deploy"])
def test_the_deploy_fixture_seeds_a_tag_the_build_must_not_ship(name):
    project = _fixture(name).parent / "project"
    assert ":latest" in (project / "scripts" / "deploy.sh").read_text(), "the default a deploy must override"
    assert "TALLY_LEDGER_DIR" in (project / "AGENTS.md").read_text(), "an environment setting to inject"


def test_a_commit_whose_run_built_no_image_is_never_promoted(repo, tmp_path):
    """A docs-only commit's green run skips the image job, so it has no record to promote."""
    log = tmp_path / "deploy.log"
    (repo / "scripts" / "deploy.sh").write_text(f'#!/bin/sh\necho "$*" >> {log}\n')
    _gh_runs(tmp_path, run_id="4242", artifact=False)
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CI", "GITHUB_", "GITLAB_"))}
    out = subprocess.run(["sh", "scripts/ci/run.sh", "promote", "production", COMMIT], cwd=repo,
                         capture_output=True, text=True,
                         env={**clean, "PATH": f"{tmp_path / 'bin'}:{os.environ['PATH']}", **GITHUB_DISPATCH})
    assert out.returncode != 0 and "built no image" in out.stderr
    assert not log.exists()
