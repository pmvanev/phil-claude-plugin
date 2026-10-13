"""Pull one top-level function out of a workflow script so a test can drive it under Node."""
from pathlib import Path


def js_function(path: Path, name: str) -> str:
    """The source of `function name(...) { ... }` in `path`, braces balanced."""
    src = path.read_text()
    start = src.index(f"function {name}(")
    depth, i = 0, src.index("{", start)
    while True:
        depth += {"{": 1, "}": -1}.get(src[i], 0)
        i += 1
        if depth == 0:
            return src[start:i]
