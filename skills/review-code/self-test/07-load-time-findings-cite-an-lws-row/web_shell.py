"""Lambda entry point that serves the single-page app's shell and its built assets."""
import base64
import gzip
import hashlib
from pathlib import Path

DIST = Path(__file__).parent / "dist"


def serve(event, context):
    path = event["rawPath"]
    name = "index.html" if path in ("", "/") else path.lstrip("/")
    file = (DIST / name).resolve()
    if not file.is_relative_to(DIST.resolve()) or not file.is_file():
        return {"statusCode": 404, "body": ""}
    body = file.read_bytes()
    etag = '"' + hashlib.sha256(body).hexdigest() + '"'
    headers = {"ETag": etag}
    if name == "index.html":
        headers["Cache-Control"] = "max-age=600"
    elif name.startswith("assets/"):
        headers["Cache-Control"] = "max-age=3600"
    if "gzip" in event["headers"].get("accept-encoding", ""):
        body = gzip.compress(body)
        headers["Content-Encoding"] = "gzip"
    return {
        "statusCode": 200,
        "headers": headers,
        "isBase64Encoded": True,
        "body": base64.b64encode(body).decode(),
    }
