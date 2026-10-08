# Portal batch — ready for user-operated run, not executed

Portal_Batch_Resume.xaml reads all10supplied input rows. It skips only TR-402318, already verified as K-GY-4147, and processes the other9inside the same attached browser. All captured target descriptors are unchanged. File validation and clean whole-project build passed. No portal activity was executed by the agent.

Each pending row has its own run directory, input snapshot, five field checkpoints, one submission, confirmation check, actual case-ID file and screenshots. Atomic per-policy reservations are created before any submission; uncertain outcomes stop the run. The first reservation is retained. No automatic submission retries.

CSV(3) is preserved and reconciled in portal_baselines/pre_batch_export3_20261007/baseline_review.json: four own records unchanged, first input exact once, other9absent, only the original reservation. User-reported total24 implies20seed records. Only batchBaselineReviewed changed from False to True; captured targets and original trial are unchanged. Fresh file validation has no diagnostics; whole-project compilation succeeded with analyzer warnings. See portal_batch_ready.json and ../portal_batch_ready_validate.json, ../portal_batch_ready_build.json. This is preparation, not execution.

1. In the original Brave portal, return to the empty Új kárbejelentés form. If the saved-record state changed since CSV(3), stop and export again.
2. In Studio's BPA_Setup_Smoke project, open Portal_Batch_Resume.xaml. If Studio offers to reload externally changed contents, choose Reload. Confirm Variables shows batchBaselineReviewed=True; never change targets or delete reservations.
3. Choose Debug File from the ribbon once, for this open XAML, rather than running Main. Wait until Studio stops running. It should skip TR-402318 and process9pending records.
4. Reply done, or give the error without Retry/rerun. On the portal, Kárügyek listája → Saját rögzítések exportálása CSV-be; report its total and the new CSV suffix. Expected33total/13own, not30.

Agent must review the actual logs, nine case IDs, all saved fields,27screenshots and new CSV before marking the batch complete. The exact clean manual-first-policy/reset variant of D4-11 remains unexecuted; the cumulative route preserves earlier fixtures and actual first-row evidence.

Expected count uses the fresh baseline: if it is24cases with4own, the remaining9yield33cases/13own, ten of them matching supplied inputs. This is cumulative completion with preserved fixtures; it is not a fresh20+10=30run. A cleanup/reset requires separate reconciliation and user action.

Original project: nap04/working/setup_2026-10-06/BPA_Setup_Smoke/project.json. Stable portal: nap04/working/readiness_2026-10-06/gyakorlo_karportal.html. Neither page nor reservation should be moved/deleted.
