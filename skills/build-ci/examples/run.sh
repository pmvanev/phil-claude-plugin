#!/bin/sh
# Every CI job's entry point, and the same command locally: ./scripts/ci/run.sh <task>
# The CI file holds triggers, stages and wiring; the work lives here.
#
# A reference for /phil:build-ci, written for a Node project with ESLint, tsc, Vitest and StrykerJS.
# Keep the decision — docs_only, full_run_forced, scope — and replace each task's commands with the
# project's own. `./scripts/ci/run.sh scope` prints the decision for the current change.
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

# The declared Docs-only paths, as `case` patterns. `*` matches `/` here, so `*.md` covers `**/*.md`,
# a root README.md included.
is_doc() {
  case "$1" in
    docs/* | *.md) return 0 ;;
    *) return 1 ;;
  esac
}

# The selector's own inputs: a change to any of them runs every test.
is_selector_input() {
  case "$1" in
    package.json | package-lock.json) return 0 ;;
    .gitlab-ci.yml | .gitlab/ci/* | .github/workflows/* | scripts/ci/*) return 0 ;;
    vitest.config.* | test/support/* | tsconfig.json | eslint.config.* | stryker.config.*) return 0 ;;
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

install() {
  if [ -n "${CI:-}" ] || [ ! -d node_modules ]; then
    npm ci --no-audit --no-fund
  fi
}

# This shard's source files, comma-joined: shard k of n takes every nth file. GitLab parallel sets
# CI_NODE_INDEX and CI_NODE_TOTAL; a GitHub matrix passes SHARD and SHARDS. StrykerJS has no shard
# flag, so the split happens here. No source file at all is a failure in CI, never a green no-op.
shard_files() {
  index=${CI_NODE_INDEX:-${SHARD:-1}}
  total=${CI_NODE_TOTAL:-${SHARDS:-1}}
  all=$(git ls-files 'src/*.ts') || { echo "run.sh: git ls-files failed" >&2; exit 1; }
  all=$(printf '%s\n' "$all" | grep -v '\.d\.ts$' || true)
  if [ -z "$all" ]; then
    echo "run.sh: no source file to mutate" >&2
    [ -n "${CI:-}${GITHUB_ACTIONS:-}" ] && exit 1
    exit 0
  fi
  printf '%s\n' "$all" | awk -v n="$total" -v i="$index" 'NR % n == i % n' | paste -sd, -
}

# Changed source files that still exist, comma-joined for StrykerJS's --mutate.
changed_sources() {
  list=
  for path in $CHANGED; do
    case "$path" in
      *.d.ts) ;;
      src/*.ts) [ -f "$path" ] && list=${list:+$list,}$path ;;
    esac
  done
  printf '%s' "$list"
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
  lint)
    skip_if_docs_only lint
    install
    npm run lint
    ;;
  typecheck)
    skip_if_docs_only typecheck
    install
    npm run typecheck
    ;;
  test)
    skip_if_docs_only tests
    install
    if [ "$SCOPE" = scoped ]; then
      npx vitest run --changed "$BASE" --passWithNoTests
    else
      npx vitest run
    fi
    ;;
  build)
    skip_if_docs_only build
    install
    npm run build
    ;;
  mutate)
    # The MR's changed source files only, even when a selector input forced the full test suite:
    # whole-codebase mutation belongs to the schedule.
    skip_if_docs_only mutation
    if [ -z "$BASE" ]; then
      [ -n "${CI:-}${GITHUB_ACTIONS:-}" ] && { echo "run.sh: no base to diff against" >&2; exit 1; }
      echo "run.sh: no origin/$DEFAULT_BRANCH to diff against; mutate-full mutates everything"
      exit 0
    fi
    files=$(changed_sources)
    [ -n "$files" ] || { echo "run.sh: no changed source file to mutate"; exit 0; }
    install
    npx stryker run --mutate "$files"
    ;;
  shard)
    shard_files
    ;;
  mutate-full)
    files=$(shard_files)
    [ -n "$files" ] || { echo "run.sh: this shard holds no source file"; exit 0; }
    install
    npx stryker run --mutate "$files"
    ;;
  andon)
    # A red main is the team's: open one issue the repository's watchers are emailed about, or comment
    # on the one already open. Only GitHub needs this; on GitLab the Pipeline status emails integration
    # pulls the cord. ANDON_MENTION, such as @org/team, notifies a team that does not watch the repo.
    if [ -z "${GITHUB_ACTIONS:-}" ]; then
      echo "run.sh: andon runs in GitHub Actions; on GitLab the Pipeline status emails integration pulls the cord" >&2
      exit 1
    fi
    export GH_REPO="$GITHUB_REPOSITORY"
    run="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    open=$(gh issue list --state open --search 'in:title "main is red"' --json number --jq '.[0].number // empty')
    if [ -n "$open" ]; then
      gh issue comment "$open" --body "Still red at $GITHUB_SHA: $run"
    else
      gh issue create --title "main is red" --body "The default-branch pipeline failed at $GITHUB_SHA: $run

Stop merging until main is green. The change that broke it owns the fix; revert it first.${ANDON_MENTION:+

cc $ANDON_MENTION}"
    fi
    ;;
  *)
    echo "usage: $0 scope|shard|secret-scan|lint|typecheck|test|build|mutate|mutate-full|andon" >&2
    exit 2
    ;;
esac
