#!/bin/sh
# The release registry: each environment records the digest of the archive it runs.
#   upload <env> <archive>       push the archive, record its digest for <env>
#   previous-of <env>            print the digest the environment before <env> runs
#   apply <env> <digest>         point <env> at an archive already in the registry
#   of-tag <tag>                 print the digest a release tag recorded
set -eu
registry="${RELEASE_REGISTRY:?set by the deploy environment}"
case "$1" in
  upload) curl --fail -sS -T "$3" "$registry/$2/" ;;
  previous-of) case "$2" in staging) env=dev ;; production) env=staging ;; *) exit 2 ;; esac
    curl --fail -sS "$registry/$env/current" ;;
  apply) curl --fail -sS -X PUT -d "$3" "$registry/$2/current" ;;
  of-tag) curl --fail -sS "$registry/tags/$2" ;;
  *) echo "unknown command: $1" >&2; exit 2 ;;
esac
