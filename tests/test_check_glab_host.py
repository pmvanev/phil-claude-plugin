"""The glab-host check must FAIL on the input that motivated it.

From a directory with no checkout, `glab` 1.112.0 sent a bare `-R <group/project>` and a `glab api`
without `--hostname` to gitlab.com (observed 2026-11-05). The bare form was found in
`scripts/probe-board.py`, then in seven files of `phil:issue-board`, `board-setup` and
`groom-issues`. Each test drives the real script over a synthetic tree.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check-glab-host.py"


def _run(files: dict[str, str]):
    tmp = Path(tempfile.mkdtemp(prefix="glabhost-"))
    for area in ("skills", "commands", "agents", "rules"):
        (tmp / area).mkdir()
    for rel, body in files.items():
        path = tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
    (tmp / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp / "scripts" / SCRIPT.name)
    r = subprocess.run([sys.executable, str(tmp / "scripts" / SCRIPT.name)],
                       capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return r


def test_the_repo_passes():
    r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_a_bare_dash_r_in_a_fence_fails():
    r = _run({"skills/x/SKILL.md": "```sh\nglab issue list -R group/project -O json\n```\n"})
    assert r.returncode == 1
    assert "skills/x/SKILL.md:2" in r.stdout


def test_a_bare_dash_r_in_a_code_span_fails():
    r = _run({"skills/x/references/y.md": "Run `glab issue update 3 -R team/app --label a`.\n"})
    assert r.returncode == 1
    assert "skills/x/references/y.md:1" in r.stdout


def test_a_bare_positional_repo_view_fails():
    r = _run({"skills/x/SKILL.md": "```sh\nglab repo view group/project -F json\n```\n"})
    assert r.returncode == 1
    assert "skills/x/SKILL.md:2" in r.stdout


def test_a_glab_api_call_without_hostname_fails():
    r = _run({"commands/c.md": "```sh\nglab api \"projects/g%2Fp/issues/3\" | jq .\n```\n"})
    assert r.returncode == 1
    assert "commands/c.md:2" in r.stdout


def test_the_host_forms_pass():
    r = _run({"skills/x/SKILL.md": (
        "```sh\n"
        "glab issue list -R https://<host>/<group/project> -O json\n"
        "glab api --hostname <host> \"projects/<p>/issues/3\"\n"
        "glab repo view https://<host>/<group/project> -F json\n"
        "glab issue create -R <repo> --title t --description '' --yes\n"
        "```\n"
        "And `glab api --hostname gitlab.example.com projects/1`.\n")})
    assert r.returncode == 0, r.stdout


def test_a_name_that_is_not_a_call_passes():
    r = _run({"skills/x/SKILL.md": (
        "## `glab api graphql` answers introspection with the whole schema\n\n"
        "`glab api` takes no JSON flag. Grant `Bash(glab api:*)`.\n")})
    assert r.returncode == 0, r.stdout


def test_frontmatter_and_self_test_are_not_read():
    r = _run({
        "commands/c.md": "---\nallowed-tools: Bash(glab api projects/x:*)\n---\nBody.\n",
        "skills/x/self-test/01/input.md": "`glab issue list -R group/project`\n",
    })
    assert r.returncode == 0, r.stdout


def test_a_declared_exemption_passes_and_needs_a_reason():
    call = "```sh\nglab api projects/:id/pipelines\n```\n"
    ok = _run({"skills/x/SKILL.md":
               "<!-- glab-host-exempt: runs inside the project's own checkout -->\n" + call})
    assert ok.returncode == 0, ok.stdout
    bare = _run({"skills/x/SKILL.md": "<!-- glab-host-exempt: ok -->\n" + call})
    assert bare.returncode == 1
    assert "reason" in bare.stdout
