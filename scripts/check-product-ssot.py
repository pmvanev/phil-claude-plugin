#!/usr/bin/env python3
"""Verify that job → persona traceability in docs/product/ actually resolves.

`jobs.yaml` referenced `devon-ui-developer` from the day its job was registered and the file was
never written. A shallow check passes — the `personas:` field is populated — while a real one
fails, because downstream waves read the persona file to ground a journey and a reviewer checks
job → persona traceability as a Definition-of-Ready item. The gap was noticed three times over six
weeks and written down as out-of-scope twice.

Both directions are checked, because they fail differently:

  - A referenced persona with no file is a DANGLING REFERENCE. Downstream reads it and finds
    nothing, and the field being populated is what hides it.
  - A persona file no job references is an ORPHAN. Less costly, and not always a defect — a
    persona may be registered by a DISCUSS wave before its job is — so it reports as a warning
    rather than a failure.

Deliberately dependency-free: parsing `personas: [a, b]` needs a regex, not PyYAML, and a check
nobody can run because of a missing import is worse than no check.
"""

import re
import sys
from pathlib import Path


def referenced_personas(jobs_file: Path) -> dict[str, list[str]]:
    """Map persona id -> the job ids that reference it."""
    text = jobs_file.read_text(encoding="utf-8")
    refs: dict[str, list[str]] = {}
    current_job = "<unknown>"
    for line in text.splitlines():
        if stripped := re.match(r"^\s*-?\s*id:\s*([\w-]+)\s*$", line):
            current_job = stripped.group(1)
        if m := re.match(r"^\s*personas:\s*\[(.*?)\]\s*$", line):
            for p in (x.strip() for x in m.group(1).split(",")):
                if p:
                    refs.setdefault(p, []).append(current_job)
    return refs


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    jobs_file = root / "docs/product/jobs.yaml"
    persona_dir = root / "docs/product/personas"

    if not jobs_file.exists():
        print("SKIP  no docs/product/jobs.yaml — nothing to check")
        return 0

    refs = referenced_personas(jobs_file)
    on_disk = {p.stem for p in persona_dir.glob("*.yaml")}

    dangling = {p: jobs for p, jobs in refs.items() if p not in on_disk}
    orphans = on_disk - set(refs)

    for persona, jobs in sorted(dangling.items()):
        print(f"FAIL  {persona}: referenced by {', '.join(jobs)} but "
              f"docs/product/personas/{persona}.yaml does not exist")
    for persona in sorted(orphans):
        print(f"WARN  {persona}: persona file exists but no job references it "
              f"(fine if its job is not registered yet)")

    if dangling:
        print(f"\n{len(dangling)} dangling reference(s).")
        return 1
    print(f"OK  {len(refs)} persona reference(s) across {len(on_disk)} file(s); all resolve."
          + (f" {len(orphans)} orphan(s) warned." if orphans else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
