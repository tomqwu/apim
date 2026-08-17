# Migration tests

Place a stable gateway route over a simulated Mule/PCF backend, capture golden behavior, deploy an AKS replacement, test safe reads/shadow where appropriate, shift weighted traffic, enforce abort signals, reconcile outputs/side effects, roll back, and prove legacy dependency removal. Never duplicate live non-idempotent writes casually.
