# Verified nap04 handoff

Five Windows / Visual Basic projects and their actual execution evidence are preserved. Final review reuses those actual runs; it does not rerun completed robots.

| Project | Open in Studio | Verified behavior |
| --- | --- | --- |
| First robot | Nap04_gyakorlas/project.json | Main; Greeting_Initial (intentional invalid-input failure); Greeting_Repaired; eight-case Validation_Regression |
| Excel classification | ExcelRobot/project.json | Main: 100000 threshold; Classify_150000: separate 150000 output |
| Office reports | RiportRobot/project.json | Main: 12 records; Report_6: six records, native Excel and slide9 charts |
| File sorter | Fajlrendezo/project.json | Main: documents; Sort_With_Images: PNGs and zero-move second run |
| Portal | PortalRobot/setup_2026-10-06/BPA_Setup_Smoke/project.json | User-started first-row trial and remaining-nine batch; all ten policies exact |

Read each project's README before selecting a workflow. Completed output/report guards and portal reservations must remain intact. For a new non-portal exercise, use fresh working copies and destinations. The portal batch is already complete: **do not rerun it**.

The portal uses Brave with the user's extension/file permissions and captured targets. It retains the original readiness portal and absolute log/reservation paths. The standalone package is for this workspace; copying it to another machine requires a new path/permission/target review. Agent access to the local portal remains restricted; the user starts portal runs.

The original portal result is **13 own / 33 total**, including four preserved earlier records and nine new batch cases. This is the recorded cumulative adaptation, not a clean 30-case run. The exact manual first-row / reset exercise separately passed in the isolated **MANUAL RESET TEST** copy, ending with 20 samples, zero own cases and an empty form. Its screenshots/CSV/reviews are under PortalRobot/manual_reset_20261007/.

Dependencies: System 26.8.2; Excel 3.6.1 where used; Presentations 2.6.1 for reports; UIAutomation 26.10.5 for portal. Local Studio/Excel/PowerPoint prerequisites have actual setup and lesson execution evidence. Studio restores the declared packages when opening a clean project.

The clean archive excludes build caches, Python caches and temporary Office lock files; target resources and completed-run markers are retained. Original folders are preserved. No credentials, new account permissions, scheduled local job or graded submission are included.

Evidence: final_audit/handoff_verification.json inside the archive; standalone audit under ../working/final_audit_20261007/; actual project outputs and native screenshots in each project directory. Older preparation reports remain historical, including pre-run guards/build hashes. Current delivered portal batch XAML was reconciled to the actual Studio working serialization; the earlier delivery is preserved in the audit work area.
