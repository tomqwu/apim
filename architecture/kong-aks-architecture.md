# Kong on AKS reference

Use separate namespaces/service accounts, restricted security contexts, signed images, resource guarantees, topology spread, HPA, PDB, graceful termination, default-deny networking, private management/status endpoints, approved secret/PKI delivery, and edge/internal load balancers by zone.

The platform team owns GatewayClass and shared gateway infrastructure. Domain teams own permitted HTTPRoutes and API contracts. Policy attachment is constrained by admission controls and reviewed templates.
