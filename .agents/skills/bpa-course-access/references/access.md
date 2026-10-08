# Access procedures

Root `AUTOMATION.md` is the maintained status inventory. Recheck capabilities needed for the exercise; prior sign-in or a downloaded installer is not proof of current access.

## APIs

Run from BPA root:

```powershell
python nap03/working/bpa_access.py status
python nap03/working/bpa_access.py check
```

`status` prints filled/empty only. `check` performs live BTC/ETH EUR quotes and minimal EU CRM Leads read, creating no record. Reuse these helpers rather than another credential loader.

Only root ignored `.env.local` stores local credentials. Required external values: `CMC_PRO_API_KEY`, `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`. Bootstrap uses temporary `ZOHO_GRANT_CODE`; the helper generates `ZOHO_ACCESS_TOKEN`, `ZOHO_REFRESH_TOKEN`, `ZOHO_ACCESS_TOKEN_EXPIRES_AT`. Refresh removes the need for another grant every hour. Days1–4 require no OpenAI API key, Moodle API token or UiPath API key.

If initial Zoho access is absent, give these private steps: `https://api-console.zoho.eu`, existing Self Client, Generate Code, scope `ZohoCRM.modules.ALL`, duration10minutes if offered, description `BPA kurzus`, select own CRM organization, Create, copy into root `.env.local` as `ZOHO_GRANT_CODE`, save, report saved without pasting it in chat. Do not duplicate clients. User handles identity verification and sensitive console fields.

Immediately run `python nap03/working/bpa_access.py zoho-auth`, then `check`. The helper sends secrets in the EU endpoint's form body, atomically saves tokens, preserves unrelated settings and clears the consumed code. Expired/consumed grants need a fresh code; refresh is different. Never dump the environment or put secrets in URLs/arguments.

Import `CourseAPI` from `nap03/working/bpa_access.py` for working Python. `cmc_quotes((1,1027), 'EUR')` uses a header. `zoho('GET', 'Leads', params=...)` and `zoho('POST', 'Leads', payload=...)` target `www.zohoapis.eu/crm/v8`. Read actual signatures. Expiry refreshes before requests; rejected reads retry once; writes never auto-retry. After an uncertain write, search/read before retry. Require per-record `SUCCESS`, `success`, `details.id`, then read back the fictional record. Use `trigger: []` in lesson creations.

Do not copy keys into the lesson's URL examples, notebooks, workbooks, screenshots or shared script source. Prepare credential-free working variants using headers and runtime inputs. A UI exercise needing its own credential store requires a user-controlled secure path; do not silently substitute a static export or broaden approved secret destinations.

## Moodle and browser

Course: `https://econ.elearning.ubbcluj.ro/moodle/course/view.php?id=9525`. Reuse the authenticated in-app tab; check for login redirect. When expired, ask for private user sign-in in that tab, then resume. No password/cookie reading, fixed timeout assumptions or keep-alive job. Later-day outlines are not assignment specs; obtain the published resource when reached.

Use the in-app browser first. Read static lessons directly from files when `file:` is blocked; no server/proxy/alternative route to defeat that restriction. For an actual local practice UI use a permitted user/browser handoff. Read Computer Use instructions before Windows UI work and obey its authentication, privacy and permission restrictions. Office connector absence is not a blocker if native Office works.

## UiPath and Office

Use the current user's own Community organization. The author's former organization is not a transferable account or setup target. Verify current Community Plan and Studio entitlement before choosing an installer or project.

Each new user must install/license their own free Community Studio/Robot. Download the current official installer and validate its UiPath signature. Check current executables before relaunching. Do not assume historical install authorization or guess legacy ADDLOCAL flags. User handles security prompts, license acceptance and Studio sign-in privately. See SETUP.md and record actual current entitlement/run checks.

After installation verify Studio opens, Community/Pro, Windows+Visual Basic Process, package restoration and a Message Box run. Record observed version. Portal extension/file-URL permissions are separate; user handles restricted settings. Bootstrap updater alone is not a completed Studio installation.

Excel/PowerPoint are installed under `C:/Program Files/Microsoft Office/root/Office16`; verify working copies open when needed. Workbook activities need no Excel; chart activities need both desktop apps. Package choices must match Studio; use official UiPath documentation for changed activity names/schemas.

Sheets is an Excel alternative in nap03. Colab is explicitly used for its API chapter. Request private Google sign-in when needed. Local API results validate logic but do not prove Colab/Sheets execution. ChatGPT browser exercises use an authenticated AI interface, not an OpenAI API key. Account privacy choices remain user-controlled.
