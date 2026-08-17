# Workload classification

| Class | Signal | Default destination |
|---|---|---|
| G | Routing/security/traffic policy | Gateway |
| F | Facade plus small deterministic compatibility mapping | Gateway plus thin service if required |
| T | Complex reusable transformation/DataWeave | AKS integration service/function |
| O | Multi-step stateful process/compensation | Domain or workflow runtime |
| M | Queue/event/replay/order | Messaging/event platform and consumer |
| B | Schedule/batch/file/SFTP | Job or managed transfer capability |
| C | SaaS/database/protocol connector | Approved adapter or native connector |
| R | No valid consumers/business need | Controlled retirement |
