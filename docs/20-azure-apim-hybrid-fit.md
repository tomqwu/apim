# Azure APIM hybrid fit

## PoC scenarios

1. Deploy self-hosted gateway to AKS with private access to the Azure configuration endpoint.
2. Enable local configuration backup, interrupt Azure connectivity, restart a pod, and test clean scale-out.
3. Compare policy behavior and feature coverage with the managed gateway.
4. Test Entra workload identity rather than rotating 30-day access tokens.
5. Map workspace federation requirements to the documented prohibition on self-hosted association.
6. Capture customer/Microsoft support boundaries for CNI, NetworkPolicy, firewall, mesh, telemetry, availability, and capacity.

## Falsification question

Can APIM produce a coherent centrally governed, domain-delegated API program with workload-local gateways across the required locations without unsupported combinations or excessive service-instance sprawl?
