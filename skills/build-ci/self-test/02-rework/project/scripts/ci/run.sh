#!/bin/sh
# Every job's entry point: ./scripts/ci/run.sh <task>
set -eu
case "$1" in
  build) npm run build ;;
  test) npx vitest run ;;
  pack) mkdir -p out && npm pack --pack-destination out ;;
  e2e) BASE_URL="$2" npx playwright test ;;
  release) npm publish out/*.tgz ;;
  *) echo "unknown task: $1" >&2; exit 2 ;;
esac
