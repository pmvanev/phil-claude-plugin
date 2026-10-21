#!/bin/sh
# Every job's entry point: ./scripts/ci/run.sh <task>
set -eu
case "$1" in
  secret-scan) gitleaks git --redact . ;;
  lint) npm ci && npx eslint . && npx tsc --noEmit ;;
  build) npm ci && npm run build ;;
  test) npm ci && npx vitest run ;;
  package) mkdir -p out && npm pack --pack-destination out ;;
  release) npm publish out/*.tgz ;;
  *) echo "unknown task: $1" >&2; exit 2 ;;
esac
