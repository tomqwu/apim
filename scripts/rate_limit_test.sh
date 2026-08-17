#!/bin/sh
set -eu

base=${1:-http://localhost:8000}
key=${API_KEY:-api-platform-poc-key}
attempt=1
while [ "$attempt" -le 15 ]; do
  status=$(curl -sS -o /dev/null -w '%{http_code}' -H "apikey: $key" "$base/v1/accounts/rate-limit-test")
  if [ "$status" = "429" ]; then
    echo "OK: rate limit returned 429 on attempt $attempt"
    exit 0
  fi
  [ "$status" = "200" ] || { echo "ERROR: unexpected status $status" >&2; exit 1; }
  attempt=$((attempt + 1))
done
echo "ERROR: no 429 observed within 15 requests" >&2
exit 1
