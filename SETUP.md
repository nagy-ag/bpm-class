# Set up on another Windows laptop

## 1. Get the project

Install Git and Python 3.12+ (enable Python's PATH option). In PowerShell:

```powershell
git clone https://github.com/nagy-ag/bpm-class.git
cd bpm-class
./harness/setup.ps1
```

If PowerShell blocks an unsigned downloaded script, review it and follow your laptop's normal script approval process. You can run the same steps manually without changing security policy:

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -m harness.cli init
./.venv/Scripts/python.exe -m harness.cli doctor
```

Use `.venv/Scripts/python.exe` instead of `python` below if your default Python does not have the dependencies. No environment activation is required.

The repository contains code/skills/tests, **not the napXX folders or completed lesson files**. Obtain your own lesson ZIPs from the course, place them in `lesson-downloads/` (or the checkout root), and explicitly ask `$bpa-import-lessons lesson-downloads/nap01.zip`, then the other days. This safely extracts/inspects sources and keeps them local-only. The importer never solves tasks. When you request solving a day, the agent reads those current lessons and starts its fresh revision task plan. Offline code tests run without the professor's bundles; platform/course tests require the local assets.

## 2. Open in Codex

Open this cloned folder as a **local Windows project** in the Codex desktop app. Sign in to your own account. The seven skills live in `.agents/skills`; restart/reopen Codex if they do not appear. Do not copy another user's global Codex settings, login/session files or plugins cache.

For desktop control: open **Plugins → Computer Use → Install/Enable**, turn on its **server and skill** toggles, then **Try now**. In **Settings → Computer use**, review app access and approve the specific apps when prompted. Keep Windows unlocked with the target app visible during a run. Availability depends on account, region and administrator controls. The built-in browser is used first for web work. See [CAPABILITIES.md](harness/CAPABILITIES.md) for agent-side checks. Ask Codex:

> Use the repository's $bpa-course-access. Read AGENTS.md and harness/WORKFLOWS.md. Use my fresh .bpa progress. Check which browser and native computer tools are actually available, then complete the setup acceptance steps in SETUP.md. Do not assume the author's access or completion applies to me.

The agent must actually open a harmless public page with its browser tool and verify a harmless native application read/action when the tool permits it. A shell doctor cannot verify tool availability. If native control is unavailable, the agent uses permitted integrations/offline work and gives exact short user actions. Git cannot transfer Codex permissions, account entitlements or overcome a restricted file page.

Prefer a short clone path such as C:\src\bpm-class for Studio resource paths. If Git reports long-path errors, use `git -c core.longpaths=true clone` with the same URL in a shorter parent folder; no system-wide policy change is needed.

## 3. Supply your own accounts and keys

Setup creates a blank root `.env.local` from `.env.example`. Fill it privately in your editor:

- CMC: create your own CoinMarketCap Developer API key → CMC_PRO_API_KEY.
- Zoho EU: API Console → Self Client → Client ID/Secret. Generate a fresh code with scope `ZohoCRM.modules.ALL` for your fictional course CRM. Save ZOHO_GRANT_CODE and immediately run the check below. The helper exchanges it, clears the single-use code and maintains access/refresh tokens.
- Moodle, Google and UiPath: sign in privately when prompted. Never add website passwords, cookies or verification codes to files or chat.

```powershell
python harness/course_tools/day03/bpa_access.py check
```

This checks live API access and may exchange/refresh Zoho tokens. The helper currently targets Zoho **EU**; a non-EU account needs an explicit regional adaptation first. Do not reuse the author's CRM records or permission state. Picklist Phone and course account relationships must be checked in your CRM before fictional inserts.

In `.bpa/config.json`, enter **your own** Colab, Google Sheet and Apps Script URLs after creating copies from the tracked notebook/script sources. For Sheets, set CMC_PRO_API_KEY in the bound script's private Script Properties; authorize privately. Colab prompts for runtime credentials privately; clear runtime state before exporting the output-free notebook. Review live service requirements before authorization.

## 4. Install course desktop tools

Install/activate desktop Microsoft Excel and PowerPoint. Install UiPath Community Studio **with Robot**, then sign in with your own entitlement. Open a fresh Windows/Visual Basic project and restore its declared packages. The reference projects pin System 26.8.2, Excel 3.6.1, UI Automation 26.10.5 and Presentations 2.6.1 where used. Resolve any current compatibility issue in a new work copy and record it; do not silently upgrade reference evidence.

Use a Studio-supported Edge/Chrome browser for the course robot. Enable the official UiPath extension and **Allow access to file URLs** yourself. Brave was used on the author's machine; verify it independently if choosing Brave. Normal-window practice does not require private-window access. Browser selectors may need user recapture on another installation.

Optional authoring CLI, only if a workflow needs it: install Node.js, then:

```powershell
npm ci --prefix harness/tooling
./harness/tooling/node_modules/.bin/uip.cmd tools install '@uipath/rpa-tool@1.202.1'
./harness/tooling/node_modules/.bin/uip.cmd skills install --agent codex --path .bpa/tooling
```

Read the returned official uipath-rpa skill path and its required references before CLI authoring/validation. The repo day skills route agents there. Use `--help` on the installed version for current arguments. The downloaded upstream skill/runtime cache stays private under .bpa or the tool's user store. Studio can open/restore/run projects without this optional CLI; it does not replace Studio licensing. Do not copy another user's CLI login store.

## 5. Run offline checks, then actual platform checks

```powershell
python harness/verify.py
python -m harness.cli doctor
python -m harness.cli prepare ExcelRobot
```

Record actual checks in local shared setup tasks, in order:

| Check | Pass evidence |
| --- | --- |
| Browser and private sessions | Tool opens public page; own Moodle/Google/Zoho page authenticated. Session expiry asks for private sign-in. |
| API | CMC quote and Zoho access check succeed without exposing credentials; fictional test record read back only as the lesson requires. |
| Excel / PowerPoint | Fresh workbook formula recalculates; local Power Query refreshes and saves/reopens; native chart appears in fresh presentation. |
| Studio | Licensed Windows/VB project, packages restored, validation passes, real Message Box and workbook read/write run complete with matching outputs. |
| CMC auto-refresh | Prepare CMC_auto_refresh, run `./harness/configure-cmc.ps1`, then actual Studio run; JSON and workbook timestamps advance, values match. |
| Portal | Prepare PortalRobot; user captures targets, reports baseline, starts one fictional trial and exports CSV. Verify before batch (WORKFLOWS.md). |
| BIMP / Colab / Sheets | Actual model simulation/export/heatmap; actual notebook positive/no-write branches; actual manual and optional time-driven Sheets refresh with cleanup proof. |

A fresh clone contains reusable code, task plans and verification tools; it is not platform-verified. This laptop must pass its own actual runs before its tasks are marked done.

The root summary describes historical reference runs; their day-folder artifacts are retained only on the author's laptop. Shared robot templates contain code, not completed workbook/deck outputs or transferable proof. Missing source files do not count as source verification. `prepare CMC_auto_refresh` additionally requires a locally created native CMC workbook from its prerequisite lesson; it is not distributed.

## 6. Work through the class

Ask: **“Use $bpa-nap01 and complete the first unfinished task step by step. Keep my local progress current. Ask me only for a necessary private sign-in or exact UI action.”** Then proceed nap02 → nap03 → nap04. Final graded submission needs your specific instruction.

Your local work is `.bpa/`; keep it backed up privately. Git pull updates reusable files and leaves it untouched. Do not erase completed-run reservations to retry; reconcile ambiguous output first.

Two optional repo-local maintenance commands are available after opening this checkout in Codex: `$bpa-import-lessons ZIP` and `$bpa-audit-injections TARGET`. Both require explicit invocation. ZIPs are extracted first into safe staging; old completion is preserved and updated-source coursework starts only on a later solve request. Root ZIP downloads and `lesson-downloads/` are ignored, while imported source provenance/tests are shareable. See [lesson maintenance](harness/LESSON_UPDATES.md).

Official product references (checked 2026-10-08): [repo-scoped skills](https://learn.chatgpt.com/docs/build-skills), [Windows app](https://learn.chatgpt.com/docs/windows/windows-app), [browser](https://learn.chatgpt.com/docs/browser), [computer use](https://learn.chatgpt.com/docs/computer-use), [UiPath package management](https://docs.uipath.com/studio/standalone/latest/user-guide/managing-activities-packages), [UiPath file URL permissions](https://docs.uipath.com/studio/standalone/latest/user-guide/enable-access-to-file-urls-and-inprivate-mode).
