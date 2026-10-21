"""`skills/build-ci/scripts/pipeline-timings.py`, which `/phil:build-ci --speed` measures with.

A speed pass that guesses spends effort off the critical path, and one that folds queue wait into job
time tunes a job when the runners were the wait. This file holds the script to the two things the pass
rests on: each pipeline's critical path, traced from the forge's own timestamps, and queue wait kept
apart from execution. Both forges' job formats are read.

Written 2026-10-21, with slice 04 of `docs/feature/ci-pipeline-standard/`.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "build-ci" / "scripts" / "pipeline-timings.py"


def _module():
    spec = importlib.util.spec_from_file_location("pipeline_timings", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _t(seconds):
    """An ISO timestamp `seconds` after 12:00:00 UTC."""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"2026-10-21T{12 + h:02d}:{m:02d}:{s:02d}.000Z"


def _gitlab_job(name, ready, queue, duration, status="success", stage="test"):
    start = ready + queue
    return {"name": name, "stage": stage, "status": status, "queued_duration": float(queue),
            "duration": float(duration), "started_at": _t(start), "finished_at": _t(start + duration)}


def _github_job(name, ready, queue, duration, conclusion="success"):
    start = ready + queue
    return {"name": name, "conclusion": conclusion, "created_at": _t(ready),
            "started_at": _t(start), "completed_at": _t(start + duration)}


# lint (60 s) and build (300 s) start together; test waits for build and runs 120 s; deploy waits for
# test. The critical path is build -> test -> deploy; lint is off it however slow it gets.
def _gitlab_pipeline(queue=5):
    return [
        _gitlab_job("lint", 0, queue, 60, stage="check"),
        _gitlab_job("build", 0, queue, 300, stage="check"),
        _gitlab_job("test", 300 + queue, queue, 120),
        _gitlab_job("deploy", 300 + queue + queue + 120, queue, 30, stage="deploy"),
        _gitlab_job("release", 0, 0, 0, status="manual", stage="deploy"),
    ]


def test_the_critical_path_follows_the_timestamps_not_the_job_order():
    m = _module()
    path = m.critical_path(m.load_gitlab(_gitlab_pipeline()))
    assert [j.name for j in path] == ["build", "test", "deploy"]


def test_a_job_that_never_started_is_left_out():
    m = _module()
    assert "release" not in [j.name for j in m.load_gitlab(_gitlab_pipeline())]


def test_queue_wait_is_kept_apart_from_execution():
    m = _module()
    summary = m.summarize([m.load_gitlab(_gitlab_pipeline(queue=60))])
    path = summary["pipelines"][0]
    assert path["execution"] == 300 + 120 + 30
    assert path["queue"] == 3 * 60
    assert path["wall"] == 60 + 300 + 60 + 120 + 60 + 30


def test_github_jobs_are_read_with_creation_as_ready_time():
    m = _module()
    jobs = m.load_github({"jobs": [
        _github_job("lint", 0, 20, 60), _github_job("test", 0, 20, 400),
        _github_job("report", 420, 10, 15)]})
    assert [j.name for j in m.critical_path(jobs)] == ["test", "report"]
    assert {j.name: j.queue for j in jobs} == {"lint": 20, "test": 20, "report": 10}


def test_medians_and_path_share_across_pipelines():
    m = _module()
    runs = [m.load_gitlab(_gitlab_pipeline(queue=q)) for q in (5, 10, 300)]
    summary = m.summarize(runs)
    build = summary["jobs"]["build"]
    assert build["duration"] == 300 and build["queue"] == 10 and build["on_path"] == 3
    assert summary["jobs"]["lint"]["on_path"] == 0
    assert summary["median_queue"] == 30 and summary["runs"] == 3


def test_the_command_line_reads_files_and_prints_a_report(tmp_path):
    files = []
    for i, q in enumerate((5, 10, 300)):
        f = tmp_path / f"pipeline-{i}.json"
        f.write_text(json.dumps(_gitlab_pipeline(queue=q)))
        files.append(str(f))
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), "--forge", "gitlab", *files],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert "build → test → deploy" in out.stdout
    assert "queue" in out.stdout.lower()


def test_no_pipeline_is_an_error_not_an_empty_report(tmp_path):
    empty = tmp_path / "empty.json"
    empty.write_text("[]")
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), "--forge", "gitlab", str(empty)],
                         capture_output=True, text=True)
    assert out.returncode != 0 and "no job" in out.stderr


def test_a_file_that_is_not_json_is_named_and_stops_the_measure(tmp_path):
    """Two of beatrix's job lists came back empty from a timed-out fetch; a traceback named neither."""
    good, bad = tmp_path / "good.json", tmp_path / "bad.json"
    good.write_text(json.dumps(_gitlab_pipeline()))
    bad.write_text("")
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), "--forge", "gitlab", str(good), str(bad)],
                         capture_output=True, text=True)
    assert out.returncode != 0 and "bad.json" in out.stderr and "Traceback" not in out.stderr


