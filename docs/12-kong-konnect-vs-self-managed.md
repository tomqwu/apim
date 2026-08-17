# Kong Konnect hybrid versus self-managed

| Dimension | Konnect hybrid | Self-managed hybrid | Evidence needed |
|---|---|---|---|
| Control plane | Kong-operated SaaS | Enterprise-operated service/database | Responsibility matrix and SLA |
| Data plane | Enterprise-hosted or managed option | Enterprise-hosted | Placement and image controls |
| Request path | Enterprise data plane | Enterprise data plane | Packet/telemetry validation |
| Configuration/metadata residency | Vendor regions/terms apply | Organization-specific design applies | Data map and contract |
| Upgrades | Shared compatibility contract | Full organizational planning | N/N-1 and rollback test |
| Availability burden | Lower CP operations; connectivity dependency | CP, DB, backup, and DR owned by the organization | Staffing and runbook exercise |
| Exit/portability | Export and entitlement constraints to test | Higher direct control | Restore/export test |

No preference is final until privacy, residency, support, commercial, and disaster-recovery evidence is available.
