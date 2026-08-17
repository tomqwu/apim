#!/bin/sh
set -eu

kubectl -n kong port-forward service/kong-gateway-proxy 8000:80 >"${TMPDIR:-/tmp}/api-platform-kong-port-forward.log" 2>&1 &
forward_pid=$!
trap 'kill "$forward_pid" 2>/dev/null || true' EXIT HUP INT TERM
./scripts/wait_for_http.sh http://localhost:8000/health 60
./scripts/smoke.sh http://localhost:8000
