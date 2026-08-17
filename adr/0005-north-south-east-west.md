# ADR-0005: Keep API and service-networking boundaries explicit

- Status: proposed
- Date: 2026-08-17

Use the enterprise API gateway for intentional north-south and enterprise API boundaries. Do not route every AKS east-west call through it by default; use direct service networking or a service mesh according to workload requirements.
