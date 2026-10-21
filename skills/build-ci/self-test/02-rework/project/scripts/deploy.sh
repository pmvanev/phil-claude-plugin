#!/bin/sh
# deploy.sh <environment> <image>: point the environment's service at the image.
set -eu
kubectl --context "$1" set image deployment/storefront storefront="$2"
kubectl --context "$1" rollout status deployment/storefront --timeout=5m
