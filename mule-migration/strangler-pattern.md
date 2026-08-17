# Strangler routing pattern

Introduce the target gateway on the existing consumer contract; route to Mule first; deploy target backend; validate safe shadow/contract traffic; shift a small cohort or weight; monitor objective signals; increase; keep a bounded rollback; then remove the legacy route and dependencies.

Never mirror non-idempotent writes without isolated targets and reconciliation approved by the business owner.
