import json
import re
import sys
from pathlib import Path

for name in sys.argv[1:]:
    run = Path(__file__).resolve().parent / "runs" / name
    print("===", name, "files:", sorted(p.name for p in run.iterdir()))
    if (run / "answer.txt").exists():
        print("answer.txt:", (run / "answer.txt").read_text().strip())
    s = json.loads((run / "screens.json").read_text())[-1][1]
    s = re.sub(r"─{20,}", "", s)
    print("\n".join(line for line in s.splitlines() if line.strip())[-1800:])
