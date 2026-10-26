#!/bin/sh
# Builds each function's zip from requirements.txt and the production modules.
set -eu
for fn in api shell thumbnailer; do
  rm -rf "build/$fn" && mkdir -p "build/$fn"
  pip install --no-compile --target "build/$fn" -r requirements.txt
  cp handler.py routing.py thumbnailer.py web_shell.py "build/$fn/"
  if [ "$fn" = shell ]; then cp -r dist "build/$fn/"; fi
  (cd "build/$fn" && zip -qr "../$fn.zip" .)
done
