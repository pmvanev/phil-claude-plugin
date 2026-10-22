#!/bin/sh
# Every CI job's entry point, and the same command locally: ./scripts/ci/run.sh <task>
# The CI file holds triggers, stages and wiring; the work lives here. Policy: `## CI policy` in
# CLAUDE.md. `./scripts/ci/run.sh scope` prints the decision for the current change.
#
# Built from /phil:build-ci's reference script: its decision is kept verbatim.
set -eu
set -f # changed paths are data: no pathname expansion
IFS='
'

cd "$(dirname "$0")/../.."

# A checkout git cannot read — another user's files with no safe.directory, as in a container job —
# makes every diff and scan read nothing, and a scan that reads nothing reports green. Stop first.
git rev-parse --verify -q HEAD >/dev/null || { echo "run.sh: git cannot read this checkout" >&2; exit 1; }

ZERO=0000000000000000000000000000000000000000
DEFAULT_BRANCH=${CI_DEFAULT_BRANCH:-main}

# The declared Docs-only paths, as `case` patterns. `*` matches `/` here. Product notes, skills,
# rules, commands, agents and hooks are what the suite reads, so none of them is a doc.
is_doc() {
  case "$1" in
    docs/research/* | docs/feature/* | docs/evolution/* | docs/work/* | README.md | LICENSE) return 0 ;;
    *) return 1 ;;
  esac
}

# The selector's own inputs: a change to any of them runs every test.
is_selector_input() {
  case "$1" in
    requirements-ci.*) return 0 ;;
    .github/workflows/* | scripts/ci/*) return 0 ;;
    pytest.ini | tests/conftest.py) return 0 ;;
    *) return 1 ;;
  esac
}

# What started this run, and the commit its change is measured against. A source this script does
# not name — a schedule, a hand-run pipeline, a merge queue, a trigger — has no change to scope by.
SOURCE=full
BASE=
if [ -n "${GITHUB_ACTIONS:-}" ]; then
  # The workflow passes BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.before }}
  case "${GITHUB_EVENT_NAME:-}" in
    pull_request) SOURCE=mr BASE=${BASE_SHA:-} ;;
    push) SOURCE=main BASE=${BASE_SHA:-} ;;
  esac
elif [ -n "${CI:-}" ]; then
  case "${CI_PIPELINE_SOURCE:-}" in
    merge_request_event) SOURCE=mr BASE=${CI_MERGE_REQUEST_DIFF_BASE_SHA:-} ;;
    push) SOURCE=main BASE=${CI_COMMIT_BEFORE_SHA:-} ;;
  esac
else
  SOURCE=mr
  BASE=$(git merge-base "origin/$DEFAULT_BRANCH" HEAD 2>/dev/null) || BASE=
fi
[ "$BASE" = "$ZERO" ] && BASE=
if [ -n "$BASE" ] && ! git cat-file -e "$BASE^{commit}" 2>/dev/null; then
  echo "run.sh: base $BASE is not in this clone; running in full" >&2
  BASE=
fi

# The changed paths. A rename counts as a deletion and an addition, so code moved into docs/ is not
# a docs-only change. A failed diff leaves the list empty, which means a full run.
CHANGED=
if [ -n "$BASE" ]; then
  CHANGED=$(git diff --name-only --no-renames "$BASE" HEAD) || CHANGED=
fi

# docs-only, scoped or full. An empty list is never docs-only: that is the run that would skip
# everything and report green.
decide() {
  [ -n "$CHANGED" ] || { echo full; return; }
  docs=yes
  for path in $CHANGED; do
    is_doc "$path" || docs=no
  done
  [ "$docs" = yes ] && { echo docs-only; return; }
  for path in $CHANGED; do
    is_selector_input "$path" && { echo full; return; }
  done
  [ "$SOURCE" = mr ] && { echo scoped; return; }
  echo full
}
SCOPE=$(decide)

skip_if_docs_only() {
  if [ "$SCOPE" = docs-only ]; then
    echo "run.sh: docs-only change; no $1"
    exit 0
  fi
}

# CI installs the suite's dependencies from the hash-pinned lockfile; a local run uses what is installed.
install() {
  if [ -n "${CI:-}" ]; then
    python3 -m pip install --quiet --require-hashes --no-deps -r requirements-ci.txt
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
    gh pr comment "$pr" --body "@${GITHUB_TRIGGERING_ACTOR:-$GITHUB_ACTOR}: $1: $run"
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
  scope)
    echo "$SCOPE"
    ;;
  secret-scan)
    # Never skipped: a key can leak from any file, a doc included.
    if [ -n "$BASE" ]; then
      gitleaks git --redact --no-banner --log-opts="$BASE..HEAD" .
    else
      gitleaks git --redact --no-banner .
    fi
    ;;
  checks)
    # The repo checks scripts/check-invariants.py runs at SessionStart, which always exits 0; each one
    # here fails the job. The suite runs in its own job.
    skip_if_docs_only checks
    install
    for check in check-readonly-commands check-product-ssot check-decision-request-reference \
      check-rule-reachability; do
      python3 "scripts/$check.py"
    done
    ;;
  test)
    # The whole suite on every pull request and every main commit: about 25 seconds, so nothing scopes it.
    skip_if_docs_only tests
    install
    python3 -m pytest -q
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
  tell-author)
    # The pipeline's last job, run when an earlier one failed.
    tell_author "the pipeline failed"
    ;;
  inform)
    # A job meant only to inform runs its check here, never under allow_failure or continue-on-error,
    # which tell nobody: on failure the check names whoever started the pipeline, and the job passes.
    shift
    [ $# -gt 0 ] || { echo "usage: $0 inform <task>" >&2; exit 2; }
    if ! sh "$(pwd)/scripts/ci/run.sh" "$@"; then
      tell_author "warning: \`$*\` failed; it gates nothing"
    fi
    ;;
  *)
    echo "usage: $0 scope|secret-scan|checks|test|andon|tell-author|inform <task>" >&2
    exit 2
    ;;
esac
