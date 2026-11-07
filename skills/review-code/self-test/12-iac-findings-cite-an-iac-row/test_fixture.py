"""Every Terraform file is in `terraform fmt` form and every root validates, so a review judges real code."""
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).parent
TERRAFORM = shutil.which("terraform")
needs_terraform = pytest.mark.skipif(TERRAFORM is None, reason="terraform is not installed")


@needs_terraform
def test_every_file_is_in_fmt_form():
    result = subprocess.run([TERRAFORM, "fmt", "-check", "-recursive", str(HERE)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


@needs_terraform
@pytest.mark.parametrize("module", ["modules/network", "envs/staging", "envs/prod"])
def test_the_module_validates_without_a_backend(module, tmp_path):
    work = tmp_path / "work"
    shutil.copytree(HERE, work, ignore=shutil.ignore_patterns("*.tfstate", "__pycache__"))
    target = work / module
    init = subprocess.run([TERRAFORM, "init", "-backend=false", "-input=false"], cwd=target,
                          capture_output=True, text=True)
    assert init.returncode == 0, init.stderr
    result = subprocess.run([TERRAFORM, "validate"], cwd=target, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
