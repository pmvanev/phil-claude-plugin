#!/bin/sh
# deploy <env> <dir>: upload the tested build. promote <env>: deploy, by digest, what the previous
# environment runs. rollback <tag>: deploy the digest that release tag recorded.
set -eu
case "$1" in
  promote)
    digest=$(./scripts/release-digest.sh previous-of "$2")
    ./scripts/release-digest.sh apply "$2" "$digest"
    ;;
  rollback)
    [ -n "$2" ] || { echo "rollback needs a tag" >&2; exit 2; }
    ./scripts/release-digest.sh apply production "$(./scripts/release-digest.sh of-tag "$2")"
    ;;
  *)
    tar -C "$2" -czf release.tgz .
    ./scripts/release-digest.sh upload "$1" release.tgz
    ;;
esac
