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
import re
import shlex
import subprocess
import sys
import tempfile

LEDGER = ".refactor-loop-ledger.md"
PATCH = ".refactor-loop-patch.diff"
MESSAGE = ".refactor-loop-commit-msg"
LOOP_FILES = (LEDGER, PATCH, MESSAGE)
WRITE_TOOLS = ("Write", "Edit", "NotebookEdit")

# Refused before a command is split into words: each lets an allowed first word carry a second command,
# a redirect or an expansion. The probe's escapes were a chain, a redirect and a substitution.
SHELL_SYNTAX = re.compile(r"[;&|<>$`\\\n\r*?\[\]{}~!#]")

# The test-path globs of G2 and of the workflow's diff scan, anchored for git's repo-relative paths.
TEST_PATTERNS = [r"(^|/)tests?/", r"(^|/)spec/", r"(^|/)__tests__/", r"_test\.", r"\.test\.", r"\.spec\.",
                 r"(^|/)test_[^/]*\.py$", r"(^|/)conftest\.py$"]
# Files a later session loads as instructions or settings: a patch that edits them escalates past the run.
# A bare `.claude` entry and `CLAUDE.local.md` passed the first patterns (plugin-dev:plugin-validator).
# The list is not complete: a file a CLAUDE.md `@import`s, or a script a project's hook runs, also
# persists past the run. It keeps the obvious routes out; the test suite already runs the patch's code.
INSTRUCTION_PATTERNS = [r"(^|/)\.claude(/|$)", r"(^|/)claude(\.local)?\.md$", r"(^|/)agents\.md$",
                        r"(^|/)\.mcp\.json$"]
SYMLINK_MODE = "120000"
GITLINK_MODE = "160000"


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


def run_is_active(root):
    """Only the ledger writer can write the ledger, so an active one marks the repository this run targets."""
    ledger = os.path.join(root, LEDGER)
    if os.path.islink(ledger) or not os.path.isfile(ledger):
        return False
    with open(ledger, encoding="utf-8", errors="replace") as f:
        return re.search(r"^active-run:\s*true\s*$", f.read(), re.M) is not None


def is_repo_root(directory):
    proc = subprocess.run(["git", "-C", directory, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, timeout=10)
    return proc.returncode == 0 and os.path.realpath(proc.stdout.strip()) == directory


def is_loop_file_at_a_repo_root(name, path, cwd):
    spelled = os.path.normpath(os.path.join(cwd, path))
    # A symlinked file sends the write wherever it points; a symlinked directory still ends here.
    if os.path.basename(spelled) != name or os.path.islink(spelled):
        return False
    return is_repo_root(os.path.realpath(os.path.dirname(spelled)))


def names_the_ledger(path, cwd):
    # Case-folded, because `.Refactor-Loop-Ledger.md` is the ledger on a case-insensitive filesystem.
    spelled = os.path.join(cwd, path)
    leaves = (os.path.basename(spelled), os.path.basename(os.path.realpath(spelled)))
    return any(leaf.casefold() == LEDGER for leaf in leaves)


def only_this_file(role, name, tool_input, cwd, active_run=False):
    path = target_path(tool_input)
    if not is_loop_file_at_a_repo_root(name, path, cwd):
        raise Refused(f"the {role} may touch only {name} at a repository root, not {shown(path)}.")
    if active_run and not run_is_active(os.path.realpath(os.path.dirname(os.path.join(cwd, path)))):
        raise Refused(f"no refactor-loop run is active in that repository, so the {role} may not act there.")


def ledger_writer(tool, tool_input, cwd):
    if tool not in ("Read", "Write"):
        raise Refused(f"the ledger writer may only Read and Write the run ledger, not use {tool}.")
    only_this_file("ledger writer", LEDGER, tool_input, cwd)


def command_words(tool_input):
    if not isinstance(tool_input, dict) or not isinstance(tool_input.get("command"), str):
        raise Refused("the call carries no command to check.")
    command = tool_input["command"]
    if SHELL_SYNTAX.search(command):
        raise Refused(f"shell syntax is refused; run the one allowed command alone, not {shown(command)}.")
    return shlex.split(command)


def root_named_by(word):
    root = os.path.normpath(word)
    if not os.path.isabs(root) or not is_repo_root(os.path.realpath(root)):
        return None
    return root


def loop_file_named_by(word, root, name):
    if os.path.normpath(word) != os.path.join(root, name) or not is_loop_file_at_a_repo_root(name, word, root):
        return None
    return word


def patch_named_by(words, shape):
    """`git -C <repo root> apply --recount <shape…> <repo root>/<PATCH>`, word for word."""
    flags = words[5:-1]
    if (len(words) < 6 or words[:2] != ["git", "-C"] or words[3:5] != ["apply", "--recount"]
            or flags not in shape):
        return None
    root = root_named_by(words[2])
    patch = root and loop_file_named_by(words[-1], root, PATCH)
    return (root, patch) if patch else None


def require_active_run(role, root):
    if not run_is_active(os.path.realpath(root)):
        raise Refused(f"no refactor-loop run is active in that repository, so the {role} may not act there.")


def git(root, *args, env=None):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, timeout=10, env=env)


