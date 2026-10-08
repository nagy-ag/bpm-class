# Logged portal workflow: user handoff

Updated 2026-10-07. The user-started one-row trial passed saved-record verification for K-GY-4147 / TR-402318. [Final result](PORTAL_TRIAL_RESULT.md). No agent portal action or submission occurred.

## Completed test

No further user action is needed for this test. The user's (2) export is preserved beside the run evidence. [Verification](portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202/verification.json) passed all 19 checks; all five saved values agree, the case/policy occurs once, and the three pre-existing records remain unchanged. [Visual execution review](portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202/execution_evidence_review.json) also passed. Preserve reservation TR-402318.lock and do not rerun this first input row.

Everything below records historical preparation and the completed run handoff. Earlier pending instructions are superseded by the final result above.

Target1 is saved: offline inspection found an InputBox target for the kotvenyszam INPUT, its label anchor and screenshot reference. This confirms saved configuration, not an executed robot.

Target2 is saved: offline inspection found a DropDown target for the kartipus SELECT, label anchor and screenshot reference. Capture replaced Item with the placeholder; restored through Studio to `CurrentRow("kartipus").ToString()` and independently checked the saved expression/target. No live validation or run occurred.

Target3 is saved: offline inspection found an InputBox target for karesemeny-datum INPUT, label anchor and screenshot reference. Its spreadsheet expression remains `CurrentRow("karesemeny_datum").ToString()`. Targets1–2 and their expressions are preserved. No live validation or run occurred.

Target4 is saved: offline inspection found an InputBox target for becsult-osszeg INPUT, label anchor and screenshot reference. Its spreadsheet expression remains `CurrentRow("becsult_osszeg").ToString()`. Targets1–3 and their expressions are preserved. No live validation or run occurred.

Target5 is saved: offline inspection found a karleiras TEXTAREA descriptor, label anchor and screenshot reference. Its spreadsheet expression remains `CurrentRow("karleiras").ToString()` and clearing remains MultiLine. Targets1–4 and their expressions are preserved. No live validation or run occurred.

Target6 is saved: offline inspection found the bejelentes-rogzites BUTTON descriptor and screenshot reference. All five spreadsheet expressions and description MultiLine clearing remain correct. No live validation or run occurred.

Baseline is now preserved in [portal_baselines/20261007_083051/](portal_baselines/20261007_083051/baseline_review.json), including the original exported bytes, SHA256 and review. It contains two own records (K-GY-9610/TR-123456 and K-GY-1660/TR-654321). Robot input policy TR-402318 is absent. The separate manual capture policy TR-900007 is absent from both the baseline and all ten input rows. This is baseline reconciliation, not robot execution.

Offline inspection also found target7 incorrectly captured as tab-lista BUTTON (Kárügyek listája). It must be re-indicated as the actual confirmation heading before any run. Targets8–9 remain unconfigured. Studio is open at target7; leave it until the user has produced the confirmation screen.

User completed the separate manual setup fixture. The supplied screenshot visibly confirms success and **K-GY-5405**, policy TR-900007, vízkár, 2025-11-03 and1850lei. [Preserved screenshot/review](portal_baselines/20261007_083051/manual_capture_K-GY-5405/manual_confirmation_review.json). Description is not visible and post-submit CSV has not yet been reviewed. This is a user-performed manual confirmation, not robot evidence.

Target7 is now corrected and saved: offline XAML has a Text/H2 target, and Studio's saved thumbnail highlights the confirmation heading. Earlier incorrect button captures are superseded. No live agent validation or robot execution occurred.

Target8 is now captured and saved: Text/DIV id ugyszam-ertek, with output caseId preserved. This is offline configuration review, not live execution.

Target9 is now captured and saved as BUTTON id uj-bejelentes. All nine direct descriptors, five input bindings, caseId output, one-row range and False guard passed [offline review](portal_targets_configured_review.json). [Fresh file validation](portal_targets_configured_validation.txt) reports no diagnostics. [Project compilation](portal_targets_configured_build.txt) succeeds with analyzer warnings; built-in verification is disabled on several actions, and actual user-run/readback testing remains required.

Fresh `sajat_karbejelentesek (1).csv` is preserved in [pre_robot_20261007_085655](portal_baselines/pre_robot_20261007_085655/pre_robot_review.json). It contains three own records; both earlier records are unchanged, manual TR-900007 / K-GY-5405 matches all five expected values, and robot policy TR-402318 is absent. No reservation locks exist. The run guard is now True; semantic comparison confirms no other workflow changes. [Preparation evidence](portal_user_run_prepared.json), [validation](portal_user_run_validation.txt), [compilation](portal_user_run_build.txt).

Current user action: start the one-row trial once, then wait.

1. In Brave, normally click the top **Új kárbejelentés** tab. Leave the empty form open in the same logged-in portal tab; do not fill or submit it manually.
2. Switch to Studio. **Portal_Logged_Trial.xaml** is already the selected tab.
3. Open the dropdown beside the top-left Run triangle and choose **Run File**. Do not choose Run Project, which runs the original Main workflow.
4. Leave the mouse and keyboard alone while the robot runs. Expected sequence: fill five values for TR-402318, submit once, capture confirmation/case number, return to a blank form.
5. Wait until Studio Output shows **BPA_Setup_Smoke execution ended** and, on success, **run_finished_pending_readback**. Reply **done**. If an error appears, report the error and do not run again.

