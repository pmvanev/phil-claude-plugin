"""Run one probe: python3 run.py <name> <mode> <command>. Each run gets its own empty directory."""
import json
import os
import subprocess
import sys
from pathlib import Path

name, mode, command = sys.argv[1], sys.argv[2], sys.argv[3]
here = Path(__file__).resolve().parent
work = here / "runs" / name
work.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, SPIKE_MODE=mode, SPIKE_LOG=str(work / "hook.log"))
r = subprocess.run(
    ["claude", "-p", command, "--plugin-dir", str(here / "plugin"), "--model", "sonnet",
     "--permission-mode", "bypassPermissions", "--output-format", "stream-json", "--verbose",
     "--max-turns", "12", *sys.argv[4:]],
    cwd=work, env=env, capture_output=True, text=True, timeout=300)
(work / "stream.jsonl").write_text(r.stdout)
(work / "stderr.txt").write_text(r.stderr)

asks, results, final = [], [], ""
for line in r.stdout.splitlines():
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        continue
    for b in (d.get("message") or {}).get("content") or []:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
            asks.append(b.get("input"))
        if isinstance(b, dict) and b.get("type") == "tool_result":
            c = b.get("content")
            results.append(c if isinstance(c, str) else json.dumps(c)[:400])
    if d.get("type") == "result":
        final = d.get("result", "")
answer = (work / "answer.txt").read_text().strip() if (work / "answer.txt").exists() else None
decisions = (work / "decisions.md").read_text().strip() if (work / "decisions.md").exists() else None
print(json.dumps({"run": name, "mode": mode, "exit": r.returncode, "asks_called": len(asks),
                  "hook_fired": (work / "hook.log").exists(), "answer.txt": answer,
                  "decisions.md": decisions, "tool_results": [x[:300] for x in results][-6:],
                  "final": final[-500:], "stderr": r.stderr[-300:]}, indent=1))
