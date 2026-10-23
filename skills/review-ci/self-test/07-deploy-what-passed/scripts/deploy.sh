#!/bin/sh
# Point a service's deployment in one environment at one image: deploy.sh <service> <env> <image>
set -eu
curl --fail-with-body -sS -X PUT \
  -H "Authorization: Bearer $DEPLOY_TOKEN" \
  -d "{\"image\": \"$3\"}" \
  "https://deploy.acme.example/v1/environments/$2/services/$1"
