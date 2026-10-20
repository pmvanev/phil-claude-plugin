"""`skills/refactor-loop/SKILL.md`, the `--interactive` fallback, must keep the safety the Workflow path has.

Found 2026-10-13, all predating that day's hardening:
- It never committed green work, and REVERT's `git checkout -- <files>` restores HEAD, so a red
  iteration wiped earlier green refactors the ledger still called resolved.
- It had no dirty-tree check, and the command's `--interactive` branch skips the one the Workflow path
  has, so a red gate discarded the user's uncommitted edits.
- It said the G2 hook needs no re-check, though a diff applied through Bash bypasses an `Edit|Write`
  matcher.
- An interrupted run left `active-run: true`, and the always-wired G2 hook then blocked test edits in
  later, unrelated sessions.
- It treated all three hooks as unwired; G2 ships wired, G7 and G10 do not, and G10 had no prose check.
- `iter` rose only on a G5 back-prompt, so the G8 cap did not bound the other paths.
- Reverting a diff that created a file failed outright.
- "The latest git changes" was undefined, and the DONE predicate read a severity and confidence the
  ledger never held; DONE now follows the Workflow path.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "refactor-loop" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split())


def test_green_work_is_committed_before_the_next_iteration():
    assert "commit the changed files" in _flat()


def test_init_refuses_a_dirty_tree_and_apply_rechecks_it():
    body = _flat()
    assert "git status --porcelain -- . ':!.refactor-loop-ledger.md'" in body
    assert "git stash push -u -- . ':!.refactor-loop-ledger.md'" in body
    assert "Confirm the tree is clean" in body
    assert "If the commit fails, HALT and report" in body


def test_the_loop_scans_the_diff_for_test_paths_itself():
    body = _flat()
    assert "You do not need to re-check it" not in body
    assert "refuse any diff that touches a test path" in body


def test_the_diff_scan_reads_every_path_line_in_any_case():
    """A pure rename carries only `rename to`, and `Tests/` is `tests/` on a case-insensitive
    filesystem; the scan read only `---`/`+++`, case-sensitively (CWE-180, issue 48)."""
    body = _flat()
    for line in ("`diff --git`", "`rename to`", "`copy to`", "in any letter case"):
        assert line in body, line


def test_the_diff_scan_refuses_a_diff_that_reaches_the_ledger():
    """The ledger arms G2, so a diff that rewrites it disarms the guard (CWE-807, issue 48)."""
    assert "refuse any diff that touches the ledger" in _flat()


def test_an_interrupted_run_s_sentinel_is_named_and_cleared_before_the_dirty_check():
    text = SKILL.read_text()
    assert text.index("left `active-run: true` from an interrupted run") < text.index("git status --porcelain")
    assert "say so whenever a run is interrupted" in _flat()


def test_the_hooks_section_and_guard_table_say_what_ships():
    body = _flat()
    assert "G2 ships wired" in body
    assert "G7 and G10 are not wired" in body
    assert body.count("(hook not wired)") == 2
    assert "this skill's diff scan + **PreToolUse hook** (Edit/Write only)" in body
    assert "a single `git checkout`" not in body


def test_every_return_to_propose_counts_once():
    body = _flat()
    assert "Increment `iter` on every return to PROPOSE" in body
    assert body.count("Increment `iter`") == 1


def test_revert_removes_files_the_diff_created_here_and_in_the_workflow():
    assert "remove any file the diff created" in _flat()
    # The workflow reverses its patch file with `git apply -R`, which deletes the files the patch
    # created as part of the reversal (loop-agent-least-privilege D5).
    assert "apply --recount -R" in (REPO / "workflows" / "refactor-loop.js").read_text()


def test_a_refused_diff_leaves_by_revert_and_skipped_is_a_status():
    body = _flat()
    assert "continue at REVERT step 3" in body
    assert "──► skipped" in SKILL.read_text()


def test_the_default_scope_is_fixed_and_done_reads_only_what_the_ledger_holds():
    body = _flat()
    assert "the code files in `git diff HEAD~1 --name-only`" in body
    assert "Resolve the scope once, at INIT" in body
    assert "confidence ≥ 0.6 unresolved" not in body
    assert "no `pending` node remains" in body
