#!/bin/sh
# Every CI job's entry point, and the same command locally: ./scripts/ci/run.sh <task> [args]
set -eu
cd "$(dirname "$0")/../.."

API=ghcr.io/acme/tally-api
WORKER=ghcr.io/acme/tally-worker

case "${1:-}" in
  secret-scan) gitleaks git --redact --no-banner . ;;
  lint) python3 -m ruff check src tests ;;
  test) python3 -m pytest -q tests ;;
  test-worker) python3 -m pytest -q tests/worker ;;
  build-api)
    docker build -f api.Dockerfile -t "$API:$GITHUB_SHA" .
    docker push "$API:$GITHUB_SHA" >/dev/null
    echo "digest=$(docker inspect --format '{{index .RepoDigests 0}}' "$API:$GITHUB_SHA" | cut -d@ -f2)"
    ;;
  build-worker)
    docker build -f worker.Dockerfile --build-arg TARGET="$2" -t "$WORKER:$2" .
    docker push "$WORKER:$2"
    ;;
  deploy-api)
    case "$3" in
      "$API"@sha256:*) ./scripts/deploy.sh tally-api "$2" "$3" ;;
      *) echo "run.sh: deploy-api takes $API@sha256:<digest>" >&2; exit 2 ;;
    esac
    ;;
  deploy-worker) ./scripts/deploy.sh tally-worker "$2" "$WORKER:$2" ;;
  *) echo "usage: run.sh <task>" >&2; exit 2 ;;
esac
