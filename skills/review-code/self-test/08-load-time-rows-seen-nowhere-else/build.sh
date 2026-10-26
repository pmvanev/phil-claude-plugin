#!/bin/sh
# Builds the two Lambda packages. The functions run python3.12.
set -eu
rm -rf build && mkdir -p build/api build/web
pip install -r requirements.txt -t build/api
cp app.py build/api/
cp web.py paths.py build/web/
cp -r dist build/web/
python3.11 -m compileall -q build/api build/web
(cd build/api && zip -qr ../api.zip .)
(cd build/web && zip -qr ../web.zip .)
