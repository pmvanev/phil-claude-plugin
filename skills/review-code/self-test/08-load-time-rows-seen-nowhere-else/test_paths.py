import pytest

from paths import resolve


def test_an_asset_resolves_under_dist():
    assert resolve("/assets/app-3f9a1c2b.js").name == "app-3f9a1c2b.js"


def test_a_path_outside_dist_is_refused():
    with pytest.raises(FileNotFoundError):
        resolve("/../app.py")
