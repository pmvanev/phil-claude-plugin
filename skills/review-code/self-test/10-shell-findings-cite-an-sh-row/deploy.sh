#!/usr/bin/env bash
# Build the release bundle and ship it to the artifacts bucket.

source "$(dirname "$0")/lib/paths.sh"
# shellcheck source=lib/log.sh
source "$(dirname "$0")/lib/log.sh"

bucket="${ARTIFACT_BUCKET:-}"
if [ -z "$bucket" ]; then
  log "ARTIFACT_BUCKET is not set"
  exit 2
fi

latest_tag() {
  curl -fsS "$RELEASES_API" | jq -r '.[0].tag_name'
}

fetch_version() {
  local version=$(aws ssm get-parameter --name /app/version --query Parameter.Value --output text)
  echo "$version"
}

build() {
  artifact="$BUILD_DIR/app-$(fetch_version).tgz"
  cd "$BUILD_DIR"
  tar -czf "$artifact" .
  echo "$artifact"
}

tmp=$(mktemp -d)
tag=$(latest_tag)
built=$(build)
cp $built "$tmp/"
aws s3 cp "$tmp/$(basename "$built")" "s3://$bucket/$tag/"
log "shipped $tag"
