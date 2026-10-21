#!/usr/bin/env python3
"""Measure pipelines from the forge's own job records: each job's queue wait and duration, and each
pipeline's critical path.

Used by `/phil:build-ci --speed`. Give it one JSON file per pipeline, as the forge's API returns it:

    GitLab   glab api "projects/:id/pipelines/<id>/jobs?per_page=100"   > pipeline-<id>.json
    GitHub   gh api "repos/<owner>/<repo>/actions/runs/<id>/jobs?per_page=100" > run-<id>.json

    python3 pipeline-timings.py --forge gitlab --latest-shape --exclude release-prod pipeline-*.json

Give the files oldest first. A pipeline's shape is the set of job names it ran; history that spans a
redesign mixes shapes, and a median across them describes neither. `--latest-shape` measures only the
pipelines shaped like the newest. `--exclude` leaves out a job a person starts — a manual release or
deploy — whose wait for that person is not the pipeline's time.

**Unverified on GitHub:** whether a job that `needs:` another is created when it becomes ready, so that
`created_at` is its ready time. Check one run with `needs:` before trusting a GitHub path through one.

It reads timestamps and nothing else, so it needs no access to the forge and writes nothing.

**The critical path is inferred from timestamps, not read from the CI file.** Each job became ready at
some moment: GitLab's start minus its `queued_duration`, GitHub's `created_at`. The job that ended last
ends the path; its predecessor is the job that ended last, and earlier, at or before it became ready;
and so on back. That is a heuristic: a job that happened to end just before the real dependency can
stand in for it. Shortening a job off the path shortens nothing — until the path is shorter than the
**runner-up**, the latest end of any job off it, which caps every saving.

**Queue wait is kept apart from execution.** A job that waited ten minutes is not a slow job. The wait is
mostly the runners', and can also be an environment approval, a `concurrency` group or a GitLab
`resource_group`. Wall clock that is neither — **other** — is latency between jobs, or a person.
"""
import argparse
import json
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime

SLACK = 2.0  # seconds: a predecessor may end this long after a job became ready, from clock rounding


@dataclass(frozen=True)
class Job:
    name: str
    ready: float
    start: float
    end: float

    @property
    def queue(self):
        return round(self.start - self.ready, 3)

    @property
    def duration(self):
        return round(self.end - self.start, 3)


def _epoch(stamp):
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()


def load_gitlab(jobs):
    """GitLab's `pipelines/:id/jobs` list. A job that never started — manual, skipped, created — is left out."""
    out = []
    for job in jobs:
        if job.get("status") in ("manual", "skipped", "created", "scheduled"):
            continue
        if not job.get("started_at") or not job.get("finished_at"):
            continue
        start, end = _epoch(job["started_at"]), _epoch(job["finished_at"])
        out.append(Job(job["name"], start - float(job.get("queued_duration") or 0), start, end))
    return out


def load_github(payload):
    """GitHub's `actions/runs/:id/jobs` object. A job that never started is left out."""
    out = []
    for job in payload.get("jobs", []):
        if not job.get("started_at") or not job.get("completed_at") or job.get("conclusion") == "skipped":
            continue
        out.append(Job(job["name"], _epoch(job["created_at"]), _epoch(job["started_at"]),
                       _epoch(job["completed_at"])))
    return out


def critical_path(jobs):
    """The chain of jobs that decided when the pipeline ended, first job first."""
    if not jobs:
        return []
    current = max(jobs, key=lambda j: j.end)
    path = [current]
    while True:
        # Strictly earlier ends only: each step moves back in time, so the trace always stops, even
        # when two short sibling jobs end within the slack of each other's ready time.
        before = [j for j in jobs if j.end < current.end and j.end <= current.ready + SLACK]
        if not before:
            break
        current = max(before, key=lambda j: j.end)
        path.append(current)
    return list(reversed(path))


def _median(values):
    return statistics.median(values) if values else 0


def shape(jobs):
    return frozenset(j.name for j in jobs)


