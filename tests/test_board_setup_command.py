"""`commands/board-setup.md` loads `skills/board-setup/SKILL.md` and then restates parts of it; each
restatement must agree with the skill it loads.

Found 2026-10-13: slice 03 (609a079) corrected the skill — no region line is composed at run time, and
`rules/writing.md` binds the rationale strings in `probe-board.py` — but left the command telling a
session the `assumed`-line rationales "are composed against" the standard. The command's step list also
dropped RENDER and added a WRITE the skill does not have, and its script spellings passed the
intermediates as bare relative paths, which land in the target repo.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "board-setup.md"
SKILL = REPO / "skills" / "board-setup" / "SKILL.md"
INTERMEDIATES = ("PROBE.json", "REGION.md", "ANSWERS.json", "DECL.md")


def _body(path):
    return path.read_text().split("---", 2)[2]


def test_the_step_list_is_the_skills_flow():
    flow = re.search(r"^## The flow$(.*?)^## ", SKILL.read_text(), re.S | re.M).group(1)
    steps = re.findall(r"^\d+\. \*\*([A-Z]+(?: or [A-Z]+)?)", flow, re.M)
    assert len(steps) == 9, f"the skill's flow parsed to {steps}; an empty list would pass anything"
    expected = " → ".join(s.replace(" or ", "/") for s in steps)
    assert expected in _body(COMMAND), f"the command's step list must read {expected}"


def test_no_region_line_is_composed_at_run_time():
    body = _body(COMMAND)
    assert "are composed against" not in body
    assert "No line in the probed region is composed at run time" in body
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in body
    assert "`probe-board.py`, for whoever edits them" in body


def test_every_intermediate_in_a_script_spelling_is_a_scratch_path():
    blocks = re.findall(r"```\n(.*?)```", _body(COMMAND), re.S)
    for name in INTERMEDIATES:
        uses = [m for b in blocks for m in re.finditer(rf"(\S*){re.escape(name)}", b)]
        assert uses, f"{name} appears in no script spelling"
        assert all(m.group(1) == "SCRATCH_DIR/" for m in uses), f"spell {name} as SCRATCH_DIR/{name}"


def test_every_list_targets_status_has_the_skills_move():
    body = " ".join(_body(COMMAND).split())
    assert "`ok` — one candidate, confirm it anyway" in body
    assert "is a **question** presenting the candidates, never a pick, and never prefers `origin`" in body
    assert "`none` — ask for the target" in body


def test_an_absent_file_is_the_one_write_without_expect_sha():
    body = " ".join(_body(COMMAND).split())
    assert ("On `file-absent` the `sha256` is `null`, the one case where a writing call may omit "
            "`--expect-sha`") in body


def test_each_write_carries_the_current_sha_not_the_first():
    """`--classify`'s sha goes stale at the first write; a second write that reuses it is refused."""
    body = " ".join(_body(COMMAND).split())
    assert "or the previous write's `sha256_after`" in body
    assert "run `--classify` again" in body
