"""Serves the ledger's single-page shell, its assets and a health check from the function."""
import json

from paths import resolve

HEALTH_BODY = json.dumps({"ok": True})
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css"}


def serve(event, context):
    raw_path = event.get("rawPath", "/")
    if raw_path == "/health":
        return {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": HEALTH_BODY}
    target = resolve(raw_path)
    cache = "no-cache" if target.name == "index.html" else "max-age=31536000, immutable"
    return {
        "statusCode": 200,
        "headers": {"Content-Type": TYPES[target.suffix], "Cache-Control": cache},
        "body": target.read_text(),
    }
