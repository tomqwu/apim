# MuleSoft capability decomposition

| Current Mule responsibility | Preferred destination | Migration evidence |
|---|---|---|
| API routing/facade | Kong route/service plus stable hostname | Contract and parity tests |
| Authentication enforcement | Gateway with enterprise IdP/PKI | Negative and token-claim tests |
| Rate/usage controls | Gateway; shared store if globally consistent | Limit, failure-mode, latency tests |
| Simple transport/header mapping | Gateway when bounded | Configuration review |
| DataWeave or complex mapping | AKS integration service/function | Golden input/output corpus |
| Orchestration/business process | Domain/integration service or workflow engine | State, retry, compensation tests |
| Queue/event integration | Approved messaging/event platform | Delivery and replay tests |
| Batch/scheduler | Managed job/workflow capability | Schedule, restart, audit tests |
| SFTP/MFT | Approved managed file-transfer/integration service | Encryption and reconciliation tests |
| SaaS/database connector | Approved adapter/service | Vendor, pooling, security tests |
| API catalog/portal | Selected API management platform/catalog | Discovery and onboarding test |
| Analytics/audit | Gateway telemetry plus enterprise platforms | Completeness and retention test |

No migration wave is approved until every current responsibility has a named destination, owner, operational runbook, and rollback path.
