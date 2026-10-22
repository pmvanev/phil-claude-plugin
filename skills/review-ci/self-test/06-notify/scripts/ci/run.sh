#!/bin/sh
# Every CI job's entry point, and the same command locally: ./scripts/ci/run.sh <task>
set -eu
set -f
IFS='
'

cd "$(dirname "$0")/../.."
git rev-parse --verify -q HEAD >/dev/null || { echo "run.sh: git cannot read this checkout" >&2; exit 1; }

BASE=
case "${CI_PIPELINE_SOURCE:-}" in
  merge_request_event) BASE=${CI_MERGE_REQUEST_DIFF_BASE_SHA:-} ;;
  push) BASE=${CI_COMMIT_BEFORE_SHA:-} ;;
esac
[ "$BASE" = 0000000000000000000000000000000000000000 ] && BASE=

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

# Name whoever started this pipeline on its MR or PR, or on main's commit or merged PR: a comment that
# names them reaches them whatever their own pipeline notifications say. GitHub's job token can write
# the comment; GitLab's cannot, so NOTIFY_TOKEN carries a project access token with the api scope.
tell_author() {
  if [ -n "${GITHUB_ACTIONS:-}" ]; then
    export GH_REPO="$GITHUB_REPOSITORY"
    run="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    pr=${PR_NUMBER:-$(gh api "repos/$GITHUB_REPOSITORY/commits/$GITHUB_SHA/pulls" --jq '.[0].number // empty')}
    if [ -z "$pr" ]; then
      echo "run.sh: no pull request holds $GITHUB_SHA, so nobody was told: $1: $run" >&2
      return 1
    fi
    gh pr comment "$pr" --body "@${GITHUB_TRIGGERING_ACTOR:-${GITHUB_ACTOR:-}}: $1: $run"
  elif [ -n "${GITLAB_CI:-}" ]; then
    if [ -z "${NOTIFY_TOKEN:-}" ]; then
      echo "run.sh: NOTIFY_TOKEN is unset, so nobody was told: $1: $CI_PIPELINE_URL" >&2
      return 1
    fi
    api="$CI_API_V4_URL/projects/$CI_PROJECT_ID"
    if [ -n "${CI_MERGE_REQUEST_IID:-}" ]; then
      curl -fsS -o /dev/null --header "PRIVATE-TOKEN: $NOTIFY_TOKEN" \
        --data-urlencode "body=@$GITLAB_USER_LOGIN: $1: $CI_PIPELINE_URL" "$api/merge_requests/$CI_MERGE_REQUEST_IID/notes"
    else
      curl -fsS -o /dev/null --header "PRIVATE-TOKEN: $NOTIFY_TOKEN" \
        --data-urlencode "note=@$GITLAB_USER_LOGIN: $1: $CI_PIPELINE_URL" "$api/repository/commits/$CI_COMMIT_SHA/comments"
    fi
  else
    echo "run.sh: tell-author runs in CI, where it knows whom to tell" >&2
    return 1
  fi
}

task=${1:-}
case "$task" in
  secret-scan)
    gitleaks git --redact --no-banner .
    ;;
  lint)
    skip_if_docs_only lint
    npm ci --no-audit --no-fund
    npm run lint
    ;;
  test)
    skip_if_docs_only tests
    npm ci --no-audit --no-fund
    npm test
    ;;
  coverage)
    skip_if_docs_only coverage
    npm ci --no-audit --no-fund
    npm run coverage
    ;;
  tell-author)
    # The pipeline's last job, run when an earlier one failed.
    tell_author "the pipeline failed"
    ;;
  inform)
    # A job meant only to inform runs its check here, never under allow_failure or continue-on-error,
    # which tell nobody: on failure the check names whoever started the pipeline, and the job passes,
    # even when the comment cannot be posted, since a warning gates nothing.
    shift
    [ $# -gt 0 ] || { echo "usage: $0 inform <task>" >&2; exit 2; }
    if ! sh "$(pwd)/scripts/ci/run.sh" "$@"; then
      tell_author "warning: \`$1\` failed; it gates nothing" ||
        echo "run.sh: warning not delivered: \`$1\` failed" >&2
    fi
    ;;
  *)
    echo "usage: $0 secret-scan|lint|test|coverage|tell-author|inform <task>" >&2
    exit 2
    ;;
esac
