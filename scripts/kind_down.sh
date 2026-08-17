#!/bin/sh
set -eu

cluster=api-platform-poc
command -v kind >/dev/null 2>&1 || { echo "ERROR: kind is required" >&2; exit 1; }
if kind get clusters | grep -qx "$cluster"; then
  kind delete cluster --name "$cluster"
else
  echo "OK: cluster $cluster does not exist"
fi
