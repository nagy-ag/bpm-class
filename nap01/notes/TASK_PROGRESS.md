# nap01 task progress

Follow [the mandatory workflow](../../TASK_PROGRESS.md) before every action. Runbook steps specify implementation; this file records execution. Update one logical step at a time, with evidence before advancing. Mini-exercises and variants have their own IDs.

Initialized 2026-10-06. Completed entries carry forward prior dated evidence; this tracker does not claim new course execution. Unassigned partial entries need a new agent claim before resuming.

| Task | Scope | Status | Next step |
| --- | --- | --- | --- |
| [D1-01 — Café model](#d1-01) | required | done | None |
| [D1-02 — Morning routine mini-exercise](#d1-02) | required | done | None |
| [D1-03 — CoinMarketCap lesson and quote mini-exercise](#d1-03) | required | done | None |
| [D1-04 — First manual fictional Zoho lead](#d1-04) | required | done | None |
| [D1-05 — UiPath installation and smoke robot](#d1-05) | required | done | None |
| [D1-06 — AI account and instruction setup](#d1-06) | required | done | None |
| [D1-07 — AI output checks and mini-prompt](#d1-07) | required | done | None |

<a id="d1-01"></a>
## D1-01 — Café model

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: None.

Source: [01_folyamatabra.html](../nap01/pages/01_folyamatabra.html).

Migrated 2026-10-05 editor verification; not rerun for tracking.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read the lesson and supplied model; confirm the named start, three tasks and end. | done | [Course evidence](../../PROGRESS.md), [model](../deliverables/kave_rendeles.bpmn) |
| 2 | Build and save kave_rendeles.bpmn with valid BPMN geometry. | done | [Course evidence](../../PROGRESS.md), [model](../deliverables/kave_rendeles.bpmn) |
| 3 | Reopen supplied example and own model in bpmn.io; verify the sequence. | done | [Course evidence](../../PROGRESS.md), [model](../deliverables/kave_rendeles.bpmn) |
| 4 | Link final model and editor verification. | done | [Course evidence](../../PROGRESS.md), [model](../deliverables/kave_rendeles.bpmn) |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.

<a id="d1-02"></a>
## D1-02 — Morning routine mini-exercise

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task in lesson order.

Source: [01_folyamatabra.html](../nap01/pages/01_folyamatabra.html).

Sample routine, not a factual claim about user habits.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read the mini-exercise and distinguish a sample from the user's actual routine. | done | [Course evidence](../../PROGRESS.md), [sample model](../deliverables/reggeli_rutin.bpmn) |
| 2 | Build at most six named activities with start/end; save reggeli_rutin.bpmn. | done | [Course evidence](../../PROGRESS.md), [sample model](../deliverables/reggeli_rutin.bpmn) |
| 3 | Reopen and check order, reachability and labels. | done | [Course evidence](../../PROGRESS.md), [sample model](../deliverables/reggeli_rutin.bpmn) |
| 4 | Link final model and disclose that this is a sample. | done | [Course evidence](../../PROGRESS.md), [sample model](../deliverables/reggeli_rutin.bpmn) |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.

<a id="d1-03"></a>
## D1-03 — CoinMarketCap lesson and quote mini-exercise

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: Previous applicable task in lesson order.

Source: [02_coinmarketcap.html](../nap01/pages/02_coinmarketcap.html).

API access is verified; chapter demonstrations and quote evidence remain separate.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read current lesson and public demo requirements. | done | Current refreshed lesson and nap01 tasks runbook read; public listings demo then BTC/ETH EUR request. Existing access recheck passed2026-10-07; use HTTP header for key, not lesson URL-key demo. |
| 2 | Verify existing approved free account/key and live BTC/ETH EUR API access. | done | [Access inventory](../../AUTOMATION.md) |
| 3 | Try the public demo; record actual success or service limitation. | done | In-app browser attempted the supplied unauthenticated listings URL2026-10-07; net::ERR_BLOCKED_BY_CLIENT. Record limitation; no paid setup or alternate route attempted. |
| 4 | Retrieve BTC and ETH prices safely; record numeric EUR quotes and retrieval time without credentials. | done | Actual CourseAPI request2026-10-07T09:26:29Z returned BTC74902.68393311542 and ETH2328.532061121165 EUR; response/observation saved under working/cmc_exercise. |
| 5 | Verify JSON status/paths and save the quote/concept evidence. | done | Saved response independently checked: error_code0, null error_message normal, expected IDs/symbols/paths, numeric finite positive prices. [Quotes](../deliverables/coinmarketcap_quotes.json), [Hungarian explanation/demo limitation](../deliverables/coinmarketcap_notes.md). |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.

<a id="d1-04"></a>
## D1-04 — First manual fictional Zoho lead

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: EU CRM access; no duplicate course lead.

Source: [03_zoho.html](../nap01/pages/03_zoho.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read source fields and verify EU CRM/session. | done | Refreshed lesson fields read; authenticated crm.zoho.eu orgREDACTED_AUTHOR_CRM_ORG Home loaded in-app2026-10-07. |
| 2 | Check whether Kiss Márta / Corner Shop already exists. | done | All Leads UI shows exactly10sample records, Next disabled. No Kiss/Corner Shop record; no creation retry needed. |
| 3 | Create the lead through UI only if missing; preserve sample data. | done | Authorized Phone option added through Leads Standard layout Edit Properties; all 16 prior choices retained and default unchanged. Fresh All Leads UI had exactly 10 samples and no course identity. Created one Kiss/Márta, Corner Shop Kft, marta.kiss@cornershop.example, supplied phone, Source Phone through Create Lead UI. Saved record URL /Leads/1037931000000654026; no retry. |
| 4 | Reopen and verify all fields plus Timeline; save fictional record evidence. | done | Saved record 1037931000000654026 detail verifies Márta Kiss / Corner Shop Kft, exact fictional email/phone and Lead Source Phone. Timeline History shows Lead Created 07.10.2026 02:50 PM. Screenshots working/zoho_lead_overview.png and zoho_lead_timeline.png preserved. No calls/messages or sample modifications. Final evidence at deliverables/zoho_lead_verification.json. |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.

<a id="d1-05"></a>
## D1-05 — UiPath installation and smoke robot

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: Shared access-04.

Source: [04_uipath.html](../nap01/pages/04_uipath.html).

Independent from the blocked Zoho picklist decision. Reuse completed shared setup-01 license/packages; this lesson requires a separate Proba project and the exact course message, which differs from the earlier readiness smoke.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson; verify existing Community organization and authorized installation. | done | [Setup inventory](../../AUTOMATION.md) |
| 2 | Finish existing installation and privately signed-in desktop Studio; verify license. | done | Actual shared setup-01 steps4–6 passed: Studio2026.0.203STS Community/Pro, System26.8.2, Message Box and workbook runs. Evidence retained in setup README; no reinstall/sign-in. |
| 3 | Create Windows/VB Proba project, restore packages and add the Message Box. | done | CLI init created Windows/VB Proba with System26.8.2. Exact message displayed in native designer. Per-file validation no diagnostics; whole build Success=true, only Hub URL/default name/log warnings. [Validation](../working/proba_validate.txt), [build](../working/proba_build.txt). |
| 4 | Run; observe correct message and successful completion after OK. | done | Actual desktop run displayed Fut az első robotom!; observed dialog and clicked its OK. CLI Data.output=Session ended, errors=[], debugState=Completed, duration00:00:58. [Run](../working/proba_run.txt), [dialog](../working/proba_dialog.jpg). |
| 5 | Save runnable project and version/run evidence. | done | [Clean runnable project](../deliverables/Proba/project.json), [verification](../deliverables/Proba_verification.json). Main/project files match executed version byte-for-byte; cache omitted. Warnings recorded, no errors. |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.

<a id="d1-06"></a>
## D1-06 — AI account and instruction setup

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: Previous applicable task in lesson order.

Source: [05_chatgpt.html](../nap01/pages/05_chatgpt.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson and inspect the permitted authenticated AI interface. | done | Current lesson explicitly permits another AI tool. This active authenticated Codex session is the selected tool; response generation and file authoring work. No new account or API key needed. |
| 2 | Prepare adapted Hungarian instructions without overwriting unrelated preferences. | done | [Scoped instruction draft](../deliverables/ai_course_instructions.md) uses known BPA context and preserves global preferences; no assumed degree facts. |
| 3 | Apply permitted instruction changes or record exact user-only setting handoff. | done | Scoped instruction file read into this AI session for the next exercise; each saved prompt includes it explicitly. Separate global settings handoff is in the same file; global persistence not claimed. |
| 4 | Record optional memory/data-control choices only when provided by the user; link configuration evidence. | not_applicable | Optional choices not supplied; no change required. [Configuration and global-setting handoff](../deliverables/ai_course_instructions.md). Completion covers permitted Codex/direct-prompt route, not global ChatGPT setting persistence. |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.

<a id="d1-07"></a>
## D1-07 — AI output checks and mini-prompt

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: required. Dependencies: Previous applicable task in lesson order.

Source: [05_chatgpt.html](../nap01/pages/05_chatgpt.html).

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read required prompt checks and prepare separate explanation/example counts. | done | [Exact prompts](../working/ai_prompts.json): explanation3sentences, summary2paragraphs, mini5explanation sentences plus3separate examples. Each includes explicit scoped preamble. |
| 2 | Run business-process explanation and summary tests. | done | Actual current-model outputs saved in working/ai_explanation.txt and ai_summary.txt. No independent model/global-setting test claimed. |
| 3 | Run five-sentence explanation plus three insurer examples. | done | Actual current-model output saved in working/ai_mini.txt, with separate explanation/examples blocks. |
| 4 | Evaluate actual language, counts/style; refine and rerun if needed. | done | All7programmatic checks pass in working/ai_evaluation.json. Hungarian semantic review completed; first outputs pass, no rerun needed. |
| 5 | Save prompts, outputs and evaluations; index nap01 artifacts. | done | [Exact prompts/actual outputs/checks](../deliverables/ai_prompt_checks.json), [readable outputs](../deliverables/ai_prompt_checks.md), [day index](../deliverables/README.md). Global-setting test explicitly excluded; Codex permitted alternative used. |

Handoff / exceptions: None recorded beyond the evidence or blocker above. Update this line when scope, source requirements, ownership or retry safety changes.
