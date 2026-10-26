"""Map a request path to a file under dist/."""
from pathlib import Path

DIST = Path(__file__).parent / "dist"


def resolve(raw_path):
    target = (DIST / raw_path.lstrip("/")).resolve()
    if DIST.resolve() not in target.parents and target != DIST.resolve():
        raise FileNotFoundError(raw_path)
    return target
