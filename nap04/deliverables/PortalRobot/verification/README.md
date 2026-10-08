# Offline portal batch verification

These tools read saved evidence only; they never control a browser or execute UiPath. Nine isolated synthetic tests passed. They are not actual batch execution evidence.

After fresh baseline reconciliation, guard enablement and the user's one-time Debug File run, preserve the post-run CSV and user-reported total. From this directory run:

```text
python verify_portal_batch.py ABS_RUN_FOLDER ABS_BASELINE_CSV ABS_POST_CSV ABS_SOURCE_XLSX --before-total ACTUAL_BEFORE --after-total ACTUAL_AFTER
```

Use the original `readiness_2026-10-06/karbejelentesek_input.xlsx` and exact saved batch folder. Requires Python with openpyxl, already available in the workspace.

The verifier requires nine complete per-policy evidence directories, exact input snapshots, ordered events, five fields, one submission/confirmation/case-ID chain per row, three PNG evidence files per row, all ten unique saved policies, nine new case IDs, unchanged earlier records and the count increase. The preserved first case must remain TR-402318/K-GY-4147.

Success means **automated checks passed, visual review pending**. Review all per-row screenshots and actual execution observations separately before marking D4-13 complete. It checks PNG signature/size, not screenshot semantic content. Page totals come from the user's observations; the CSV does not independently establish the20seed records.

Any error requires reconciliation of saved records before a retry. No output of this tool enables the batch or removes reservations. Cumulative completion preserves existing practice fixtures and is not a clean20+10=30 demonstration.