The agent waits for this reply before reviewing generated logs, case ID, input snapshot and screenshots offline, then requesting a fresh own-record export to verify saved values. A stopped or uncertain run must be reconciled against exported records before any retry; do not delete reservations or reset portal records. Preserve all targets, input, baselines and confirmation evidence. Do not regenerate the workflow or access the blocked page through another tool.

Historical export checkpoint below predates the preserved baseline and manual fixture; it is superseded by their evidence above.

User requested a check of the export sequence: saved target6 still points to bejelentes-rogzites BUTTON, so that target was not replaced with the list/export button. No matching karbejelentesek CSV or partial CSV download was found in the normal `C:/Users/nagya/Downloads` folder at this check. The export remains pending; a custom save location is possible. Wait for a fresh export or its actual path before baseline review.

## What is prepared

`Portal_Log.xaml` writes timestamped, correctly quoted UTF-8 CSV events plus a last-event checkpoint, and echoes events in Studio Output. Its file-only `Portal_Log_Smoke.xaml` actually executed successfully in seven seconds. Hungarian text and quote roundtrips passed; evidence is in `portal_logging_preparation_verified.json` and `portal_runs/logger_smoke_36c093251d9c4f1e8605abe93077bd32/`.

`Portal_Logged_Trial.xaml` contains real UI Automation activities, one-row input validation, an input snapshot, field checkpoints, application screenshots, submission/confirmation checkpoints and actual case-ID readback. It reserves each policy in a durable lock before submission and stops on uncertainty without retrying the submit action. The final event is deliberately `run_finished_pending_readback`; a completed activity sequence alone does not prove the saved record is correct.

The workflow retains the historical **TODO Indicate** display names, but all nine descriptors have now been supplied by user capture. `targetsConfigured=True` is saved after fresh record reconciliation; the earlier False-guard configuration review is historical. Offline validation and compilation pass. Original Main.xaml, Workbook_Roundtrip.xaml and input bytes are preserved. Compilation does not prove live targeting or saved-record correctness.

The official [UiPath authoring skill](https://raw.githubusercontent.com/UiPath/skills/main/skills/uipath-rpa/SKILL.md) and its [Placeholder-Selector Stub Pattern](https://raw.githubusercontent.com/UiPath/skills/main/skills/uipath-rpa/references/uia-starter-guide.md) require a "TODO Indicate" marker when live capture is unavailable. The browser tool's file-URL restriction also prohibits indirect access. The user performs target capture and the eventual portal run; the agent can review saved artifacts offline.

## Remaining targets, in workflow order

| Marker | User-selected control |
| --- | --- |
| 1 | Kötvényszám textbox — user captured/saved; offline descriptor inspected |
| 2 | Kár típusa dropdown — user captured/saved; descriptor and restored spreadsheet expression inspected |
| 3 | Káresemény dátuma textbox — user captured/saved; descriptor and spreadsheet expression inspected |
| 4 | Becsült összeg textbox — user captured/saved; descriptor and spreadsheet expression inspected |
| 5 | A kár rövid leírása textarea — user captured/saved; descriptor/expression/MultiLine clearing inspected |
| 6 | Bejelentés rögzítése button — user captured/saved; BUTTON descriptor inspected |
| 7 | A bejelentést rögzítettük confirmation heading — corrected/saved Text-H2 descriptor; thumbnail matches heading |
| 8 | Generated K-GY-… case-number text — user captured/saved; Text-DIV descriptor and caseId output inspected |
| 9 | Új bejelentés rögzítése button — user captured/saved; BUTTON descriptor inspected |

Targets 7–9 require a confirmation screen and a reconciled manual trial; do not submit a claim solely to capture these without preserving its case ID and checking existing records. Future targeting is handled step by step after the current reply.

## Eventual user-run acceptance (not the current action)

Before any run: all targets must be captured and checked by the user, validation must pass, and `targetsConfigured` may only become True after that review. Inspect the current own-record list for the input policy and reconcile any earlier manual/uncertain submission. Do not delete reservation locks or resubmit to clear an error. Keep the range at `bejelentesek!A1:F2`; this is a one-row setup trial, not the ten-row assignment.

When explicitly handed off for execution, select this workflow and use Studio's Run dropdown → **Run File**. Wait for execution to end and for `run_finished_pending_readback` in Output. Successful evidence should include `events.csv`, `last_event.txt`, `input_snapshot.xlsx`, `case_id.txt`, and `01_before.png`, `02_filled.png`, `03_confirmation.png` inside a unique `portal_runs/` folder. A `stopped_requires_review` event or exception requires inspecting saved records before retrying.

The user then exports their own practice records from the portal and supplies that CSV path. The offline reviewer `verify_portal_run.py` compares the actual case ID and all five saved values with the snapshot, checks ordered events and evidence files, and writes `verification.json` only if checks pass. Screenshots still need visual review. No actual portal evidence has been supplied yet; this checker is prepared and syntax-checked, not a verified portal result.

Delimiter correction: the static portal exporter writes semicolon-separated CSV with a UTF-8 BOM; the logger writes comma-separated CSV. The reviewer now parses these separately. Focused parser checks passed for BOM/semicolons/quoted text and logger commas; these parser fixtures are not portal-run evidence.

The agent must not run this workflow, capture/validate its portal targets, serve the portal via localhost, or change its URL/browser to work around the existing restriction.
