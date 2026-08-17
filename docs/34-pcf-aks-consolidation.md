# PCF-to-AKS consolidation

Use stable API hostnames at the gateway while backends move behind them:

1. Baseline the existing PCF route and contract.
2. Introduce the gateway facade without changing behavior.
3. Deploy the AKS replacement and run shadow or contract tests where safe.
4. Shift weighted traffic with explicit success/abort signals.
5. Retain a time-bounded rollback route.
6. Remove PCF dependencies only after consumers, DNS, certificates, monitoring, and support ownership are reconciled.

Do not force internal service-to-service traffic through the enterprise gateway solely because the backend moved to AKS. Keep the API boundary intentional.
