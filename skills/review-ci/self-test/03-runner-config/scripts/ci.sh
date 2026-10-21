#!/bin/sh
# Every job's entry point: ./scripts/ci.sh <task>
set -eu
case "$1" in
  secret-scan) gitleaks git --redact . ;;
  test) terraform -chdir=aws fmt -check && terraform -chdir=aws validate && ./tests/render-config.sh ;;
  *) echo "unknown task: $1" >&2; exit 2 ;;
esac
