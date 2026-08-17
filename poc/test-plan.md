# PoC test plan

| ID | Test | Baseline status | Exit evidence |
|---|---|---|---|
| POC-001 | OpenAPI and YAML static validation | Automated | CI log |
| POC-002 | Six routes return contract-shaped synthetic responses | Automated | Smoke log |
| POC-003 | Missing API key denied; fixture key accepted | Automated | 401/2xx assertions |
| POC-004 | Correlation and transformed headers present | Automated | Header/body assertions |
| POC-005 | Local fixed-window limit returns 429 | Automated | Rate test log |
| POC-006 | Gateway API route accepted/programmed | Not run | Live-cluster Accepted/Programmed conditions |
| POC-101 | Entra OIDC client credentials and negative claims | Not run | Token matrix |
| POC-102 | Client/upstream/CP-DP mTLS rotation and revocation | Not run | PKI exercise |
| POC-103 | Distributed limit consistency and Redis failure | Not run | Load/failure data |
| POC-104 | Konnect/self-managed control-plane isolation | Not run | Disconnection matrix |
| POC-105 | Config promotion diff rollback and drift | Not run | Pipeline/audit artifacts |
| POC-106 | Representative performance and soak | Not run | Reproducible result set |
| POC-107 | Pod/node/zone/region and dependency failures | Not run | RTO/SLO evidence |
| POC-108 | Mule facade and PCF-to-AKS cutover | Not run | Golden/canary/reconciliation evidence |
