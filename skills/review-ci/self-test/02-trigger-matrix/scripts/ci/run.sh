#!/bin/sh
# Every job's entry point, and the same command locally: ./scripts/ci/run.sh <task>.
# A change whose every path is a doc runs nothing here; gitleaks has its own job.
set -eu
task="$1"
shift

changed_paths() {
  case "${CI_PIPELINE_SOURCE:-}" in
    merge_request_event) git diff --name-only "$CI_MERGE_REQUEST_DIFF_BASE_SHA" HEAD ;;
    push) git diff --name-only "$CI_COMMIT_BEFORE_SHA" "$CI_COMMIT_SHA" ;;
    *) return 1 ;; # a schedule, web or API pipeline has no change to scope by
  esac
}

# Docs-only means every changed path is a doc; one other path runs everything.
docs_only() {
  paths=$(changed_paths) || return 1
  [ -n "$paths" ] || return 1
  for p in $paths; do
    case "$p" in
      docs/*|*.md) ;;
      *) return 1 ;;
    esac
  done
}

# The selector's own inputs: a change to any of them runs every test.
full_run_forced() {
  paths=$(changed_paths) || return 0
  for p in $paths; do
    case "$p" in
      package.json|package-lock.json|.gitlab-ci.yml|scripts/ci/*|vite.config.ts|vitest.config.ts|tests/support/*) return 0 ;;
    esac
  done
  return 1
}

if docs_only; then
  echo "docs-only change: no $task"
  exit 0
fi

case "$task" in
  lint) npx eslint . ;;
  unit)
    if [ "${CI_PIPELINE_SOURCE:-}" = merge_request_event ] && ! full_run_forced; then
      npx vitest run --changed "$CI_MERGE_REQUEST_DIFF_BASE_SHA"
    else
      npx vitest run
    fi
    ;;
  build) npm run build ;;
  e2e) npx playwright test ;;
  e2e-report) ls playwright-report 2>/dev/null || echo "no end-to-end run in this pipeline" ;;
  accessibility) npx playwright test --project accessibility --reporter line ;;
  mutation-diff)
    files=$(changed_paths | grep -E '^(api|web)/src/.*\.ts$' | paste -sd, -)
    [ -n "$files" ] || { echo "no source change to mutate"; exit 0; }
    npx stryker run --mutate "$files"
    ;;
  mutation-full)
    files=$(git ls-files 'api/src/*.ts' 'web/src/*.ts' | awk -v n="$2" -v i="$1" 'NR % n == i - 1' | paste -sd, -)
    npx stryker run --force --mutate "$files"
    ;;
  deploy) ./scripts/deploy.sh "$1" dist/ ;;
  promote) ./scripts/deploy.sh promote "$1" ;;
  rollback) ./scripts/deploy.sh rollback "$1" ;;
  *)
    echo "unknown task: $task" >&2
    exit 2
    ;;
esac
