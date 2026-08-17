# Kong configuration

- `deck/kong.yaml` is a native Kong declarative configuration loaded directly by the Docker DB-less gateway. Despite the folder name, decK does not sync it to DB-less mode.
- `helm/values-kind.yaml` pins the verified local chart/image settings.
- `gateway-api/` points to portable Kubernetes routing resources.
- `plugins/` and `policies/` document the tested OSS and untested enterprise boundary.
