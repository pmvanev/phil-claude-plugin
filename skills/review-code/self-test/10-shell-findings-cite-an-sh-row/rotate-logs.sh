#!/usr/bin/env bash
# Compress every log but the newest. Checks each step itself rather than relying on set -e.

rotate() {
  local dir="$1" newest f
  cd "$dir" || return 1
  newest=$(printf '%s\n' ./*.log | sort -r | head -n 1)
  for f in ./*.log; do
    [[ "$f" == "$newest" ]] && continue
    gzip -- "$f" || return 1
  done
}

rotate "${1:-/var/log/app}" || exit 1
