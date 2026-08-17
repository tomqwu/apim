# Risk register

| ID | Risk | Early indicator | Mitigation | Owner |
|---|---|---|---|---|
| R-01 | Gateway becomes a new integration monolith | Policies contain domain branches/scripts | Enforce capability boundary and review | Architecture |
| R-02 | Kong-first bias distorts evidence | Requirements/weights change after demos | Freeze criteria before scoring | Assessment lead |
| R-03 | Hybrid management/residency fails controls | Unclear metadata/telemetry flows | Data-flow review and contract evidence | Security/privacy |
| R-04 | Required plugin is licensed/topology-incompatible | PoC uses substitutes | Feature/topology/license bill of materials | Platform |
| R-05 | Distributed rate limit creates new shared failure | Redis latency/errors affect traffic | Failure-mode design and load test | SRE |
| R-06 | Mule inventory misses embedded logic | Post-cutover behavior divergence | Static analysis plus owner walkthrough/golden tests | Integration |
| R-07 | PCF and Mule coexistence persists indefinitely | No exit dates or dependency burn-down | Wave benefits and retirement gates | Program |
| R-08 | Portal/governance work is underestimated | Manual onboarding backlog | Journey PoC and operating-cost model | Product owner |
| R-09 | Vendor support stops at platform boundary | CNI/firewall issue bounces between teams | RACI, joint support exercise, contract terms | Vendor mgmt |
| R-10 | Observability leaks sensitive data | Payload/token found in logs | Default redaction and automated tests | Security |
| R-11 | Multi-region design doubles cost without tested value | Idle capacity/no exercises | SLO-derived topology and annual game day | Resilience |
| R-12 | Exit path is untested | Proprietary policy/catalog lock-in | Export/restore and portability tests | Architecture |
