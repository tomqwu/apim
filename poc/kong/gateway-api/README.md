# Gateway API

The executable GatewayClass, Gateway, and HTTPRoute are in `../../kubernetes/networking/gateway.yaml`. The class is explicitly unmanaged because the pinned KIC/ingress chart creates the gateway Deployment and Service; KIC reconciles route intent into that gateway.
