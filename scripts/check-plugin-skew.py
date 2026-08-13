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

import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN_KEY = "phil@pmvanev-plugins"


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
        return 0

    detail = (
        f"PLUGIN SKEW — /phil:* commands load {loaded_version}; this tree is {tree_version}.\n"
        f"  loaded from: {loaded_path}\n"
        f"  A dogfood run here exercises {loaded_version}, NOT your working copy. Any claim about\n"
        f"  a skill's behaviour is a claim about {loaded_version} until the plugin is updated.\n"
        f"  Run /plugin to update phil, or state the version the run exercised."
    )
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
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # A detector that breaks the session is worse than the defect it detects.
        sys.exit(0)
