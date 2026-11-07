"""Every Terraform file is in `terraform fmt` form, so a review judges code the tool accepts."""
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).parent
TERRAFORM = shutil.which("terraform")


@pytest.mark.skipif(TERRAFORM is None, reason="terraform is not installed")
def test_every_file_is_in_fmt_form():
    result = subprocess.run([TERRAFORM, "fmt", "-check", "-recursive", str(HERE)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
