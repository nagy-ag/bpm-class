# One-row portal trial — passed

Verified 2026-10-07. The user started `Portal_Logged_Trial.xaml` with Studio Run File. The agent reviewed saved evidence offline; no agent control of the restricted local browser page occurred.

Case **K-GY-4147**, policy **TR-402318**. All five saved values match the input snapshot: vízkár, 2025-11-03, 1850 lei, and the original Hungarian description, together with the policy number.

- [Automated verification](portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202/verification.json): all 19 checks passed, including ordered checkpoints, five field activities, actual case-ID readback, screenshots, exported values and unique policy/case.
- [Visual execution review](portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202/execution_evidence_review.json): saved before/fill/confirmation screenshots reviewed; filled values and success confirmation agree with logs and snapshot.
- [Export reconciliation](portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202/post_export_reconciliation.json): post-run own-record count is four; all three prior records are unchanged and exactly one new record was added. Original downloaded CSV bytes are preserved beside these reports.

The reservation `portal_runs/reservations/TR-402318.lock` is retained. Do not rerun this first row or delete its lock; future batch work must reconcile this already-created case and process only unfinished records.

This completes the one-row readiness test for setup items 1–3 together with the previously verified Office and Studio checks. It does not complete the ten-row assignment or establish unattended website login. No further user action is needed for this test. Resume coursework in course order using its detailed task trackers; preserve this setup evidence when reusing the workflow.
