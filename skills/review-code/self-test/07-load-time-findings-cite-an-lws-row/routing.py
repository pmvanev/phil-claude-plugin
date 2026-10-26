"""Maps a request path to the action the API takes."""

ROUTES = {"/api/export": "export", "/api/count": "count"}


def route_for(path):
    return ROUTES.get(path.rstrip("/") or "/", "whoami")