def paths_git_will_touch(root, patch):
    """Applies the patch to a scratch index made from HEAD and lists every path that changed, a rename
    as both its sides. Git does the parsing, so every header form and quoting reaches the check as the
    path git writes. A header regex let through an unprefixed rename, `rename old`/`rename new` and
    octal-quoted names (plugin-dev:plugin-validator, 2026-10-20); `--numstat` then named only a rename's
    destination, so a rename out of tests/ passed."""
    with tempfile.TemporaryDirectory() as scratch:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env["GIT_INDEX_FILE"] = os.path.join(scratch, "index")
        if git(root, "rev-parse", "--verify", "-q", "HEAD", env=env).returncode == 0:
            base = "HEAD"
            if git(root, "read-tree", "HEAD", env=env).returncode != 0:
                raise Refused("git cannot read HEAD, so the patch cannot be checked.")
        else:
            base = git(root, "hash-object", "-t", "tree", "/dev/null", env=env).stdout.decode().strip()
        applied = git(root, "apply", "--cached", "--recount", patch, env=env)
        if applied.returncode != 0:
            raise Refused(f"git cannot apply the patch to HEAD: {shown(applied.stderr.decode('utf-8', 'replace').strip())}")
        listed = git(root, "diff", "--cached", "--raw", "--no-renames", "-z", base, env=env)
        if listed.returncode != 0:
            raise Refused("git cannot list the paths the patch changes.")
    # `--raw -z` alternates a `:<old mode> <new mode> <old id> <new id> <status>` record and its path.
    fields = listed.stdout.decode("utf-8", "replace").split("\0")
    return [(path, record[1:].split()[:2]) for record, path in zip(fields[0::2], fields[1::2]) if path]


def check_patch_contents(root, patch):
    """The cage scanned the proposer's diff, not the bytes the applier wrote (D6)."""
    if not os.path.isfile(patch):
        raise Refused(f"the patch file {shown(patch)} does not exist.")
    changed = paths_git_will_touch(root, patch)
    for named, modes in changed:
        # `git add -- ':^x'` reads a leading colon as pathspec magic and stages the whole tree.
        if named.startswith(":"):
            raise Refused(f"the patch names a path git would read as pathspec magic ({shown(named)}).")
        if any(re.search(p, named, re.IGNORECASE) for p in TEST_PATTERNS):
            raise Refused(f"the patch reaches a test path ({shown(named)}); the suite is the oracle.")
        if os.path.basename(named).casefold() in LOOP_FILES:
            raise Refused(f"the patch reaches a loop file ({shown(named)}).")
        if any(re.search(p, named, re.IGNORECASE) for p in INSTRUCTION_PATTERNS):
            raise Refused(f"the patch reaches a file later sessions load as instructions ({shown(named)}).")
        if SYMLINK_MODE in modes:
            raise Refused(f"the patch creates or changes a symlink ({shown(named)}), which can point anywhere.")
        if GITLINK_MODE in modes:
            raise Refused(f"the patch creates or changes a submodule entry ({shown(named)}).")
    return [named for named, _ in changed]


def runs_one_apply(role, shape, form):
    def check(tool, tool_input, cwd):
        if tool != "Bash":
            raise Refused(f"the {role} may only run `{form}`, not use {tool}.")
        named = patch_named_by(command_words(tool_input), shape)
        if named is None:
            raise Refused(f"the {role} may only run `{form}` on {PATCH} at a repository root.")
        root, patch = named
        require_active_run(role, root)
        check_patch_contents(root, patch)
    return check


apply_patch = runs_one_apply("applier", ([], ["--check"]), "git -C <repo> apply --recount [--check] <repo>/" + PATCH)
reverse_patch = runs_one_apply("reverter", (["-R"], ["-R", "--check"]),
                               "git -C <repo> apply --recount -R [--check] <repo>/" + PATCH)


def applier(tool, tool_input, cwd):
    if tool in ("Read", "Write"):
        only_this_file("applier", PATCH, tool_input, cwd, active_run=True)
    else:
        apply_patch(tool, tool_input, cwd)


COMMIT_FORMS = ("git -C <repo> --literal-pathspecs add -- <paths the patch touches>",
                "git -C <repo> commit -F <repo>/" + MESSAGE)


def committer(tool, tool_input, cwd):
    if tool in ("Read", "Write"):
        only_this_file("committer", MESSAGE, tool_input, cwd, active_run=True)
        return
    if tool != "Bash":
        raise Refused(f"the committer may only run `{COMMIT_FORMS[0]}` and `{COMMIT_FORMS[1]}`, not use {tool}.")
    words = command_words(tool_input)
    root = root_named_by(words[2]) if len(words) > 3 and words[:2] == ["git", "-C"] else None
    # --literal-pathspecs: a staged word is a path, never pathspec magic (plugin-dev:plugin-validator).
    if root and words[3:6] == ["--literal-pathspecs", "add", "--"] and len(words) > 6:
        require_active_run("committer", root)
        patch = os.path.join(root, PATCH)
        if not loop_file_named_by(patch, root, PATCH):
            raise Refused(f"there is no patch file at {shown(patch)} to bound what may be staged.")
        touched = set(check_patch_contents(root, patch))
        for path in words[6:]:
            if path.startswith(":") or os.path.isabs(path) or os.path.normpath(path) not in touched:
                raise Refused(f"the committer may stage only paths the patch touches, not {shown(path)}.")
        # Staging part of the patch would commit part of a green change and leave the rest in the tree,
        # while the run records it committed (plugin-dev:plugin-validator, 2026-10-20).
        missing = touched - {os.path.normpath(path) for path in words[6:]}
        if missing:
            raise Refused(f"the committer must stage every path the patch changes; missing {shown(sorted(missing))}.")
        return
    if root and words[3:] == ["commit", "-F", os.path.join(root, MESSAGE)]:
        require_active_run("committer", root)
        if not loop_file_named_by(words[5], root, MESSAGE):
            raise Refused(f"the message file must be {MESSAGE} at the repository root, not a link.")
        return
    raise Refused(f"the committer may only run `{COMMIT_FORMS[0]}` and `{COMMIT_FORMS[1]}`.")


ROLES = {
    "refactor-ledger-writer": ledger_writer,
    "refactor-applier": applier,
    "refactor-reverter": reverse_patch,
    "refactor-committer": committer,
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
