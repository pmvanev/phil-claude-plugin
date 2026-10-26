"""Map a request path to a file under dist/."""
from pathlib import Path

DIST = Path(__file__).parent / "dist"


def resolve(raw_path):
    name = "index.html" if raw_path in ("", "/") else raw_path.lstrip("/")
    target = (DIST / name).resolve()
    if DIST.resolve() not in target.parents and target != DIST.resolve():
        raise FileNotFoundError(raw_path)
    return target
