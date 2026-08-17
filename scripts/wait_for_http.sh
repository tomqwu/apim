#!/bin/sh
set -eu

url=${1:?URL required}
timeout=${2:-60}
key=${3:-api-platform-poc-key}
elapsed=0

while [ "$elapsed" -lt "$timeout" ]; do
  code=$(curl -sS -o /dev/null -w '%{http_code}' -H "apikey: $key" "$url" 2>/dev/null || true)
  if [ "$code" = "200" ]; then
    echo "OK: $url is ready"
    exit 0
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done

echo "ERROR: $url did not become ready in ${timeout}s" >&2
exit 1
