#!/usr/bin/env python3
"""Report when /phil:* commands would run a different version than this working tree.

Claude Code loads a plugin from ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/,
snapshotted at install time. Editing this repo does not change what /phil:* executes. The skew
is silent: nothing errors, and a dogfood run against a stale snapshot is indistinguishable from
one against the working tree.

This runs from the working tree via .claude/settings.json, not from the plugin, so it is not
subject to the skew it reports. A detector shipped inside the plugin would load from the cache
and could not report the gap that exists before the first update.

Silent when in sync. Never fails the session: any error exits 0 with no output, because a
broken check must not be mistaken for a clean one — and must not block a session either.
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN_KEY = "phil@pmvanev-plugins"

# The directories that actually ship and are actually loaded. `docs/` and `tests/` ship too (an
# accepted decision, see CLAUDE.md) but nothing loads them, so a difference there is not skew.
SHIPPED = ("skills", "agents", "commands", "rules", "hooks")


def fingerprint(root: Path) -> str:
    """Hash the shipped surfaces by relative path and content.

    **Why a version comparison is not enough.** The version check answers "is a different release
    loaded", and content can change without the version moving — which is the normal state of a
    working tree mid-slice. Measured 2026-08-26: tree and cache both read 0.69.0, so the detector was
    silent, while one shared fragment differed by 51 lines and seven files existed only in the tree.
    That is precisely the state this file's own docstring calls indistinguishable from a clean one,
    and it was being covered by a human writing it into a slice document by hand.
    """
    h = hashlib.sha256()
    for top in SHIPPED:
        base = root / top
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".json", ".py", ".sh"):
                continue
            h.update(str(path.relative_to(root)).encode())
            h.update(path.read_bytes())
    return h.hexdigest()[:12]


def repo_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and (Path(env) / ".claude-plugin/plugin.json").exists():
        return Path(env)
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, timeout=5,
        cwd=Path(__file__).resolve().parent,
    )
    return Path(out.stdout.strip())


def emit(detail: str) -> None:
    json.dump(
        {
            "systemMessage": detail,
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": detail,
            },
        },
        sys.stdout,
    )


def main() -> int:
    root = repo_root()
    tree_version = json.loads((root / ".claude-plugin/plugin.json").read_text())["version"]

    installed = json.loads(
        (Path.home() / ".claude/plugins/installed_plugins.json").read_text()
    )
    entries = installed.get("plugins", {}).get(PLUGIN_KEY) or []
    if not entries:
        # Not installed at all. Nothing loads the plugin, so there is no skew to report —
        # and saying "not installed" to someone who never installed it is noise.
        return 0

    loaded_version = entries[0].get("version")
    loaded_path = entries[0].get("installPath", "?")
    if loaded_version == tree_version:
        loaded_root = Path(loaded_path).expanduser()
        if not loaded_root.is_dir():
            return 0
        tree_fp, loaded_fp = fingerprint(root), fingerprint(loaded_root)
        if tree_fp == loaded_fp:
            return 0
        detail = (
            f"PLUGIN CONTENT SKEW — same version {tree_version}, different bytes.\n"
            f"  loaded from: {loaded_path}\n"
            f"  tree fingerprint {tree_fp} vs loaded {loaded_fp}.\n"
            f"  The version matches, so nothing else reports this. A /phil:* run here still exercises\n"
            f"  the snapshot, NOT your edits. Bump the version and update, or say which copy you ran.\n"
        )
        emit(detail)
        return 0

    detail = (
        f"PLUGIN SKEW — /phil:* commands load {loaded_version}; this tree is {tree_version}.\n"
        f"  loaded from: {loaded_path}\n"
        f"  A dogfood run here exercises {loaded_version}, NOT your working copy. Any claim about\n"
        f"  a skill's behaviour is a claim about {loaded_version} until the plugin is updated.\n"
        f"  Run /plugin to update phil, or state the version the run exercised."
    )
    emit(detail)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # A detector that breaks the session is worse than the defect it detects.
        sys.exit(0)
