# Success criteria

The baseline passes when static checks pass; six operations return 2xx with the fixture key; missing key returns 401; correlation/transform headers are observed; rate limiting returns 429; and the Kubernetes route reaches Accepted/Programmed where the Kubernetes path is run.

The product PoC passes only when all mapped mandatory matrix gates are pass with required evidence, no unmitigated critical finding exists, representative load/failure targets are met, operator runbooks work, and unknown coverage is below the approved threshold.