def test_pipelines_of_different_shapes_are_counted():
    """beatrix's main history spans a redesign: `ts` became `ts-fast`, and medians across both mislead."""
    m = _module()
    before = m.load_gitlab(_gitlab_pipeline())
    after = m.load_gitlab([j for j in _gitlab_pipeline() if j["name"] != "lint"])
    summary = m.summarize([before, before, after])
    assert summary["shapes"] == 2
    assert summary["latest_shape_runs"] == 1


def test_short_sibling_jobs_do_not_trace_forever(tmp_path):
    """The validator's case: two 1-second jobs ending within the slack of each other's ready time
    handed the trace back and forth, and the script never returned."""
    jobs = [_gitlab_job("build", 0, 0, 300), _gitlab_job("notify", 300, 0, 1), _gitlab_job("label", 300, 0, 1)]
    f = tmp_path / "p.json"
    f.write_text(json.dumps(jobs))
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), "--forge", "gitlab", str(f)],
                         capture_output=True, text=True, timeout=10)
    assert out.returncode == 0
    m = _module()
    assert len(m.critical_path(m.load_gitlab(jobs))) == 2


def test_a_job_named_for_exclusion_leaves_the_path_and_the_wall_clock(tmp_path):
    """A manual release played three hours later is a human's wait, not the pipeline's."""
    jobs = _gitlab_pipeline() + [_gitlab_job("release-prod", 3 * 3600, 2, 40, stage="deploy")]
    f = tmp_path / "p.json"
    f.write_text(json.dumps(jobs))
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), "--forge", "gitlab", "--json",
                          "--exclude", "release-prod", str(f)], capture_output=True, text=True, check=True)
    summary = json.loads(out.stdout)
    assert "release-prod" not in summary["jobs"]
    assert summary["commonest_path"] == ["build", "test", "deploy"]
    assert summary["median_wall"] < 3600


def test_the_next_longest_chain_caps_any_saving():
    """In the speed fixture, shortening the path below lint's 8:25 saves nothing more: lint is next."""
    m = _module()
    summary = m.summarize([m.load_gitlab(_gitlab_pipeline(queue=5))])
    # lint: ready 0, queue 5, runs 60 s -> ends at 65; it is the only chain off the path.
    assert summary["pipelines"][0]["runner_up"] == 65
    assert summary["median_runner_up"] == 65


def test_time_on_no_job_is_reported_apart():
    """Wall clock that is neither execution nor queue on the path: dependency latency, or a person."""
    m = _module()
    jobs = m.load_gitlab([_gitlab_job("build", 0, 0, 100), _gitlab_job("deploy", 160, 0, 40)])
    summary = m.summarize([jobs])
    assert summary["pipelines"][0]["other"] == 60
    assert summary["median_other"] == 60
