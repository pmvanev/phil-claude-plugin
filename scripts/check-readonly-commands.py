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


def check_grant_is_matchable(name: str, grant: str) -> str | None:
    """Reject a `Bash(...)` grant carrying a path or a variable.

    Permission rules are literal prefix matches, and `${CLAUDE_PLUGIN_ROOT}` is interpolated in a
    command's BODY, not in `allowed-tools`. So `Bash(python3 ${CLAUDE_PLUGIN_ROOT}/x.py:*)` matches
    nothing: the model runs an absolute path that shares no prefix with the literal rule text, and
    the shell sees an empty variable if it copies the spelling instead.

    The failure is silent in the worst way — the command still works, it just prompts for
    permission on every run, and a prompt reads as normal. Worse, a grant like that *looks*
    narrower than any real grant could be, so its own documentation ends up claiming a boundary
    nothing enforces.

    Added 2026-08-17 after `board-setup` shipped exactly that grant. A survey of 211 `Bash()`
    grants across this repo and every installed plugin found it to be the only one containing a
    slash or a variable; the other 210 name a bare executable. To scope a command to one script,
    grant the interpreter and put the path in the invocation instruction, then carry the real
    intent in the skill's prose — the `adversarial-review` pattern `CLAUDE.md` already documents.
    """
    body = grant[len("Bash("):].rstrip(")")
    if "${" in body:
        return (f"{name}: `{grant}` interpolates a variable, which `allowed-tools` does not do — "
                f"the rule can never match, so the command prompts on every run")
    if "/" in body:
        return (f"{name}: `{grant}` contains a path — permission rules are literal prefix "
                f"matches, so this cannot match an absolute-path invocation. Grant the "
                f"interpreter and put the path in the command body")
    return None


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    failures: list[str] = []
    checked = 0
    grants_syntax_checked = 0

    for path in sorted((root / "commands").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        try:
            frontmatter = text.split("---", 2)[1]
        except IndexError:
            failures.append(f"{path.name}: no frontmatter")
            continue

        tools_line = re.search(r"^allowed-tools:\s*(.+)$", frontmatter, re.M)
        tools = tools_line.group(1) if tools_line else ""

        try:
            grants = tool_grants(tools)
        except ValueError as e:
            failures.append(f"{path.name}: {e}")
            continue

        # Runs for EVERY command regardless of `mutates`, because an unmatchable grant is a defect
        # in any command: it prompts on every run while looking narrower than a real grant could be.
        grants_syntax_checked += len(grants)
        for grant in grants:
            if grant.startswith("Bash("):
                problem = check_grant_is_matchable(path.name, grant)
                if problem:
                    failures.append(problem)

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
          f"all commands carry a declaration; {grants_syntax_checked} `Bash(...)` grant(s) "
          f"verified matchable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
