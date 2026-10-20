"""Drafts release notes with two subagents: one reads the history, one writes the notes."""
import json
import subprocess

AGENTS = {
    "history-reader": {
        "description": "Lists the commits since the last tag.",
        "prompt": "List the commits since the last tag, one line each, oldest first.",
        "tools": ["Bash(git log:*)"],
    },
    "notes-drafter": {
        "description": "Groups a list of commits into release notes.",
        "prompt": "Group the commits under Added, Changed and Fixed. Write nothing to disk.",
        "tools": ["Read", "Grep", "Glob"],
    },
}


def command(agent, task):
    return ["claude", "-p", task, "--agents", json.dumps(AGENTS), "--agent", agent]


def run(agent, task):
    return subprocess.run(command(agent, task), capture_output=True, text=True, check=True).stdout
