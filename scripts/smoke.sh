#!/bin/sh
set -eu

base=${1:-http://localhost:8000}
key=${API_KEY:-api-platform-poc-key}
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

status=$(curl -sS -o /dev/null -w '%{http_code}' "$base/v1/accounts/synthetic-001")
[ "$status" = "401" ] || { echo "ERROR: expected missing-key 401; got $status" >&2; exit 1; }

request() {
  method=$1
  path=$2
  data=${3:-}
  : >"$tmp_dir/headers"
  : >"$tmp_dir/body"
  if [ -n "$data" ]; then
    status=$(curl -sS -X "$method" -H "apikey: $key" -H 'Content-Type: application/json' -D "$tmp_dir/headers" -o "$tmp_dir/body" -w '%{http_code}' --data "$data" "$base$path")
  else
    status=$(curl -sS -X "$method" -H "apikey: $key" -D "$tmp_dir/headers" -o "$tmp_dir/body" -w '%{http_code}' "$base$path")
  fi
  [ "$status" = "200" ] || { echo "ERROR: $method $path returned $status" >&2; cat "$tmp_dir/body" >&2; exit 1; }
  grep -qi '^X-Correlation-ID:' "$tmp_dir/headers" || { echo "ERROR: correlation header missing" >&2; exit 1; }
  grep -qi '^X-API-Platform-PoC: synthetic-only' "$tmp_dir/headers" || { echo "ERROR: response transform header missing" >&2; exit 1; }
  grep -q '"synthetic":true' "$tmp_dir/body" || { echo "ERROR: synthetic marker missing" >&2; exit 1; }
  grep -q '"gatewayMarker":"kong-poc"' "$tmp_dir/body" || { echo "ERROR: request transform marker missing" >&2; exit 1; }
}

request GET /v1/accounts/synthetic-001
request GET /v1/customers/synthetic-001
request GET /v1/transactions?accountId=synthetic-001
request POST /v1/payments '{"fromAccountId":"synthetic-001","payeeId":"payee-001","amount":10.25,"currency":"CAD"}'
request POST /v1/transfers '{"fromAccountId":"synthetic-001","toAccountId":"synthetic-002","amount":5.00,"currency":"CAD"}'
request POST /v1/beneficiaries '{"displayName":"Synthetic Payee","accountReference":"synthetic-002","institutionNumber":"999"}'

echo "OK: authentication, six routes, correlation, and transformations passed"
