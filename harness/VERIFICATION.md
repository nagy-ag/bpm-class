# Verification and reproducibility

Run from the repository root with the setup environment:

```powershell
python harness/verify.py
python harness/audit_share.py --staged
```

The offline suite covers source hash preservation, ordered progress transitions/ownership, idempotent setup, relocation to a path containing spaces, fresh project inputs/guards, API failure/no-write paths and portal CSV/log verification. It performs no live API or UI actions. Publication report: `harness/reports/portable_verification.json`; private subsequent reports belong in `.bpa/verification`.

Reference verification remains with each day's actual outputs. Historical author-only archive checks describe original local snapshots; aggregate ZIPs/caches are not published. Do not run historical packaging/reconciliation scripts to initialize another laptop. Use harness entrypoints and the current source manifest.

Actual new-laptop acceptance is in SETUP.md. Offline success does not verify activation, entitlement, browser access, cloud execution, live refresh or robot execution. Record these separately with observed results in local progress. Keep negative/no-write branches and CSV/screenshot comparisons; do not label mocks as platform checks.

CI runs the same offline suite and source check in a clean checkout. Live tests require each user's own private accounts and remain outside CI.
