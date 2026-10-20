"""A board probe and the two PreToolUse hooks that ship beside it."""
import json
import re
import subprocess

FILE_PATH = re.compile(r"\b[\w.-]+/[\w./-]*\.\w{1,5}\b")


def repo_labels(slug):
    """`slug` is the `--repo` argument a model composes; its command grants `Bash(python3:*)`, not `gh`."""
    subprocess.run(["gh", "repo", "view", slug], check=True, capture_output=True)
    owner, name = slug.split("/", 1)
    query = 'query={ repository(owner:"%s", name:"%s"){ labels(first:100){ nodes { name } } } }' % (owner, name)
    return subprocess.run(["gh", "api", "graphql", "-f", query], check=True, capture_output=True, text=True).stdout


def paths_in(question):
    """`question` is the text of an AskUserQuestion call, of any length."""
    return FILE_PATH.findall(question)


def wording_gate(raw):
    """Refuse a question over 200 words. A wording standard, not a security control: fails open by design."""
    try:
        text = json.loads(raw)["tool_input"]["question"]
    except (ValueError, KeyError, TypeError):
        return None
    return "deny" if len(text.split()) > 200 else None


def protect_tests(raw):
    """Keep the refactor loop's agent from editing the tests that judge it."""
    try:
        path = json.loads(raw)["tool_input"]["file_path"]
    except (ValueError, KeyError, TypeError):
        return None
    return "deny" if "/tests/" in path else None
