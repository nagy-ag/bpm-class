# Current automation access — 2026-10-07

Supplied nap01–nap04 execution and expanded feature checks are verified. [Current course summary](PROGRESS.md), [nap04 handoff](nap04/deliverables/HANDOFF.md). API credentials remain in ignored.env.local and matching-service calls use the canonical helper. No account passwords are stored.

Native Office/Studio and all five robot projects have actual lesson runs; portal runs are user-started. The portal original33case result/reservations remain intact; isolated manual/reset passed20sample/0own/empty form. Google Sheets manual/SOL/hourly tests passed and its practice trigger was removed. Colab clean notebook download passed. Two automatic canonical CMC-fetch/native-Excel-Power-Query saves passed. Direct CMC credentials-from-env Power Query failed privacy firewall; use the approved Python+Power Query adaptation. Website re-login is excluded; expired web sessions need private user sign-in. No new access permission or API key is needed for the supplied lessons. Six result views opened by user; independent offline substantive content/assets/simulation-summary review passed. Direct agent browser visual/layout inspection remains unavailable. Later unpublished assignments remain unknown.

The inventory below is historical setup evidence; pending lesson statements there are superseded by this current summary.

# Course automation access

Updated 2026-10-07. The user delegated execution of the course exercises to Codex. Follow the course order and keep supplied nested bundles read-only. This file records capabilities and outstanding access steps; it is not a claim that the coursework is complete.

| Capability | Verified status | Next step |
| --- | --- | --- |
| Local lesson files, BPMN, Python | Accessible. Python 3.12 and Node are installed; nap02 deliverables already exist. | Read each task and work in its outer day folder. |
| CoinMarketCap | Live BTC/ETH/SOL EUR quotes passed using the local key in an HTTP header. | Use the shared API helper for exercises. |
| Zoho CRM EU | OAuth exchange and forced renewal passed. Leads/Accounts/Contacts/Deals reads passed; uniquely tagged fictional Lead create/read/update/read/delete passed with cleanup verified. Authenticated CRM browser accessible. | Shared helper refreshes API access. Actual course conversion/UI steps remain; website sign-in is separate. |
| Moodle course | Live lesson navigation initially revealed a timeout. After the user's fresh private sign-in, actual course and nap04 lesson navigation passed. | Reuse authenticated sessions. On 2026-10-07 the user accepted private manual sign-in when needed; unattended re-login is no longer a required setup task. |
| UiPath Automation Cloud | Free Community organization `BPAcourseautomation` created with the user's specific approval. License page shows Community Plan and one Pro license with Studio access. | Desktop Studio sign-in and Community/Pro license verified under setup-01. |
| UiPath Studio | Studio2026.0.203STS native start screen, private desktop sign-in, Community License/Pro entitlement verified. Windows/VB test project restored official System26.8.2, Excel3.6.1, UIAutomation26.10.5 and Presentations2.6.1. Message Box, workbook read/write and user-started portal one-row trial passed with saved output verification. | Setup items1–3 complete. [Checkpoint](TASK_PROGRESS.md), [portal result](nap04/working/setup_2026-10-06/PORTAL_TRIAL_RESULT.md). Preserve tested workflows; actual course assignments remain separate. |
| Excel | Native creation/edit/recalculation42→50/save/reopen passed. Local Power Query import/refresh2→3rows passed; saved result and query connection verified. | Native execution works; live CMC Power Query remains its separate lesson check. [Evidence](READINESS.md). |
| PowerPoint | Native editable chart paste and title editing passed; saved/closed/reopened deck verified with values15/25/30. Original course copies preserved. | Blank-deck readiness passed. User handles Protected View trust when editing original supplied working copies. [Evidence](READINESS.md). |
| Live Office connector | No connected Codex document sessions were found. | Native Computer Use and file-based artifact tooling remain available; a connector is optional. |
| Google Colab | Saved credential-free smoke notebook executed successfully in a connected Python3 runtime, including arithmetic/strict-threshold assertions. | Reuse authenticated session; actual course API chain/credential input remains separate. |
| BPMN / BIMP | Plain diagram imported without warnings; BIMP completed a fresh 100-instance baseline test. Generic editor warns about QBP extensions, and its download event did not complete. | Keep parameterized files out of generic-editor saves. Browser export remains unverified; preserve existing local artifacts. |
| Local practice portal | 2026-10-07: user captured nine Brave targets and started the actual one-row UiPath trial. Case K-GY-4147 / TR-402318 verified against logs, snapshot, screenshots and exported saved records: all five values match, no duplicate, three prior records unchanged. [Evidence](nap04/working/setup_2026-10-06/PORTAL_TRIAL_RESULT.md). | User-operated UiPath connection/run verified. Agent fileURL control remains prohibited, including indirect/alternate-surface workarounds. Retain policy lock; future coursework batch must account for the existing first case. This does not verify unattended authentication. |
| Google Sheets / Apps Script | Separate spreadsheet and script permission checks are not yet performed. This is an alternative to Excel for nap03. | Verify only if this path is selected; user handles restricted authorization prompts. |
| Later assignments | Moodle days 5 and 16 opened with empty resource lists; days 7 onward were shown as unavailable in the main outline. | Check published requirements when reached. Do not infer deadlines or fabricate missing assignments. |

