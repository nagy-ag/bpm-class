# nap03 execution and acceptance

Source prefix `nap03/nap03/`. Read current pages/scripts as the block begins. Remote interface/version facts need official documentation when uncertain. Never follow old screenshots over the corrected supplied code.

## 1 — pages/01_api_alapok.html

Explain provider, endpoint, `id=1,1027`, `convert=EUR`, GET/POST, header/body authentication and JSON object-vs-list traversal. Inspect `docs/cmc_pelda_valasz.json`, explicitly invented prices. Validate `data['1']['quote']['EUR']['price']`, analogous ETH path, and null error_message with error_code0. The updated intro removed its old JSON mini-task; don't invent a mandatory deliverable for it. Concise concept notes suffice.

## 2 — pages/02_excel_power_query.html (spreadsheet option A)

Actual Power Query refreshable workbook, not a static pandas/openpyxl export. Query live BTC/ETH EUR, navigate root data→IDs→name/symbol/quote→EUR→price and percent_change_24h. Decimal numeric types, distinct rows, ID column renamed CMC_ID or removed; crypto-name column Név. Close & Load, then prove Refresh issues a new request; unchanged prices can be legitimate caching.

The supplied URL-key demo conflicts with approved secret handling. Prepare M/query transformations with placeholders/runtime credential input; never embed key in saved workbook/query/URL. Determine an allowed credential mechanism before finalizing a direct refreshable query. If no approved secret-free persistence mechanism is available, keep the UI chapter pending and offer the allowed Sheets path or a separately labeled local-fetch/import adaptation. A data snapshot is not completion of this requirement.

Mini: add SOL CMC_ID5426, bold headers, two-decimal price, green/red24h changes. A raw2.1 is2.1%, not210%; divide by100 before percentage formatting or use literal-percent custom `0.00"%"`. Refresh twice one minute apart; record time and changes without inventing movement. Properties60-minute refresh works only while workbook open; opening-refresh is separate. No unattended scheduled job is implied by demonstrating the setting.

## 3 — pages/03_google_sheets.html (spreadsheet option B)

Read `docs/cmc_sheets_script.txt`; copy/adapt to working source. Bound script from spreadsheet Extensions→Apps Script, function `arfolyamFrissites`. Replace URL-key/hardcoded key approach with header plus an approved user-controlled runtime/secret mechanism, leaving exported source credential-free. User handles Google sign-in and restricted permission dialogs; if institution blocks Apps Script, select Excel if usable or ask only for the missing access choice.

Observe function run and ARFOLYAMOK A1:C3 headers/2coins/prices/timestamp; rerun updates timestamp. Mini IDS1,1027,5426 yields A1:C4. Source clears A:C: use its dedicated output sheet, never overwrite unrelated user cells. The lesson demonstrates one hourly time-driven trigger then deletes it after practice. Use app automation tools for that explicit exercise, respecting authorization; record trigger creation and cleanup. Do not leave an ongoing credit-consuming trigger or create a second scheduler as a substitute. If not exercised, record it pending.

## 4 — pages/04_zoho_crm.html (manual UI)

Reuse nap01 Kiss Márta/Corner Shop lead. Read nap01 Zoho page for missing fields. Create second fictional lead: Last_Name Nagy, First_Name Péter, Company Family Foods Kft, Email peter.nagy@familyfoods.example, Lead Source Trade Show. Verify existing records before duplicating.

Inspect Kiss Timeline, Convert to linked Account Corner Shop Kft and Contact Kiss Márta, with **Create a new Deal** selected. Deal `Corner Shop induló rendelés`, Amount4500, Closing Date about30days after execution, Stage Qualification, currency actually configured in account (don't force LEI from screenshot). Verify all3links, then pipeline Stage Needs Analysis, or content-equivalent next stage if customized; opening record and editing Stage is allowed if drag fails.

If existing matching Account/Contact offered, compare actual fields before Add to existing; name alone isn't identity. Reuse verified earlier conversion and explain current state rather than converting twice.

Manual Account `Kék Duna Étterem Kft`, Billing City Kolozsvár. Add related Contact Last_Name Molnár, First_Name Eszter, Email eszter.molnar@kekduna.example, correct Account link. Verify contacts/corporate links and CornerShop pipeline. Mini convert Nagy Péter with deal `Family Foods próbarendelés`, Amount2800; count observed UI steps, never invent a click count. Other deal fields follow current mandatory UI/lesson conventions. API lead creation doesn't automate this entire conversion exercise.

## 5 — pages/05_zoho_api.html (Colab/API)

Read `docs/zoho_token_colab.py`, `zoho_refresh_colab.py`, `zoho_lead_colab.py`. EU Self Client, ZohoCRM.modules.ALL, fresh one-use short-lived grant. Shared local authorization may already be complete; reuse refresh token rather than create another client. Colab does not read the local `.env.local` automatically.

Create `BPA_Nap3_Zoho.ipynb`, run `print("Szia, BPA!")`, and establish the Colab runtime. Prepare cells from working copies with hidden user input/runtime variables (no saved values or token prints). If user needs to supply credentials to Colab, keep it a private interaction and honor approved destinations; don't upload `.env.local`. Same runtime passes ACCESS_TOKEN in memory; restart loses variables. Refresh cell renews access; reusing redeemed grant is not refresh.

Fictional sample fields: Last_Name Teszt, First_Name API, Company Atlas Market, Email api.teszt@example.com, Lead_Source API, Description explaining course record. POST `/crm/v8/Leads`, `data:[lead]`, `trigger:[]`. Success requires HTTP success (normally201), row codeSUCCESS/statussuccess/details.id, then exact readback and visible CRM record/Timeline. API Teszt is display of First/Last, not literal Last_Name. Validate mandatory fields/custom picklist availability if account differs.

Mini: distinct fictional Last/First/Company/Email and contextual Description, then verify returned ID. Store only deliberately fictional exercise details/IDs in evidence. After network/ambiguous response search/read existing record before retry; no blind duplicate writes. INVALID_TOKEN refresh; OAUTH_SCOPE_MISMATCH examine scope; MANDATORY_NOT_FOUND inspect required fields; DUPLICATE_DATA inspect existing entity.

## 6 — pages/06_mini_lanc.html

Read `docs/arfolyam_riasztas_colab.py` and `.bpmn`. The timer symbol is planned operation; today's script is **one manual run per test**, not an hourly automation. Default threshold50000EUR, BTC_ID1; numeric finite positive live price. Conditions strictly `price > threshold`: equality also means no record.

Run same Colab runtime with established token and privately supplied CMC access. Working variants use header authentication. Choose below-current threshold for positive branch; require successful lead creation/readback with name starting `ÁRJELZÉS BTC`, Company `Árfigyelő automatizmus`, Description price/threshold, trigger[]. Choose above-current threshold for negative branch; verify no new lead from that run. Market may move: record actual price/threshold/time and outcome. Test equality with a controlled offline quote fixture separately from live evidence.

This creates a **Lead**, not CRM Task or notification, and sends no email. An API quote alone isn't chain success. Save branch log, fictional IDs and credential-free notebook/script; supplied BPMN may be copied as illustration. Do not schedule or expand scope. Day6 preview (40fictional leads) lacks current assignment details; wait for published requirements before graded work/submission.

## Completion package

Deliverable index links chosen spreadsheet and refresh evidence, concepts/manual CRM notes, runnable credential-free notebook/scripts, two distinct API leads, conversion/account/contact/deal checks and both chain branches. Separate local preparation, cloud execution and UI verification. For exported notebooks strip sensitive outputs and metadata before saving; original read-only scripts remain unchanged.
