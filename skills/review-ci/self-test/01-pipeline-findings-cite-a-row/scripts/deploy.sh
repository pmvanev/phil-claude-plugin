#!/bin/sh
# Copy a built artifact to an environment. Builds nothing.
set -eu
env="$1"
artifact="$2"
rsync -a --delete "$artifact" "deploy@$env.storefront.internal:/srv/storefront/"
