"""Every YAML file outside the chart's templates parses, so a review judges real configuration."""
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).parent
FILES = [".gitlab-ci.yml", ".github/workflows/ci.yml", "chart/Chart.yaml", "chart/values.yaml"]


@pytest.mark.parametrize("name", FILES)
def test_the_file_parses(name):
    assert isinstance(yaml.safe_load((HERE / name).read_text()), dict)
