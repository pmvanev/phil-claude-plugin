#!/usr/bin/env python3
"""Verify that every command declaring `mutates: false` is actually unable to mutate.

The gap this closes: a validator can see that `Write` is absent, but absence carries no intent.
Twice on 2026-08-13 a command declared itself read-only in prose while granting `Bash` broad
enough to mutate, and both were found by eye because the check could not be written.

`mutates` is a claim about the GRANT, not about intent — that is the half a script can verify.
`mutates: false` asserts the tool list makes mutation impossible. `mutates: true` asserts only
that the grant permits it; a command may still intend to change nothing. `adversarial-review` is
the standing example: it reports and never edits, but it runs the project's test suite as its
deterministic oracle, and executing project code can write. Declaring it `false` would be a lie
about the grant, so it declares `true` and its skill carries the intent in prose.

A missing declaration fails. That is the point: on this board, silence reading as compliance is
the recurring defect, so an undeclared command is a finding rather than a default.
"""

import re
import sys
from pathlib import Path

MUTATING_TOOLS = {"Write", "Edit", "NotebookEdit"}

# Verbs that cannot change the repository, the forge, or anything else. Deliberately short:
# an entry here is a promise, so add one only after checking the verb has no writing mode.
READ_ONLY_VERBS = {
    "git log", "git status", "git diff", "git show", "git blame", "git rev-parse",
    "git rev-list", "git ls-tree", "git ls-files", "git cat-file", "git describe",
    "git shortlog", "git for-each-ref",
    "gh issue list", "gh issue view", "gh label list", "gh search",
    "glab issue list", "glab issue view",
    "ls", "cat", "head", "tail", "wc", "find", "rg", "grep", "jq", "sort", "uniq",
}


def tool_grants(tools: str) -> list[str]:
    """Split an allowed-tools line into individual grants.

    Comma-splitting is safe only because no grant in this plugin contains a comma; a future
    `Bash(a,b)` would split wrongly, so the checker refuses one rather than mis-reading it.
    """
    if re.search(r"\([^)]*,", tools):
        raise ValueError("a grant contains a comma; comma-splitting would mis-read it")
    return [g.strip() for g in tools.split(",") if g.strip()]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    failures: list[str] = []
    checked = 0

    for path in sorted((root / "commands").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        try:
            frontmatter = text.split("---", 2)[1]
        except IndexError:
            failures.append(f"{path.name}: no frontmatter")
            continue

        declared = re.search(r"^mutates:\s*(true|false)\s*$", frontmatter, re.M)
        if not declared:
            failures.append(
                f"{path.name}: no `mutates:` declaration — every command must state whether "
                f"its grant permits mutation"
            )
            continue
        if declared.group(1) == "true":
            continue

        checked += 1
        tools_line = re.search(r"^allowed-tools:\s*(.+)$", frontmatter, re.M)
        tools = tools_line.group(1) if tools_line else ""

        try:
            grants = tool_grants(tools)
        except ValueError as e:
            failures.append(f"{path.name}: {e}")
            continue

        for grant in grants:
            if grant in MUTATING_TOOLS:
                failures.append(f"{path.name}: declares `mutates: false` but grants `{grant}`")
            elif grant == "Bash":
                failures.append(
                    f"{path.name}: declares `mutates: false` but grants bare `Bash` — "
                    f"which permits rm, redirection, and any mutating verb"
                )
            elif grant.startswith("Bash("):
                verb = grant[len("Bash("):].rstrip(")").split(":")[0].strip()
                if verb not in READ_ONLY_VERBS:
                    failures.append(
                        f"{path.name}: declares `mutates: false` but grants `{grant}` — "
                        f"`{verb}` is not on the read-only verb allowlist"
                    )

    for f in failures:
        print(f"FAIL  {f}")
    if failures:
        print(f"\n{len(failures)} failure(s).")
        return 1
    print(f"OK  {checked} command(s) declaring `mutates: false` verified unable to mutate; "
          f"all commands carry a declaration.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
