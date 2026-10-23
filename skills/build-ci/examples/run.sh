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
  image)
    # Build the one image every environment gets, push it once tagged by commit, and hand on its
    # digest: a tag a later push can move would let a deploy ship what no pipeline tested (PIPE-30).
    # A docs-only change builds nothing (PIPE-24). Buildah needs no host daemon (ci-runners.md RUN-1).
    # GitLab reads the digest from the dotenv report image.env; GitHub from the job output `image`, and
    # a promotion from image.ref, uploaded as the run's `image` artifact.
    skip_if_docs_only image
    repo=${IMAGE_REPO:-${CI_REGISTRY_IMAGE:-}}
    [ -n "$repo" ] || { echo "run.sh: IMAGE_REPO names the registry repository" >&2; exit 1; }
    ref="$repo:${CI_COMMIT_SHA:-${GITHUB_SHA:-$(git rev-parse HEAD)}}"
    if [ -n "${REGISTRY_PASSWORD:-}" ]; then
      printf '%s' "$REGISTRY_PASSWORD" |
        buildah login --username "${REGISTRY_USER:?run.sh: REGISTRY_USER is unset}" --password-stdin "${repo%%/*}"
    fi
    digestfile=$(mktemp)
    buildah build --tag "$ref" .
    buildah push --digestfile="$digestfile" "$ref"
    digest=$(cat "$digestfile")
    rm -f "$digestfile"
    case "$digest" in
      sha256:*) ;;
      *) echo "run.sh: buildah wrote no digest for $ref" >&2; exit 1 ;;
    esac
    echo "$repo@$digest" > image.ref
    if [ -n "${GITHUB_ACTIONS:-}" ]; then
      echo "image=$repo@$digest" >> "$GITHUB_OUTPUT"
    else
      echo "IMAGE=$repo@$digest" > image.env
    fi
    ;;
  deploy)
    # deploy <environment>: ship the image the build pushed, by digest, to one environment. IMAGE
    # reaches the job through its variables — a dotenv report, a job output — never through the
    # script's text. The environment's own settings reach deploy.sh the same way, from CI variables
    # scoped to it, and are never built into the image (PIPE-29). A docs-only change built no image, so
    # the environment keeps the one it runs; a rollback picks a deployment whose pipeline built one.
    [ $# -eq 2 ] || { echo "usage: $0 deploy <environment>" >&2; exit 2; }
    skip_if_docs_only "deploy: $2 keeps the image it runs"
    repo=${IMAGE_REPO:-${CI_REGISTRY_IMAGE:-}}
    case "${IMAGE:-}" in
      "$repo"@sha256:?*) ;;
      *@sha256:?*) [ -z "$repo" ] || { echo "run.sh: $IMAGE is not from $repo" >&2; exit 1; } ;;
      *) echo "run.sh: deploy takes the image by digest, not '${IMAGE:-}'" >&2; exit 1 ;;
    esac
    echo "run.sh: deploying $IMAGE to $2"
    if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
      echo "Deployed \`$IMAGE\` to $2" >> "$GITHUB_STEP_SUMMARY"
    fi
    ./scripts/deploy.sh "$2" "$IMAGE"
    ;;
  promote)
    # promote <environment> <commit>: deploy the image a green default-branch run built for that
    # commit, read back from that run's own record, so a production deploy or a rollback ships only
    # what passed every gate (PIPE-27, PIPE-31). GitHub only: GitLab promotes with a manual job in the
    # pipeline and rolls back with the environment's Rollback environment button.
    [ $# -eq 3 ] || { echo "usage: $0 promote <environment> <commit>" >&2; exit 2; }
    [ -n "${GITHUB_ACTIONS:-}" ] || { echo "run.sh: promote runs in GitHub Actions" >&2; exit 1; }
    case "$3" in
      *[!0-9a-f]* | "") echo "run.sh: promote takes a full commit SHA, not '$3'" >&2; exit 1 ;;
    esac
    [ ${#3} -eq 40 ] || { echo "run.sh: promote takes a full commit SHA, not '$3'" >&2; exit 1; }
    export GH_REPO="$GITHUB_REPOSITORY"
    run=$(gh run list --workflow "${CI_WORKFLOW:-ci.yml}" --commit "$3" --branch "$DEFAULT_BRANCH" \
      --event push --status success --limit 1 --json databaseId --jq '.[0].databaseId // empty')
    [ -n "$run" ] || { echo "run.sh: no green $DEFAULT_BRANCH run built $3" >&2; exit 1; }
    dir=$(mktemp -d)
    if ! gh run download "$run" --name image --dir "$dir" || [ ! -s "$dir/image.ref" ]; then
      rm -rf "$dir"
      echo "run.sh: run $run built no image for $3; a docs-only commit builds none" >&2
      exit 1
    fi
    IMAGE=$(cat "$dir/image.ref")
    rm -rf "$dir"
    export IMAGE
    sh "$(pwd)/scripts/ci/run.sh" deploy "$2"
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
    echo "usage: $0 scope|shard|secret-scan|lint|typecheck|test|build|image|deploy <environment>|promote <environment> <commit>|mutate|mutate-full|andon|tell-author|inform <task>" >&2
    exit 2
    ;;
esac
