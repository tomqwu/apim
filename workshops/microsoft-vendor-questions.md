# Microsoft APIM vendor validation questions

1. Propose exact managed, self-hosted, workspace, and service-tier resources for the organization's federated hybrid scenarios.
2. Reconcile the documented inability to associate workspaces with self-hosted gateways with the proposed federation model.
3. Demonstrate self-hosted gateway behavior with local backup during Azure configuration-endpoint loss, pod restart, and clean scale-out.
4. Provide current feature parity across the proposed managed and self-hosted variants.
5. Demonstrate Entra authentication for self-hosted gateway management connectivity without rotating access tokens.
6. Identify all configuration, credential, telemetry, analytics, audit, and support data stored or processed in Azure.
7. Define required public/private DNS, endpoint, proxy, firewall, and egress dependencies.
8. Provide the customer/Microsoft responsibility boundary for AKS, CNI, mesh, firewall, NetworkPolicy, capacity, uptime, and diagnostics.
9. Demonstrate multi-region/failure-domain operation and configuration consistency for the proposed variants.
10. Explain current v2-tier feature gaps and migration implications for any proposed tier.
11. Demonstrate configuration-as-code diff, promotion, drift detection, rollback, and audit without portal drift.
12. Provide policy portability/export and a tested service restore/exit process.
13. Demonstrate developer/product federation for internal and partner journeys.
14. Provide sizing/TCO methodology including gateway units, workspaces, self-hosted instances, nonproduction, and DR.
15. State the conditions under which Microsoft would advise the organization to select Kong or Apigee instead.
