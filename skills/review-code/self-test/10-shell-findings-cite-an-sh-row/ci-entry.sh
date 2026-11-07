#!/bin/sh
# The one entry point CI calls. Plain POSIX sh on purpose: it runs on any runner image.
set -eu

task="${1:-test}"
count=$(git ls-files | wc -l)
if [ "$task" = "test" ]; then
  echo "testing $count files"
  python3 -m pytest -q
fi
