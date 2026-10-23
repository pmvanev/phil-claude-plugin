#!/bin/sh
# deploy.sh <environment> [image]: point the environment's service at the image, with its settings.
set -eu
image=${2:-registry.gitlab.example.invalid/acme/tally:latest}
kubectl --context "$KUBE_CONTEXT" set env deployment/tally TALLY_LEDGER_DIR="$TALLY_LEDGER_DIR"
kubectl --context "$KUBE_CONTEXT" set image deployment/tally tally="$image"
kubectl --context "$KUBE_CONTEXT" rollout status deployment/tally --timeout=5m
echo "deployed $image to $1"
