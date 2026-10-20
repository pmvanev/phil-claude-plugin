#!/usr/bin/env python3
"""The refactor-loop allow-list (PreToolUse on Bash, Read, Write, Edit, NotebookEdit).

An agent file's `tools:` line picks whole tools, never commands or paths: a probe agent granted only
`Bash(echo:*)` wrote files through `touch`, a redirect, a chain and a substitution in bypass mode
(2026-10-20). This hook is the other half of the boundary. Claude Code puts the calling subagent's
`agent_type` in every PreToolUse payload, and a deny here holds in bypass mode, so each narrowed loop
role is allowed only its own paths and commands, and refused everything else (CWE-250, issue 48).

A role is matched on the type's last segment, so a copy of the agent outside the plugin is restricted
too. Every other caller passes, except that no other subagent may write the run ledger, whose
`active-run:` arms G2 (CWE-807), through a file tool. A subagent holding an unchecked shell can still
write it through Bash; that route closes as the loop's other roles are narrowed, and no command filter
stands in for it, because a glob spells the name past any filter. The main session carries no agent
type and is never checked.

Protocol: reads the hook payload as JSON on stdin; to refuse, prints a JSON decision and exits 0.
"""
import json
import os
import subprocess
import sys

LEDGER = ".refactor-loop-ledger.md"
WRITE_TOOLS = ("Write", "Edit", "NotebookEdit")


class Refused(Exception):
    pass


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"refactor-loop allow-list: {reason}",
        }
    }))


def shown(value):
    return repr(value if len(str(value)) <= 200 else str(value)[:200] + "…")


def target_path(tool_input):
    if not isinstance(tool_input, dict):
        raise Refused("the call carries no tool input to check.")
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(path, str) or not path:
        raise Refused("the call names no target path to check.")
    return path


def is_repo_root(directory):
    proc = subprocess.run(["git", "-C", directory, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, timeout=10)
    return proc.returncode == 0 and os.path.realpath(proc.stdout.strip()) == directory


def is_ledger_at_a_repo_root(path, cwd):
    spelled = os.path.normpath(os.path.join(cwd, path))
    # A symlinked ledger sends the write wherever it points; a symlinked directory still ends here.
    if os.path.basename(spelled) != LEDGER or os.path.islink(spelled):
        return False
    return is_repo_root(os.path.realpath(os.path.dirname(spelled)))


def names_the_ledger(path, cwd):
    # Case-folded, because `.Refactor-Loop-Ledger.md` is the ledger on a case-insensitive filesystem.
    spelled = os.path.join(cwd, path)
    leaves = (os.path.basename(spelled), os.path.basename(os.path.realpath(spelled)))
    return any(leaf.casefold() == LEDGER for leaf in leaves)


def ledger_writer(tool, tool_input, cwd):
    if tool not in ("Read", "Write"):
        raise Refused(f"the ledger writer may only Read and Write the run ledger, not use {tool}.")
    path = target_path(tool_input)
    if not is_ledger_at_a_repo_root(path, cwd):
        raise Refused(f"the ledger writer may touch only {LEDGER} at a repository root, not {shown(path)}.")


ROLES = {
    "refactor-ledger-writer": ledger_writer,
}


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    # Claude Code writes the payload, not the agent, so a malformed one is no attack, and refusing it
    # would stop every tool call in every session that installs the plugin.
    if not isinstance(payload, dict):
        return
    agent_type = payload.get("agent_type")
    if not isinstance(agent_type, str) or not agent_type:
        return
    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()

    role = ROLES.get(agent_type.rsplit(":", 1)[-1])
    if role:
        # The agent writes the tool input, so anything this check cannot read is refused (CWE-636).
        try:
            role(tool, tool_input, cwd)
        except Refused as refusal:
            deny(str(refusal))
        except Exception as error:
            deny(f"the call could not be checked ({type(error).__name__}), so it is refused.")
        return

    if tool in WRITE_TOOLS and isinstance(tool_input, dict):
        path = tool_input.get("file_path") or tool_input.get("notebook_path")
        if isinstance(path, str) and path and names_the_ledger(path, cwd):
            deny(f"only the ledger writer may write the run ledger, which arms G2; {agent_type} may not.")


if __name__ == "__main__":
    main()
