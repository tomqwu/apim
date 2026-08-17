# Kubernetes baseline

The manifests use a restricted synthetic workload, two replicas, PDB, default-deny NetworkPolicy, Kong plugins/consumer fixture, and Gateway API routing. The pinned `kong/ingress` Helm chart renders separate controller and two-replica DB-less gateway Deployments.

This is a kind baseline. AKS production requires landing-zone network, workload identity, registry/signing, secret/PKI, Azure load balancer/private DNS, observability, policy, multi-zone, upgrade, and support integration.
