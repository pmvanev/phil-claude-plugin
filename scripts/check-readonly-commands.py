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
    r"""Reject a `Bash(...)` grant carrying a path or a variable.

    The rule stands; its original rationale did not survive measurement, and the corrected one is
    below. **`allowed-tools` DOES interpolate `${CLAUDE_PLUGIN_ROOT}`.** Measured 2026-08-21 against
    the shipped Claude Code 2.1.239, at two sites:

        m = a["allowed-tools"], h = typeof m === "string" ? f(m) : ...
        f = (Y) => { let W = hOe(Y, {path: o, source: r}); ... }
        function hOe(e, t) { ... e.replace(/\$\{CLAUDE_PLUGIN_ROOT\}/g, () => r(t.path)) ... }

    Reproduce with: `strings ~/.local/share/claude/versions/2.1.239 | grep -o '.\{0,220\}\["allowed-tools"\].\{0,300\}'`
    and the same over `function hOe(`.

    So the earlier claim — that such a grant "matches nothing" and merely prompts on every run — was
    FALSE on this build. The grant becomes an absolute-path rule, and because a command's body is
    interpolated by the same function at the same load, an invocation written
    `${CLAUDE_PLUGIN_ROOT}/x.py` produces the very string the rule now holds. It can match.

    Three reasons the rejection is kept anyway, none of them the original one:

    1. **The grant a human reads is not the grant enforced.** After interpolation it is an absolute,
       install- and version-specific path. A reviewer auditing `allowed-tools` cannot tell what it
       permits without knowing the install root — and the whole point of the declaration is that a
       reader can see the boundary.
    2. **It matches only one spelling.** Any other route to the same script — a relative path, a
       `cd` first, a different interpreter path — shares no prefix and silently prompts. The narrow
       grant is narrow in a way nobody can predict from reading it.
    3. **De facto convention.** The 2026-08-17 survey of 211 `Bash()` grants across this repo and
       every installed plugin found exactly one containing a slash or a variable; the other 210 name
       a bare executable.

    Whether reasons 1-3 are worth an enforced check is now a live question rather than a settled
    one, because the fact that motivated the check is gone. Recorded here rather than quietly
    kept — a check whose stated rationale is false is the defect this repo keeps finding.

    Added 2026-08-17 after `board-setup` shipped exactly that grant. A survey of 211 `Bash()`
    grants across this repo and every installed plugin found it to be the only one containing a
    slash or a variable; the other 210 name a bare executable. To scope a command to one script,
    grant the interpreter and put the path in the invocation instruction, then carry the real
    intent in the skill's prose — the `adversarial-review` pattern `CLAUDE.md` already documents.
    """
    body = grant[len("Bash("):].rstrip(")")
    if "${" in body:
        return (f"{name}: `{grant}` interpolates a variable. `allowed-tools` DOES expand "
                f"`${{CLAUDE_PLUGIN_ROOT}}` (measured on 2.1.239), so the rule becomes an "
                f"install-specific absolute path: unreadable to a reviewer and matching only one "
                f"spelling of the invocation. Grant the interpreter; put the path in the body")
    if "/" in body:
        return (f"{name}: `{grant}` contains a path. Permission rules are literal prefix "
                f"matches, so the grant covers exactly one spelling of the invocation and "
                f"silently prompts for every other. Grant the interpreter and put the path in "
                f"the command body")
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
        # Count only what the matchability check actually inspects. Counting every grant — `Read`,
        # `Glob`, `Skill` and the rest — reported 204 where 43 `Bash(...)` grants exist, overstating
        # coverage roughly fivefold. A number nobody can reconcile is how a check stops being read.
        for grant in grants:
            if grant.startswith("Bash("):
                grants_syntax_checked += 1
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
