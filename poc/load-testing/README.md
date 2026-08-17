# Load testing

Install k6 and start the PoC, then run:

```bash
k6 run -e BASE_URL=http://localhost:8000 -e API_KEY=api-platform-poc-key poc/load-testing/k6/smoke.js
```

The starter threshold is a harness check, not a production performance target. Put sanitized results in `results/` and record the full environment/configuration.
