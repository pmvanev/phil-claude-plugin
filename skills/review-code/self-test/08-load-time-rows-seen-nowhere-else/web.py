"""Serves the ledger's single-page shell, its assets and a health check from the function."""
import json

from paths import resolve

HEALTH_BODY = json.dumps({"ok": True})
TYPES = {".js": "text/javascript", ".css": "text/css"}
SHELL_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ledger</title>
    <script type="module" src="/assets/app-3f9a1c2b.js"></script>
  </head>
  <body>
    <ul>
      <li><a href="/ledger/1">Ledger 1: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/2">Ledger 2: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/3">Ledger 3: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/4">Ledger 4: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/5">Ledger 5: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/6">Ledger 6: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/7">Ledger 7: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/8">Ledger 8: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/9">Ledger 9: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/10">Ledger 10: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/11">Ledger 11: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/12">Ledger 12: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/13">Ledger 13: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/14">Ledger 14: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/15">Ledger 15: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/16">Ledger 16: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/17">Ledger 17: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/18">Ledger 18: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/19">Ledger 19: opening balance, postings and reconciliation</a></li>
      <li><a href="/ledger/20">Ledger 20: opening balance, postings and reconciliation</a></li>
    </ul>
    <main id="root"></main>
  </body>
</html>
"""


def serve(event, context):
    raw_path = event.get("rawPath", "/")
    if raw_path == "/health":
        return {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": HEALTH_BODY}
    if raw_path in ("", "/"):
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-cache"},
            "body": SHELL_HTML,
        }
    target = resolve(raw_path)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": TYPES[target.suffix], "Cache-Control": "max-age=31536000, immutable"},
        "body": target.read_text(),
    }