def summarize(pipelines):
    """Per-pipeline wall clock, path execution and path queue; per-job medians; the commonest path; and
    how many shapes the pipelines, oldest first, came in."""
    per_pipeline, on_path, durations, queues = [], Counter(), {}, {}
    paths = Counter()
    for jobs in pipelines:
        path = critical_path(jobs)
        wall = max(j.end for j in jobs) - min(j.ready for j in jobs)
        start = min(j.ready for j in jobs)
        execution = round(sum(j.duration for j in path), 3)
        queue = round(sum(j.queue for j in path), 3)
        off = [j for j in jobs if j not in path]
        per_pipeline.append({"wall": round(wall, 3), "execution": execution, "queue": queue,
                             "other": round(wall - execution - queue, 3),
                             "runner_up": round(max(j.end for j in off) - start, 3) if off else 0,
                             "path": [j.name for j in path]})
        paths[tuple(j.name for j in path)] += 1
        for j in path:
            on_path[j.name] += 1
        for j in jobs:
            durations.setdefault(j.name, []).append(j.duration)
            queues.setdefault(j.name, []).append(j.queue)
    jobs = {name: {"runs": len(durations[name]), "duration": _median(durations[name]),
                   "queue": _median(queues[name]), "on_path": on_path[name]} for name in durations}
    latest = shape(pipelines[-1]) if pipelines else frozenset()
    return {
        "runs": len(pipelines),
        "shapes": len({shape(p) for p in pipelines}),
        "latest_shape_runs": sum(1 for p in pipelines if shape(p) == latest),
        "pipelines": per_pipeline,
        "jobs": jobs,
        "median_wall": _median([p["wall"] for p in per_pipeline]),
        "median_execution": _median([p["execution"] for p in per_pipeline]),
        "median_queue": _median([p["queue"] for p in per_pipeline]),
        "median_other": _median([p["other"] for p in per_pipeline]),
        "median_runner_up": _median([p["runner_up"] for p in per_pipeline]),
        "commonest_path": list(paths.most_common(1)[0][0]) if paths else [],
        "commonest_path_runs": paths.most_common(1)[0][1] if paths else 0,
    }


def _mmss(seconds):
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}:{s:02d}"


def report(summary):
    lines = [
        f"Pipelines measured: {summary['runs']}, in {summary['shapes']} shape(s); "
        f"{summary['latest_shape_runs']} shaped like the newest",
        f"Median wall clock: {_mmss(summary['median_wall'])}"
        f" — on the critical path, execution {_mmss(summary['median_execution'])},"
        f" queue wait {_mmss(summary['median_queue'])}, other {_mmss(summary['median_other'])}",
        f"Runner-up: the latest job off the path ends at {_mmss(summary['median_runner_up'])};"
        " no change to the path saves more than the difference",
        f"Commonest critical path ({summary['commonest_path_runs']} of {summary['runs']}): "
        + " → ".join(summary["commonest_path"]),
        "",
        "| Job | Runs | Median duration | Median queue wait | On the critical path |",
        "|---|---|---|---|---|",
    ]
    ranked = sorted(summary["jobs"].items(), key=lambda kv: (-kv[1]["on_path"], -kv[1]["duration"]))
    for name, job in ranked:
        lines.append(f"| {name} | {job['runs']} | {_mmss(job['duration'])} | {_mmss(job['queue'])} "
                     f"| {job['on_path']} of {summary['runs']} |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--forge", choices=["gitlab", "github"], required=True)
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    parser.add_argument("--exclude", action="append", default=[], metavar="JOB",
                        help="leave this job out — a manual release or deploy, whose wait is a person's")
    parser.add_argument("--latest-shape", action="store_true",
                        help="measure only the pipelines that ran the newest pipeline's jobs")
    parser.add_argument("files", nargs="+", help="one job-list JSON file per pipeline")
    args = parser.parse_args(argv)
    load = load_gitlab if args.forge == "gitlab" else load_github
    pipelines = []
    for name in args.files:
        try:
            with open(name) as f:
                jobs = load(json.load(f))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as err:
            print(f"pipeline-timings: cannot read {name}: {err}; fetch it again", file=sys.stderr)
            return 1
        jobs = [j for j in jobs if j.name not in args.exclude]
        if jobs:
            pipelines.append(jobs)
    if not pipelines:
        print("pipeline-timings: no job in any file started and finished", file=sys.stderr)
        return 1
    if args.latest_shape:
        newest = shape(pipelines[-1])
        pipelines = [p for p in pipelines if shape(p) == newest]
    summary = summarize(pipelines)
    print(json.dumps(summary, indent=2) if args.json else report(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
