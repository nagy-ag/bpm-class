# nap04 task progress

Follow [the mandatory workflow](../../TASK_PROGRESS.md) before every action. Claim a task, execute its ordered steps, verify each result and update immediately. Source requirements and implementation are in the installed day runbook.

Initialized 2026-10-06. Completed coursework is migrated from existing dated evidence, not rerun. Preserve other agents' claims, blockers and evidence.

| Task | Scope | Status | Next step |
| --- | --- | --- | --- |
| [D4-01 — Studio workspace/first Run](#d4-01) | required | done | None |
| [D4-02 — Greeting/initial calculation](#d4-02) | required | done | None |
| [D4-03 — Input-validation repair](#d4-03) | required | done | None |
| [D4-04 — Excel100000classification](#d4-04) | required | done | None |
| [D4-05 — Excel150000mini-exercise](#d4-05) | required | done | None |
| [D4-06 — Excel/PPT12records](#d4-06) | required | done | None |
| [D4-07 — Six-record report mini-exercise](#d4-07) | required | done | None |
| [D4-08 — PDF/Excel/Word sorter](#d4-08) | required | done | None |
| [D4-09 — PNG sorter and second run](#d4-09) | required | done | None |
| [D4-10 — Portal prerequisites](#d4-10) | required | done | None |
| [D4-11 — Manual practice claim](#d4-11) | required | done | None |
| [D4-12 — One-row form robot](#d4-12) | required | done | None |
| [D4-13 — Ten-row form robot](#d4-13) | required | done | None |
| [D4-14 — Robot/API/human choices](#d4-14) | required | done | None |
| [D4-15 — Day4 runnable handoff](#d4-15) | required | done | None |
| [D4-P01 — Offline batch verification tooling](#d4-p01) | independent preparation | done | None |
| [D4-P02 — Isolated manual/reset practice preparation](#d4-p02) | independent preparation | done | None |

<a id="d4-p02"></a>
## D4-P02 — Isolated manual/reset practice preparation

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: independent offline preparation for blocked D4-11. Existing13own/33total and all reservation locks must remain intact. No browser/UiPath portal actions initiated by the agent.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Copy portal to a separate work area and isolate its persistence key; preserve original bytes and behavior. | done | Copied working portal to manual_reset_20261007/manual_reset_portal.html; only dedicated persistence key/title/badge changed. Source byte hash preserved. Preparation completed; console Unicode rendering failed after evidence write and is corrected without portal execution. |
| 2 | Verify exact allowed differences, seed count and first input row; save preparation evidence. | done | preparation.json verifies restoration of exactly key/title/badge differences recovers original bytes;20sample cases unchanged, first input TR-402318/vizkar/2025-11-03/1850 and supplied Hungarian description read from original workbook. No browser/robot action. |
| 3 | Write short user-only baseline/manual/confirmation/new-form/reset handoff; actual actions remain pending. | done | Short staged HANDOFF.md saved beside isolated copy. User asked only to open copy/log in/check MANUAL RESET TEST badge and20cases; wait before entry/reset. Original33cases and locks preserved; preparation only, D4-11 actual manual/reset remains blocked. |

<a id="d4-01"></a>
## D4-01 — Studio workspace/first Run

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: Shared access-04.

Source: [01_studio_terkep.html](../nap04/pages/01_studio_terkep.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson; verify desktop entitlement and Windows/VB Process. | done | Current lesson reviewed; desktop Studio26.0.203 Community/Pro entitlement and Windows/VB Process verified in setup-01. Canvas/Explorer/Properties/Output observed in prior actual runs. |
| 2 | Create Nap04_gyakorlas and restore packages. | done | Official CLI init created Nap04_gyakorlas Windows/VB with restored System26.8.2; exact Működik workflow validates without diagnostics and build Success=true. |
| 3 | Run Működik! Message Box; observe dialog and successful Output. | done | Actual dialog Működik observed and OK clicked. Desktop result Session ended, errors=[], debugState Completed; execution00:00:39. [Run](../working/nap04_main_run.json) [Dialog](../working/nap04_main_dialog.jpg). |
| 4 | Save runnable project and evidence. | done | [Clean project](../deliverables/Nap04_gyakorlas/README.md) saved with byte-identical executed Main/project files; actual run/dialog evidence linked at step3. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-02"></a>
## D4-02 — Greeting/initial calculation

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-01.

Source: [02_elso_robot.html](../nap04/pages/02_elso_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read dialogs/variable types and scopes. | done | Current02_elso_robot.html read fully. nev/darab String scoped to Main Sequence;250days is fictional lesson assumption; preserve CInt failure before repair. |
| 2 | Build name/count dialogs and initial CInt calculation. | done | Greeting_Initial.xaml has both exact dialogs, String variables and CInt annual calculation. Explicit typed InputDialog output repaired; validate clean, whole build Success=true. Main preserved. |
| 3 | Run20→5000 and demonstrate sok conversion failure. | done | Actual interactive20→5000 dialog saved; run Session ended/errors[]/126seconds. Actual sok run aborted with System.InvalidCastException and exact conversion error after110seconds. Separate run JSONs preserved. |
| 4 | Save actual outcomes and initial workflow evidence. | done | [Initial workflow](../deliverables/Nap04_gyakorlas/Greeting_Initial.xaml) and [two actual outcomes](../deliverables/greeting_initial_evidence.json) saved; expected failure distinguished from passing execution. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-03"></a>
## D4-03 — Input-validation repair

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-02.

Source: [02_elso_robot.html](../nap04/pages/02_elso_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read repair; preserve initial evidence. | done | Current repair requires TryParse with inclusive0..1000000; initial workflow and actual20/sok evidence preserved in deliverables. |
| 2 | Use TryParse and allowed0–1000000range. | done | Exact TryParse/range gate retained; explicit Assign stores validated integer before250-day calculation. Addresses observed5→0 runtime fault. Initial and diagnostic runs preserved. Project validates clean. |
| 3 | Run5→1250; sok/-1/blank→friendly message without exception. | done | Actual repaired interactive5→1250 observed/saved, Session ended/errors[]/122seconds. Actual shared-workflow regression run has8 PASS rows, errors[]:5,sok,-1,blank,0,1000000,1000001,2147483648. Compilation succeeded in actual run. |
| 4 | Save repaired project and observations. | done | [Repaired project](../deliverables/Nap04_gyakorlas/README.md), [actual evidence](../deliverables/greeting_repaired_evidence.json) saved; initial CInt and two failed regression runs retained. Corrected output independently verified. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-04"></a>
## D4-04 — Excel100000classification

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-03.

Source: [03_excel_robot.html](../nap04/pages/03_excel_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read schema and copy source workbook to working area. | done | Current lesson reviewed. input/ugyfelek.xlsx copied byte-identically; Ugyfelek schema Nev/Varos/EvesDij/Minosites,12rows and blank classifications verified; input_manifest.json saved. |
| 2 | Build workbook read/row Assign/write with headers. | done | ExcelRobot Windows/VB restored System26.8.2/Excel3.6.1. Actual Workbook ReadRange/ForEachRow inside-body Assign/WriteRange headers enabled;12-row guard and existing-output refusal; external file boundaries log/rethrow. File validation clean. |
| 3 | Run robot; verify12rows,6kiemelt/6normál and preserved values. | done | Actual desktop run Session ended/errors[]/Completed in34seconds. Independently verified12rows,6kiemelt/6normál, first3columns preserved and source/input hashes equal. [Verification](../working/ExcelRobot/verification_100000.json), [run](../working/excel_100000_run.json). |
| 4 | Save first result/project/run evidence. | done | Saved [clean project/output](../deliverables/ExcelRobot/README.md), actual run/dialog and independent verification; executed XAML/input/output copied unchanged. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-05"></a>
## D4-05 — Excel150000mini-exercise

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-04.

Source: [03_excel_robot.html](../nap04/pages/03_excel_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Preserve first output and choose v2file. | done | First result preserved in working/deliverables; mini_baseline.json records hash. Distinct v2 output does not exist. |
| 2 | Set150000threshold and run actual robot. | done | Official headless validation clean after stalled desktop designer restart. Actual UiPath Windows run completed17seconds; hasErrors=false/errorMessage=null/debugState=null; observed v2 completion dialog. Run compiles internally. |
| 3 | Verify12rows/3kiemelt and specified annual amounts. | done | Actual v2 workbook verified12rows/3kiemelt, amounts152000/187300/231000. First3columns/input unchanged; first output hash equals preserved baseline. [Verification](../working/ExcelRobot/verification_150000.json). |
| 4 | Save second result alongside first with run evidence. | done | Both executed outputs/workflows saved in [clean project](../deliverables/ExcelRobot/README.md), with separate verification and actual run/dialog evidence. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-06"></a>
## D4-06 — Excel/PPT12records

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-05; desktop Excel and PowerPoint.

Source: [04_excel_ppt.html](../nap04/pages/04_excel_ppt.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read template/native route and prepare fresh Office copies. | done | Current04lesson read fully; native route selected. Fresh reports_12 Excel/PPT copies byte-identical and source_manifest hashes saved. Native PowerPoint opened copy; Protected View requires private user Enable Editing before layout preparation. |
| 2 | Build chart/copy/paste for us-500 A1:B13 and slide9content placeholder. | done | User enabled editing, native slide9 Title and Content applied and title saved as Az első 12 rekord mennyisége. Saved OOXML identifies Content Placeholder 2; robot configured to that actual placeholder. Validation succeeds with only ExcelProcessScope recommendation. Both Office files closed. |
| 3 | Run robot; verify success and12bars in both files/correct title. | done | Actual UiPath run20s, hasErrors=false/errorMessage=null. Native reopened Excel/PPT both visibly show12bars and exact title.21independent OOXML/data checks pass: all243data rows, original slide1-8paragraph text, exact12categories/values and pasted native chart. Verification compares paragraphs because Office merged text runs without changing content. |
| 4 | Save both outputs and visible evidence. | done | Actual executed project and12record outputs packaged in deliverables/RiportRobot/README.md;21checks, actual20srun and native reopened Excel/PPT screenshots included. Completion lock preserved and source bundles unchanged. Separate6record mini remains pending. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-07"></a>
## D4-07 — Six-record report mini-exercise

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-06.

Source: [04_excel_ppt.html](../nap04/pages/04_excel_ppt.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Use separate fresh copies preserving12record reports. | done | Fresh reports_6 copies from supplied originals; SHA256 matches source_manifest.json (4818ee... workbook,ac7f26... deck). Completed reports_12 and marker preserved. |
| 2 | Set A1:B7 and run actual robot. | done | Native fresh slide9 Title and Content/title saved; observed saved Content Placeholder2. Report_6.xaml uses A1:B7, separate run lock; validation only ExcelProcessScope recommendation. Actual UiPath run completed14s, hasErrors=false/errorMessage=null, Riport kész6rekord. report_6_run.json. |
| 3 | Verify6bars in Excel/PPT with successful Output. | done | Actual14s UiPath run and21independent output checks passed. Native reopened PowerPoint slide9 and Excel workbook both visibly show6bars; Excel accessibility confirms LA33/MI87/NJ58/AK82/OH38/OH54. report_6_excel_reopened.jpg and report_6_ppt_reopened.jpg saved; Protected View retained, no rerun. |
| 4 | Save separate reports/evidence. | done | Separate reports_6 and Report_6.xaml packaged with actual run/validation logs, both reopened native screenshots and21-check verification. package_verification.json confirms byte-identical copies, unchanged twelve-record files and both preserved run markers. Nap04 index/root summary updated:12of15required verified; portal/manual variant/final day handoff remain. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-08"></a>
## D4-08 — PDF/Excel/Word sorter

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-07.

Source: [05_fajlrendezo.html](../nap04/pages/05_fajlrendezo.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read ZIP; extract isolated working copy and record20files. | done | Current05lesson read fully; official CLI initialized Windows/VB Fajlrendezo. Isolated exercise/gyakorlo_mappa contains exactly20files:6PDF/4XLSX/5DOCX/3PNG/2TXT. ZIP traversal bounds checked and all original filenames/hashes saved in input_manifest.json. |
| 2 | Build top-only loop/folders/lowercase rules/full filename destinations. | done | Real CreateDirectory/ForEachFileX/If/MoveFile authored; loop top-only/filter*, lowercase extensions, full original filenames, Overwrite/ContinueOnError false and boundary log/rethrow. Per-file validation clean; resolved source/destinations checked inside isolated exercise directory. |
| 3 | Run robot; verify6PDF/4Excel/5Word,3PNG/2TXTroot and20preserved files. | done | Actual UiPath run completed2seconds, hasErrors=false/errorMessage=null,15move logs. Independent verification:6PDF/4Excel/5Word,3PNG/2TXTroot; all20filenames/content hashes preserved. [Evidence](../working/Fajlrendezo/verification_basic.json). |
| 4 | Save project and content/filename/count evidence. | done | Saved [clean project](../deliverables/Fajlrendezo/README.md), originalZIP, actual sorted output and separate evidence_basic_state snapshot; filenames/hashes/run linked. |

Handoff / exceptions: Independent execution while D4-06 awaits user Protected View action. Sorter consumes only its own ZIP and does not depend on either report output; course-order exception is limited to this independent work. D4-06/07 remain unfinished.

<a id="d4-09"></a>
## D4-09 — PNG sorter and second run

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-08.

Source: [05_fajlrendezo.html](../nap04/pages/05_fajlrendezo.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read mini and add Kepek/.pngrule. | done | Current mini read; separate Sort_With_Images.xaml adds Kepek before loop and .png lowercase Move File rule. Basic workflow/output snapshot preserved. Validation clean. |
| 2 | Run robot; verify3images moved and2TXTroot. | done | Actual UiPath run1completed1second,3MOVED / Kepek logs, hasErrors=false/errorMessage=null. Exactly3PNG in Kepek,2TXTroot; all20filenames/hashes preserved. verification_images_run1.json saved full state. |
| 3 | Run again; verify no further moves and20preserved files. | done | Actual unchanged second run completed0seconds, moved=0/noMOVEDlogs, hasErrors=false/errorMessage=null. Independent full relative-path/hash tree exactly equals run1,20files. verification_images_run2.json saved. |
| 4 | Save both run observations/project. | done | Saved [project/final20-file state](../deliverables/Fajlrendezo/README.md), separate basic snapshot, both actual PNG run verifications and logs. Main preserved. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-10"></a>
## D4-10 — Portal prerequisites

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-09; desktop/browser prerequisites.

Source: [06_urlap_robot.html](../nap04/pages/06_urlap_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read source/policy and copy portal/input to stable working paths. | done | Current06lesson reviewed. Stable readiness portal/input copies hash-identical to supplied assets;10rows/schema checked. Executed captured-target workflow hash equals pre-run evidence. Preserve existing case/reservation; offline review only. |
| 2 | User completes required extension/fileURL permissions by permitted handoff. | done | User installed official UiPath extension in Brave and enabled fileURL access. Actual user-started UiPath five-field submission/readback passed; stronger evidence than browser open alone. setup-01steps7/8 and PORTAL_TRIAL_RESULT.md retained. |
| 3 | User opens/logs into practice tab as required; verify field-level targeting. | done | Nine user-captured targets and actual trial saved:4TypeInto/SelectItem/Submit/CheckState/GetText/New-form. Actual K-GY-4147/TR-402318, five values/confirmation/export match;19checks passed. User login/session and user-operated identification verified; agent live file-page control remains prohibited. |
| 4 | Record browser/path/access evidence without credentials. | done | Saved [course portal status](PORTAL_COURSE_STATUS.md) with stable source paths, actual trial links and explicit user-operated/agent-access distinction. No credentials or new portal actions. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-11"></a>
## D4-11 — Manual practice claim

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-10.

Source: [06_urlap_robot.html](../nap04/pages/06_urlap_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read schema and establish20sample baseline. | done | Preserved CSV(3) in portal_baselines/pre_batch_export3_20261007;4own rows identical to(2), user-reported total24 implies20seeds. First policy exact once,19trial checks pass, other9absent, only original lock. baseline_review.json records evidence and limitations. No live portal action. |
| 2 | Enter first row manually; submit/confirm/new-form action. | done | Actual initial manual record all5fields exact in CSV(5); isolated replay success K-GY-4147/four summary fields then user-directed green new-record button produced visually empty form/default type/focused policy. Ordered replay_confirmation_user.png to new_record_cleared_user.png reviewed, new_record_clear_review.json saved. Wrong-copy duplicate detour reconciled: original CSV(6) unchanged. |
| 3 | Preserve evidence and reset only disposable added practice records as permitted. | done | Pre-reset CSV(7) preserved/all5fields exact. Actual final_reset_list_user.png shows MANUAL RESET TEST and20sample+0own=20total after user deletion. final_reset_review.json saves visual evidence. Original13own/33total verified unchanged in CSV(6); no agent reset/browser action. |
| 4 | Verify baseline/form before robot trial. | done | User final_reset_empty_form_user.png visibly confirms MANUAL RESET TEST/default type/empty description and placeholder inputs after verified20sample+0own reset. Final reviews and hashed evidence package saved at deliverables/PortalRobot/manual_reset_20261007/README.md. Original13own/33total and reservations preserved; no agent portal action or robot rerun. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

D4-11 step2 recovery branch2026-10-07, added before execution: current screenshot confirms five prior values remain after navigation. Confirmation new-record button is hidden after tab changes. Preserve already verified CSV(5)/success screenshot, then have user reset only the single isolated MANUAL RESET TEST own case and verify20baseline. Repeat manual first-row submission, click the green-confirmation new-record button before switching tabs, and verify empty form. This bounded recovery is part of unfinished step2; it does not complete later reset acceptance or replay the original portal/robot. See form_values_retained_review.json.

D4-11 resume2026-10-07: separate [manual reset copy](../working/manual_reset_20261007/manual_reset_portal.html), dedicated storage key and visible MANUAL RESET TEST badge prepared/verified offline under D4-P02. User replied20: isolated baseline confirmed by user; baseline_user_confirmation.json preserves the report. Manual submission screenshot verifies K-GY-4147 and four visible first-row fields. Actual CSV(5) now verifies all five fields/one own row; user confirms21total. Await new-form/empty-form action confirmation and reset; see manual_export_verification.json. Preserve original33cases and all locks. Follow staged [handoff](../working/manual_reset_20261007/HANDOFF.md); do not rerun the already completed robot batch.

<a id="d4-12"></a>
## D4-12 — One-row form robot

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-11.

Source: [06_urlap_robot.html](../nap04/pages/06_urlap_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Build Windows/VB UrlapRobot reading A1:F2. | done | Existing Windows/VB BPA_Setup_Smoke Portal_Logged_Trial reads bejelentesek A1:F2, headers true, guarded1row. Input/workflow hashes match actual successful trial; project-name/typedForEach variation recorded. |
| 2 | Attach logged-in tab; configure clear typing/Select Item and submit/wait/reset/Throw. | done | Unchanged user-captured Brave attachment has Open/Close Never;4clear TypeInto,SelectItem,oneSubmit,10sCheckState/GetText/New-form and Throw on absent confirmation. Same9targets proved by actual trial; no new live validation. |
| 3 | Run actual robot; verify first-row saved fields and Output. | done | Actual user-started trial passed K-GY-4147/TR-402318: all5saved fields match,19checks passed; ordered events/screenshots/readback and exported CSV agree. Exactly1newrecord,3prior unchanged. Evidence reused explicitly; no new agent-run claim. |
| 4 | Preserve evidence and reset only trial record as permitted. | done | Saved [minimal clean copied project](../deliverables/PortalRobot/README.md) with byte-identical executed trial, relative input layout, user screenshots and original reservation/log paths. Whole-project build Success=true; no portal run. Reset deferred/preservation alternative explicit; D4-11baseline subsequently verified in isolated copy. |

Handoff / exceptions: Reuse/review of an already executed readiness trial, not a new portal run. D4-11 exact manual/reset later passed in an isolated disposable copy; original trial record retained. Retain K-GY-4147/TR-402318 and reservation; no repeat submission or cleanup. Existing project name BPA_Setup_Smoke and typed DataRow ForEach are equivalent implementation variations; clean package preserves executed workflow unchanged.

<a id="d4-13"></a>
## D4-13 — Ten-row form robot

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-12.

Source: [06_urlap_robot.html](../nap04/pages/06_urlap_robot.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Restore full range and verify10input rows. | done | Prepared Portal_Batch_Resume.xaml reads full10rows/unique policies, skips only already verified TR-402318/K-GY-4147, keeps original reservation and9remaining rows. Captured target descriptors unchanged; validation clean and clean whole-project build Success=true. Guard baselineReviewed=False. [Preparation/handoff](../working/setup_2026-10-06/PORTAL_BATCH_HANDOFF.md). |
| 2 | Run actual robot with same tab and checked submission/reset. | done | User-started actual batch recorded14:37:11–14:39:15UTC. Parent completion checkpoint and nine ordered thirteen-event row logs present, no failure. CSV(4) saved; all171per-row checks pass including five exported fields/unique case IDs and screenshot files. No agent portal action or rerun. |
| 3 | Verify20+10=30, K-GY IDs and first/last policy/amount/type. | done | Actual CSV(4) matches all10source policies exactly once; nine new cases,13own, four prior rows unchanged and first policy remains K-GY-4147. User confirmed33displayed total.43batch/171row checks and visual review of all27PNGs pass. Blank unused ugyszam None/empty string serialization normalized only;11verifier tests pass. Cumulative24+9 adaptation, not clean20+10. |
| 4 | Save project/evidence/export; reconcile partial submissions before retry. | done | Actual batch files/export/logs/27PNGs/verification packaged byte-identically under deliverables/PortalRobot/actual_batch_20261007; batch_result.json summarizes43+171checks/33total. Offline verifier updated with11passing tests;10reservation locks preserved. No rerun, reset or portal action. Nap04 now13of15verified; D4-11exactmanual/reset and final handoff remain. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-14"></a>
## D4-14 — Robot/API/human choices

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: D4-13.

Source: [07_zaras.html](../nap04/pages/07_zaras.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read all five scenarios and selection criteria. | done | Current07_zaras.html read fully: all5scenarios and tool-choice criteria. Future assignment preview is not treated as complete specification or submission authorization. |
| 2 | Write choices addressing access, data structure/errors and human responsibility. | done | Draft covers all5scenarios, export-first HR, responsibility for credit decision, courier duplicate prevention, PDF extraction/OCR exceptions, API credentials/freshness and no unsolicited scheduler. |
| 3 | Check reasoning without inventing real records or later assignment details. | done | Compared all5choices with current source table: matching API/RPA/human/document-processing routes, access/error/responsibility reasoning included. No real records, invented assignment deadlines or operational scheduler. |
| 4 | Save decision notes. | done | Saved reviewed [five reasoned choices](../deliverables/robot_api_ember.md); all current scenarios covered, no external action performed. |

Handoff / exceptions: Independent reasoning task while Office/user-run portal steps await user actions. Scenarios use no report/portal outputs and no real records; dependencies on execution do not affect these standalone decisions.

<a id="d4-15"></a>
## D4-15 — Day4 runnable handoff

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: All required nap04 tasks.

Source: [07_zaras.html](../nap04/pages/07_zaras.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Review all required tasks and variants. | done | Reviewed all7current chapters and14required tasks/56steps, both threshold/report/sorter variants and exact manual/reset evidence. requirements_review.json records source hashes, preserved33case adaptation, optional exclusions and no graded submission. |
| 2 | Verify project dependencies/paths and actual runs/results. | done | handoff_verification.json passed5Windows/VBprojects/12actual prior run outcomes/306credential-scanned files incl decompressed archives; source XAML matches working, static inputs resolved,21+21Office checks/output hashes and19+43+171portal evidence retained. Pre-Studio batch delivery preserved and synchronized to actual working serialization; no robot/browser run. |
| 3 | Package clean runnable projects and outputs without sensitive/transient files. | done | Created additive BPA_nap04_verified_projects_20261007.zip;324files byte-verified, target resources/inputs/outputs/actual logs and completion markers included. Excluded caches/Office temporary locks; no originals deleted. archive_verification.json records hashes/exclusions. HANDOFF.md documents exact workflows, package versions, current-workspace paths and no duplicate reruns. |
| 4 | Save index and reconcile course summary. | done | Final index/root summary/access notes reconciled. Final additive BPA_nap04_final_handoff_20261007.zip325files byte-verified/credential-scanned; preliminary archive retained. Shared updater boundary regression passed and10historical evidence blocks repaired from preserved reports. All other day tasks done, including6user-opened views independently verified offline; direct local-browser layout inspection explicitly unclaimed. final_signoff_checks.json saved. |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d4-p01"></a>
## D4-P01 — Offline batch verification tooling

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: independent preparation, not actual portal execution. Dependencies: preserved actual one-row evidence and guarded batch draft. D4-11/13 need fresh user-exported baseline; this tooling reads saved files only and performs no portal/browser action.

Source: [06_urlap_robot.html](../nap04/pages/06_urlap_robot.html), original executed trial logs, prepared Portal_Batch_Resume.xaml.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Review saved CSV/input/event contracts and pending baseline requirements. | done | Existing semicolon export has6columns; actual trial verifier checks19conditions and saved PNGs. Batch has9policy child folders,10row root snapshot, parent batch_finished_pending_readback. Fresh baseline must contain only first input policy once, preserve every earlier own record and user total; no browser action. |
| 2 | Build offline cumulative verifier preserving prior records and checking each pending row. | done | File-only verify_portal_batch.py authored and compiles. Reuses19-check per-row verifier, validates all10source rows/9new records/exact snapshots/parent completion/prior records/counts. Requires separately user-reported total and visual review; performs no portal actions. |
| 3 | Test incomplete/duplicate/changed-record failures with isolated fixtures; package verifier and partial deliverable index. | done | Nine isolated synthetic verifier tests pass (portal_batch_verifier_tests.txt), including missing rows, duplicates, changed prior record, incomplete logs, wrong snapshot/value, pending baseline and total mismatch. File-only tools packaged under deliverables/PortalRobot/verification; partial nap04 index saved. Actual batch and visual review remain pending. Generated .local/.project caches remain after automatic approval review rejected cleanup; no removal ran. |

Handoff / exceptions: No fixture is actual batch evidence. Leave D4-13 blocked until user-run logs/export and visual review pass.
