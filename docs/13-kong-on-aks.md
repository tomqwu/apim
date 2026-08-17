# Kong on AKS

## Production design checklist

- Dedicated namespace, workload identity where supported, restricted service account, Pod Security admission, read-only root filesystem where compatible, and approved image registry/signing.
- Three or more replicas for critical failure domains, topology spread across zones/nodes, resource requests/limits, HPA from measured signals, and a disruption budget.
- Internal or external load balancer chosen per trust zone; private DNS and WAF/edge placement explicit.
- NetworkPolicy default deny with only DNS, backends, control plane, telemetry, and required identity/secret endpoints allowed.
- TLS secrets sourced from approved PKI/secret delivery; rotation and revocation tested.
- Admin/status endpoints private; Prometheus scrape restricted.
- Surge upgrade, rollback, node drain, zone loss, and cluster upgrade exercised under load.

The checked-in Kubernetes baseline demonstrates structure, not a complete AKS landing-zone implementation.
