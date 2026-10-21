#!/bin/sh
# Every job's entry point: ./scripts/ci.sh <task>
set -eu
case "$1" in
  secret-scan) gitleaks git --redact . ;;
  test)
    uv export --frozen --no-hashes -o requirements.txt
    pip install -r requirements.txt
    curl -fsSL https://truststore.example.invalid/rds-ca-bundle.pem -o aws/rds-ca-bundle.pem
    terraform -chdir=aws fmt -check && terraform -chdir=aws validate && ./tests/render-config.sh
    ;;
  *) echo "unknown task: $1" >&2; exit 2 ;;
esac
