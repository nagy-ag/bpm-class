# Portal batch — run only after the remaining work is finished

**Completed and verified2026-10-07. Do not run again.** CSV(4):9new cases, all10lesson policies once,13own/33total. Logs and27screenshots reviewed. The instructions below are retained as the completed run procedure.

If you added/deleted claims since CSV(3), export a fresh CSV first and wait for review.

1. **Brave:** open the empty **Új kárbejelentés** form.
2. **Studio → BPA_Setup_Smoke:** open **Portal_Batch_Resume.xaml**. Choose **Reload** if asked.
3. Click **Debug File once**. Wait until Studio stops. It skips the completed first row and submits the remaining nine.
4. **Kárügyek listája → Saját rögzítések exportálása CSV-be**. Reply **done**, the CSV suffix and the displayed total. Expected: **33 total**.

If an error appears, stop and report it. Do not retry or delete locks. I will review the logs, screenshots and CSV.

[Detailed evidence and prerequisites](PORTAL_BATCH_DETAILS.md). [Actual verification](actual_batch_20261007/batch_verification.json).
