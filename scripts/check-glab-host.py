#!/usr/bin/env python3
"""Fail when shipped prose teaches a `glab` call that does not name its host.

From a directory with no checkout, `glab` 1.112.0 sent a bare `-R <group/project>` and a `glab api`
without `--hostname` to gitlab.com, and a self-hosted project answered `404 Not Found` (observed
2026-11-05). The bare form was found in `scripts/probe-board.py`, then in seven files of three skills.

## What counts

Every fenced block and inline code span in `skills/`, `commands/`, `agents/` and `rules/`, outside
`self-test/` and frontmatter. A fence line ending in a backslash joins the next, so a continued call reads as
one. In each:

- a `glab api` call — one naming a `projects/` or `groups/` path, `user`, `:id`, `:fullpath`, or
  `graphql` with arguments — must carry `--hostname`;
- a `-R` on a `glab` call, and the project `glab repo view` takes positionally, must be a full
  `https://` URL, `<repo>` (the URL's placeholder in `skills/start/references/gitlab.md`) or a shell
  variable.

A span that only names a subcommand, such as `glab api graphql` in a heading, is not a call.

## Exemptions

A file whose every call runs inside the project's own checkout, where `glab` takes the host from
the remote, declares it:

    <!-- glab-host-exempt: <reason, at least four words> -->

Exit 0 clean and silent, 1 with named failures.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AREAS = ("skills", "commands", "agents", "rules")

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)
SPAN = re.compile(r"`([^`\n]+)`")
CALL = re.compile(r"glab\s+(?:api|issue|mr|repo|label|ci|release|variable|incident)\b[^\n|#]*")
API_TARGET = re.compile(r"(?:projects|groups)/|\buser\b|:id\b|:fullpath\b|graphql\s+-")
DASH_R = re.compile(r"(?:^|\s)-R\s+(\S+)")
REPO_VIEW = re.compile(r"^glab\s+repo\s+view\s+([^-\s]\S*)")
HOSTED_R = re.compile(r"""['"]?(?:https://|<repo>|\$)""")
EXEMPT = re.compile(r"<!--\s*glab-host-exempt:\s*(.*?)\s*-->")


def _blank(match: re.Match) -> str:
    return "\n" * match.group(0).count("\n")


def segments(text: str):
    """Yield (line number, code text) for every fence line and inline code span."""
    text = FRONTMATTER.sub(_blank, text)
    for m in FENCE.finditer(text):
        first = text[:m.start(1)].count("\n") + 1
        lines = m.group(1).split("\n")
        i = 0
        while i < len(lines):
            start, joined = i, lines[i]
            while joined.rstrip().endswith("\\") and i + 1 < len(lines):
                i += 1
                joined = joined.rstrip()[:-1] + " " + lines[i].strip()
            yield first + start, joined
            i += 1
    for n, line in enumerate(FENCE.sub(_blank, text).split("\n"), start=1):
        for s in SPAN.finditer(line):
            yield n, s.group(1)


def violations(text: str):
    for n, seg in segments(text):
        for c in CALL.finditer(seg):
            call = c.group(0).strip()
            if call.startswith("glab api") and API_TARGET.search(call) and "--hostname" not in call:
                yield n, f"`glab api` without `--hostname`: {call}"
            for r in DASH_R.finditer(call):
                if not HOSTED_R.match(r.group(1)):
                    yield n, f"`-R` without the project's URL: {call}"
            view = REPO_VIEW.match(call)
            if view and not HOSTED_R.match(view.group(1)):
                yield n, f"`glab repo view` without the project's URL: {call}"


def main() -> int:
    failures = []
    for area in AREAS:
        for path in sorted((ROOT / area).rglob("*.md")):
            if "self-test" in path.relative_to(ROOT).parts:
                continue
            text = path.read_text()
            rel = path.relative_to(ROOT)
            exempt = EXEMPT.search(text)
            if exempt:
                if len(exempt.group(1).split()) < 4:
                    failures.append(f"{rel}: glab-host-exempt needs a reason of at least four words")
                continue
            failures += [f"{rel}:{n}: {msg}" for n, msg in violations(text)]
    if failures:
        print("glab calls that do not name their host (outside a checkout they go to gitlab.com):")
        for f in failures:
            print(f"  {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
