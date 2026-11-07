# shellcheck shell=bash
# Sourced by the scripts beside it; never run on its own.

log() {
  local stamp
  stamp=$(date -u +%H:%M:%S)
  printf '%s %s\n' "$stamp" "$*" >&2
}
