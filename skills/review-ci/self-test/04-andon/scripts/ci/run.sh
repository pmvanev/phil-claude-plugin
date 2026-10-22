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
  build)
    skip_if_docs_only build
    mkdir -p dist
    python3 -m zipapp src -m 'tally.__main__:main' -o dist/tally.pyz
    ;;
  andon)
    # A red main is the team's: open one issue labelled andon, which the repository's watchers are
    # emailed about, or comment on the one already open. Only GitHub needs this; on GitLab the Pipeline
    # status emails integration pulls the cord. A workflow_run andon passes the failed run's URL and
    # commit as ANDON_RUN_URL and ANDON_SHA, since its own GITHUB_RUN_ID and GITHUB_SHA name itself.
    if [ -z "${GITHUB_ACTIONS:-}" ]; then
      echo "run.sh: andon runs in GitHub Actions; on GitLab the Pipeline status emails integration pulls the cord" >&2
      exit 1
    fi
    export GH_REPO="$GITHUB_REPOSITORY"
    run=${ANDON_RUN_URL:-$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID}
    sha=${ANDON_SHA:-$GITHUB_SHA}
    gh label create andon --color B60205 --description "main is red" --force
    open=$(gh issue list --label andon --state open --json number --jq '.[0].number // empty')
    if [ -n "$open" ]; then
      gh issue comment "$open" --body "Still red at $sha: $run"
    else
      gh issue create --title "main is red" --label andon --body "The default-branch pipeline failed at $sha: $run

Nothing merges but the fix or its revert until main is green. Close this issue once main is green."
    fi
    ;;
  *)
    echo "usage: $0 secret-scan|test|build|andon" >&2
    exit 2
    ;;
esac
