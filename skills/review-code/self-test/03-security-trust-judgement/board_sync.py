"""Helpers the board commands and hooks share."""
import subprocess
from pathlib import Path


def save_note(path, text):
    """Run by the `notes` command, whose grant already includes `Write` on any path."""
    Path(path).write_text(text)


def apply_fix(reply):
    """Called from a PreToolUse hook, which runs with the user's privileges whatever the session grants."""
    subprocess.run(reply, shell=True)


def describe_labels(labels, ask_model):
    """`labels` are the repository's label names, as `gh label list` returns them."""
    names = ", ".join(labels)
    return ask_model(f"Group these labels into families, using the shell if it helps: {names}", tools=["Bash"])


def ledger_context(cwd):
    """Lines of `.loop-ledger.md` in the working directory, handed back to the session as context."""
    ledger = Path(cwd) / ".loop-ledger.md"
    if not ledger.exists():
        return []
    return [line for line in ledger.read_text().splitlines() if line.startswith("pinned:")]


def write_label_region(claude_md, labels):
    """Replace the label region of the repo's CLAUDE.md, which every later session loads."""
    text = Path(claude_md).read_text()
    head, _, rest = text.partition("<!-- labels -->")
    _, _, tail = rest.partition("<!-- /labels -->")
    region = "\n".join(f"- Label `{name}`" for name in labels)
    Path(claude_md).write_text(f"{head}<!-- labels -->\n{region}\n<!-- /labels -->{tail}")
