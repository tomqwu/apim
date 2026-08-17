#!/bin/sh
set -eu

cluster=api-platform-poc
gateway_api_version=v1.5.1
chart_version=0.24.0

for command in docker kind kubectl helm; do
  command -v "$command" >/dev/null 2>&1 || { echo "ERROR: $command is required" >&2; exit 1; }
done

docker info >/dev/null 2>&1 || { echo "ERROR: Docker daemon is not running" >&2; exit 1; }
if ! kind get clusters | grep -qx "$cluster"; then
  kind create cluster --name "$cluster" --wait 120s
fi
kubectl config use-context "kind-$cluster" >/dev/null

kubectl apply --server-side -f "https://github.com/kubernetes-sigs/gateway-api/releases/download/${gateway_api_version}/standard-install.yaml"
docker build -t api-platform/mock-bank:local poc/services/mock-bank
kind load docker-image --name "$cluster" api-platform/mock-bank:local

helm repo add kong https://charts.konghq.com >/dev/null 2>&1 || true
helm repo update kong >/dev/null
helm upgrade --install kong kong/ingress --version "$chart_version" --namespace kong --create-namespace --values poc/kong/helm/values-kind.yaml --wait --timeout 5m

kubectl apply -f poc/kubernetes/namespaces/api-platform-poc.yaml
kubectl apply -f poc/kubernetes/networking/plugins.yaml
kubectl apply -f poc/kubernetes/secrets/poc-consumer.yaml
kubectl apply -f poc/kubernetes/workloads/mock-bank.yaml
kubectl apply -f poc/kubernetes/networking/network-policy.yaml
kubectl apply -f poc/kubernetes/networking/gateway.yaml

kubectl -n api-platform-poc rollout status deployment/mock-bank --timeout=120s
kubectl -n api-platform-poc wait --for=condition=Accepted httproute/synthetic-bank --timeout=120s
kubectl -n api-platform-poc get httproute synthetic-bank -o wide
echo "OK: kind PoC is ready; run make k8s-smoke"
