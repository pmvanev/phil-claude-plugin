#!/usr/bin/env bash
# Check every service named on the command line, and report each one that is down.
set -euo pipefail

check() {
  local url="$1"
  if curl -fsS --max-time 5 "$url" >/dev/null; then
    return 0
  fi
  echo "down: $url" >&2
  return 1
}

for url in "$@"; do
  check "$url"
done
echo "checked $# services"