Moodle course: [Automatizarea proceselor de business](https://econ.elearning.ubbcluj.ro/moodle/course/view.php?id=9525).

## Credential workflow

Keep API credentials only in the ignored root `.env.local`. Passwords, OTPs, browser cookies, and Moodle session tokens must not be copied into project files. Logs, notes, and deliverables contain no credential values. Root and nap03 instructions were reconciled with the user's explicit authorization of the local credential store.

Run these commands from the BPA root:

```powershell
# Report only whether each credential field is filled.
python nap03/working/bpa_access.py status

# Check CMC and CRM without creating exercise records.
# If a grant code is available, this also completes initial Zoho authorization.
python nap03/working/bpa_access.py check

# Explicitly exchange a new grant code or renew with the stored refresh token.
python nap03/working/bpa_access.py zoho-auth
```

The PowerShell token helper selects a fresh grant code first, otherwise a refresh token. It saves the generated tokens and expiry time, clears a consumed grant code, and preserves unrelated `.env.local` content. API code renews expiring tokens before requests, retries a rejected read once after refresh, and does not automatically repeat CRM writes after an uncertain outcome.

Future nap03 working scripts can import `CourseAPI` from `bpa_access.py` and call `cmc_quotes()` or `zoho(method, resource, params=..., payload=...)`. Keep returned CRM records in memory unless they are fictional course data intentionally being used for a deliverable. Never print the credentials dictionary or token responses. For course record creation, use fictional data and `trigger: []` as the supplied lesson scripts do; do not trigger email or workflow actions without specific authorization.

Reference: [Zoho token renewal](https://www.zoho.com/crm/developer/docs/api/v8/refresh.html), [Zoho records API](https://www.zoho.com/crm/developer/docs/api/v8/get-records.html), [CoinMarketCap documentation](https://coinmarketcap.com/api/documentation/).

## Browser and desktop operation

Use the in-app browser first. It rejects `file:` lesson URLs under browser security policy; read those static files directly from the filesystem. Do not add a server, proxy, or alternate browser route to bypass that block. The locally supplied practice-portal UI still needs an allowed user/browser workflow when reached.

Windows Computer Use through `@oai/sky` is available and was verified against Excel. Follow its skill's confirmation and authentication restrictions. Browser session access does not expose or require the user's password. Do not read password fields, browser password stores, or cookies to reuse a session.

Zoho API access and Zoho website sign-in are separate. The configured refresh token renews API access while it remains valid; it does not authenticate browser pages. Website access reuses existing signed-in sessions. On 2026-10-07 the user accepted handling private sign-in or verification when required. Unattended re-login remains unverified and is no longer a required setup task; do not store passwords or log out solely to test it.

Run course exercises, inspect results, and save outputs in the matching outer day folders. Use actual UiPath workflows for UiPath-specific assignments; a Python substitute does not prove a robot ran. Prepare graded submissions for review and obtain the user's instruction for the particular final submission. Account creation, installations, and access changes remain subject to applicable tool confirmation rules.

## Validation

Representative cross-course tests and exact remaining actions are recorded in [READINESS.md](READINESS.md). Browser/API/file, native Office, Studio desktop licensing/packages, actual Message Box/workbook robots and user-started Brave portal one-row trial/readback passed. User-requested setup items1–3 are complete. Unattended website re-login and course-specific assignments remain separate. No extra API key is currently required for supplied nap01–nap04.

Seven offline Python checks passed for expiry refresh, read-versus-write retries, key-in-header handling, literal credential loading, safe error output, and refusing redirects/resource escapes. A separate mocked exchange passed under native Windows PowerShell 5.1, including saving expiry and clearing the consumed code. The live CMC check succeeded. Live Zoho initial exchange, subsequent refresh and EU CRM read succeeded on 2026-10-06; the helper cleared the redeemed grant and saved generated tokens without displaying them.

## Reusable execution skills

Five installed skills cover shared access and all 24 nap01–nap04 chapters. See [SKILLS.md](SKILLS.md) for entrypoints and [course_skill_manifest.json](course_skill_manifest.json) for source freshness. Skill creation does not change course completion status.
