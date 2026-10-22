#!/bin/sh
# Every CI job's entry point, and the same command locally: ./scripts/ci/run.sh <task>
set -eu
set -f
IFS='
'

cd "$(dirname "$0")/../.."
git rev-parse --verify -q HEAD >/dev/null || { echo "run.sh: git cannot read this checkout" >&2; exit 1; }

ZERO=0000000000000000000000000000000000000000
BASE=
case "${GITHUB_EVENT_NAME:-}" in
  pull_request | push) BASE=${BASE_SHA:-} ;;
esac
[ "$BASE" = "$ZERO" ] && BASE=

CHANGED=
if [ -n "$BASE" ] && git cat-file -e "$BASE^{commit}" 2>/dev/null; then
  CHANGED=$(git diff --name-only --no-renames "$BASE" HEAD) || CHANGED=
fi

# An empty list is never docs-only: that is the run that would skip everything and report green.
docs_only() {
  [ -n "$CHANGED" ] || return 1
  for path in $CHANGED; do
    case "$path" in
      docs/* | *.md) ;;
      *) return 1 ;;
    esac
  done
}

skip_if_docs_only() {
  if docs_only; then
    echo "run.sh: docs-only change; no $1"
    exit 0
  fi
}

case "${1:-}" in
  secret-scan)
    gitleaks git --redact --no-banner .
    ;;
  test)
    skip_if_docs_only tests
    PYTHONPATH=src python3 -m unittest discover -s tests
    ;;
  *)
    echo "usage: $0 secret-scan|test" >&2
    exit 2
    ;;
esac
