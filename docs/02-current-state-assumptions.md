# Current-state assumptions and required inputs

No row below is an organization-specific fact until confirmed.

| ID | Assumption | Why it matters | Validation owner | Status |
|---|---|---|---|---|
| A-01 | PCF means Pivotal Cloud Foundry. | Defines migration tooling and routing patterns. | Platform architecture | Open |
| A-02 | AKS is the strategic container platform. | Drives gateway placement and operations integration. | Cloud platform | Open |
| A-03 | MuleSoft performs both gateway and integration-runtime duties. | Determines decomposition scope. | Integration team | Open |
| A-04 | Azure is the primary cloud but platform neutrality is valuable. | Changes weight of native integration vs portability. | Enterprise architecture | Open |
| A-05 | Some request paths must stay within approved regional or private network boundaries. | Constrains management/telemetry/data planes. | Security/privacy | Open |
| A-06 | Entra ID is a primary workforce/workload identity provider. | Shapes OAuth/OIDC and workload-identity tests. | IAM | Open |
| A-07 | Central standards and federated domain ownership are desired. | Drives tenancy and delegation design. | API governance | Open |
| A-08 | Mule retirement will be phased, not a big bang. | Requires coexistence and strangler routing. | Program leadership | Open |
| A-09 | Existing PCF routes can be reached privately from gateway data planes. | Affects transition feasibility and latency. | Network | Open |
| A-10 | Production requires at least two failure domains and tested DR. | Sets topology and cost. | Resilience | Open |

## Required discovery inputs

- Mule applications, APIs, connectors, policies, schedules, queues, DataWeave, dependencies, certificates, owners, and support dates.
- API consumers, classifications, peak/average load, payloads, protocols, timeouts, latency budgets, SLOs, RTO/RPO, and seasonality.
- Current WAF, load balancer, DNS, PKI, firewall, private connectivity, egress, proxy, SIEM, APM, secrets, and identity standards.
- PCF foundations/spaces/routes and AKS clusters/regions/network model.
- Data residency, logging retention, privacy, threat-model, audit, and third-party-risk controls.
- Delivery workflow, environment promotion, segregation of duties, emergency change, rollback, and evidence requirements.
- Current and forecast MuleSoft costs plus comparable vendor quotes; never substitute list price for organization-specific TCO.

Use the templates in `templates/` and `mule-migration/inventory-template.csv` to collect these inputs.
