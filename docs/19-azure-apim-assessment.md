# Azure API Management assessment

## Confirmed strengths

APIM provides managed and self-hosted gateways, API keys and certificate/JWT checks, quotas/rate limits, transformations, caching, telemetry, a developer portal, Azure RBAC integration, and Azure-native networking/monitoring choices. Managed gateways reduce runtime operations; the self-hosted Linux container can run on Kubernetes near on-premises or cross-cloud APIs.

## Variant-specific cautions

- Feature parity varies across classic, v2, consumption, workspace, and self-hosted gateways; score exact variants.
- Self-hosted gateway hosting, scaling, uptime, Kubernetes integration, and complex network troubleshooting remain customer responsibilities.
- The self-hosted gateway depends on its Azure configuration endpoint for updates/telemetry. With local backup, stopped instances can start using the last backup while disconnected; without it, stopped instances cannot.
- Current APIM workspaces cannot associate with self-hosted gateways, which may conflict with a federated hybrid runtime model.
- Some newer v2-tier capabilities and migration paths have limitations that require current validation.

APIM is not dismissed as "not hybrid". The assessment question is whether its exact hybrid/federation boundaries meet the target model better than Kong.
