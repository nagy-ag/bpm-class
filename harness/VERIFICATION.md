# Verification and reproducibility

Run from the repository root with the setup environment:

```powershell
python harness/verify.py
python harness/verify_maintenance_export.py
python harness/audit_share.py --staged
```

The offline suite covers source hash preservation, ordered progress transitions/ownership, idempotent setup, relocation to a path containing spaces, fresh project inputs/guards, API failure/no-write paths and portal CSV/log verification. It performs no live API or UI actions. Publication report: `harness/reports/portable_verification.json`; private subsequent reports belong in `.bpa/verification`.

Lesson-maintenance regression tests additionally cover staged extraction before installation, path/link/collision/expansion rejection, stale-source refusal, rollback after a failed catalog write, exact backups, unchanged credentials/completed work, new days, explicit revision starts and preserved revision history. Injection fixtures cover raw hidden/comment instructions, entity decoding, notebook cells, ZIP-first extraction, credential exclusions/redaction and honest unsupported-format coverage. Both new skills' explicit-only metadata is checked. These are isolated synthetic fixtures, not an audit or import of current real lesson sources.

`verify_maintenance_export.py` exports Git's staged index into a temporary path with spaces, initializes fresh local state and runs the offline suite. It then tests the actual stage/audit/apply/status/start-revision/step CLI sequence against a synthetic nap05 ZIP and verifies the imported provenance. It preserves your checkout and credentials, writes its report under `.bpa/verification`, and cleans up only its own temporary checkout. Stage intended changes before running it. CI runs it too; tests/helpers remain versioned, while their private runtime outputs remain ignored.

Reference verification remains with each day's actual outputs. Historical author-only archive checks describe original local snapshots; aggregate ZIPs/caches are not published. Do not run historical packaging/reconciliation scripts to initialize another laptop. Use harness entrypoints and the current source manifest.

Actual new-laptop acceptance is in SETUP.md. Offline success does not verify activation, entitlement, browser access, cloud execution, live refresh or robot execution. Record these separately with observed results in local progress. Keep negative/no-write branches and CSV/screenshot comparisons; do not label mocks as platform checks.

CI runs the same offline suite and source check in a clean checkout. Live tests require each user's own private accounts and remain outside CI.
