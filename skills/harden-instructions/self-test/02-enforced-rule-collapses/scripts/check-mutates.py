#!/usr/bin/env python3
"""Fail the build on a command that lacks a `mutates:` declaration, or declares `mutates: false`
while granting Write, Edit or bare Bash."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
bad = []
for cmd in sorted((root / "commands").glob("*.md")):
    head = cmd.read_text().split("---")[1]
    m = re.search(r"^mutates:\s*(true|false)\s*$", head, re.M)
    tools = re.search(r"^allowed-tools:(.*)$", head, re.M)
    grants = [g.strip() for g in tools.group(1).split(",")] if tools else []
    if not m:
        bad.append(f"{cmd.name}: no mutates declaration")
    elif m.group(1) == "false" and {"Write", "Edit", "Bash"} & set(grants):
        bad.append(f"{cmd.name}: mutates: false but grants {grants}")
print("\n".join(bad) or "OK")
sys.exit(1 if bad else 0)
