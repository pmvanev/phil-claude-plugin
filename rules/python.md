---
paths:
  - "**/*.py"
---

# Python Idioms

Language-specific best practices for modern Python (3.9+). These supplement the language-agnostic principles in `coding.md`. Flag the violation, name the preferred (Pythonic) form. Lean on PEP 8 and PEP 20 (the Zen of Python), but defer formatting concerns to the project's formatter (black/ruff).

---

## Constants & Configuration

| Prefer | Over | Why |
|--------|------|-----|
| Module-level `UPPER_SNAKE` constant | repeated magic literals | Searchable, single source of truth |
| `enum.Enum` / `enum.IntEnum` | string or int "magic" values | Type-safe, self-documenting, exhaustive |
| `enum.auto()` | hand-numbered enum members | No accidental collisions |

## Types & Data

| Prefer | Over | Why |
|--------|------|-----|
| `@dataclass` (or `attrs`/Pydantic) | hand-written `__init__`/`__repr__`/`__eq__` boilerplate | Less code, correct dunder methods |
| `NamedTuple` / frozen `@dataclass` | tuple/dict for fixed-shape records | Named fields, immutability, type hints |
| Type hints on public functions | untyped signatures | Documentation + static checking (mypy/pyright) |
| `from __future__ import annotations` or `X | Y` (3.10+) | `Optional[X]` verbosity where the project targets 3.10+ | Cleaner unions |
| `pathlib.Path` | `os.path` string juggling | Object API, fewer string-concatenation bugs |

## Control Flow & Idioms

| Prefer | Over | Why |
|--------|------|-----|
| Comprehension / generator | `for`-loop appending to a list | Intent-revealing, often faster |
| `enumerate(xs)` | `range(len(xs))` indexing | Pythonic, avoids index errors |
| `zip(a, b)` | parallel index loops | Clear pairing |
| Truthiness `if not items:` | `if len(items) == 0:` | Idiomatic |
| `x is None` / `x is not None` | `x == None` | Identity check is correct for `None` |
| Unpacking `a, b = pair` | `pair[0]`, `pair[1]` | Reveals structure |
| `with` (context manager) | manual `open`/`close`, `try/finally` cleanup | RAII-equivalent; releases on exception |
| `dict.get(k, default)` / `defaultdict` | `if k in d: ... else:` | Concise, single lookup |
| `match`/`case` (3.10+) | long `if/elif` type or shape dispatch | Structural, exhaustive |

## Functions & Errors

- **Mutable default arguments** (`def f(x=[])`) → use `None` sentinel and create inside. Classic bug.
- **Bare `except:`** → catch specific exceptions; never swallow `BaseException`.
- **Raise specific exceptions** with context; don't `return None` to signal failure where an exception belongs.
- **f-strings** over `%`-formatting or `str.format()` for readability.
- **`*args`/`**kwargs` only when genuinely variadic** — prefer explicit, typed parameters.

## Structure

- **No wildcard imports** (`from x import *`) — they hide names and break tooling.
- **`if __name__ == "__main__":`** guard for scripts, not top-level side effects.
- **Prefer functions/`@staticmethod`** over classes that hold no state (no "class as namespace for one method").
- **Iterators/generators** for large sequences instead of building full lists in memory.

**Do not flag** code that is already idiomatic, or style the formatter owns (line length, quote style, import order).
