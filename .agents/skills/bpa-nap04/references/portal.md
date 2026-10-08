# Claims form robot — block6

Read `nap04/nap04/pages/06_urlap_robot.html`, `docs/gyakorlo_karportal.html` and `docs/karbejelentesek_input.xlsx`. Copy assets into outer `working/` before any edits; keep portal at a stable absolute path. This is a local fictional practice page, never a real insurer or production endpoint.

## Browser prerequisite

Prefer in-app browser when allowed; its fileURL block cannot be bypassed with a server/alternative automation route. The lesson's required UiPath Edge/Chrome local-page workflow needs a policy-permitted user handoff. Explain the actual blocked step and let the user open the practice copy. Browser extension installation and fileURL access must follow active tool permissions; Windows Computer Use cannot change security/privacy permission settings. User configures the UiPath extension and Allow access to fileURLs, then agent verifies the app can identify elements. Do not label this prerequisite complete merely because a browser opens.

Portal teaching login is public dummy `gyakorlo`/`Meridian2026`; it is not the user's account. Active Computer Use denies authentication-dialog automation, so let the user log in where required. No real password is stored. It starts with20sample cases and persists added practice cases in browser local storage. No cookie/storage extraction or injection to fake robot completion.

## Establish correct initial state

Manual UI practice: enter first spreadsheet row, submit, observe confirmation and press Új bejelentés rögzítése. The lesson calls for resetting added **practice** records before the10-row robot run. Verify scope and preserve needed evidence first; user performs any reset that active UI confirmation rules require. Do not wipe unrelated records. If baseline cannot be reset, record starting counts and identify only this run's rows; don't claim20+10=30 without that initial state.

Input sheet `bejelentesek`, columns `kotvenyszam`, `kartipus`, `karesemeny_datum`, `becsult_osszeg`, `karleiras`, `ugyszam`;10rows. Dates alreadyYYYY-MM-DDtext, amounts integer, ugyszam empty for future readback expansion. Validate headers/count before UI operations.

## Actual Studio workflow

Windows+Visual Basic Process `UrlapRobot`, Read Range Workbook headersOn/full range→adatok DataTable. First trial range `A1:F2`; verify1data row. Main run full `""`; verify10.

Use Application/Browser attached to the already authenticated practice tab. Put For Each Row adatok/CurrentRow **inside Do**, all fill/submit/wait/reset activities inside its Body. Reuse one browser, not one new window per row.

| Field | Activity | Expression | Source element ID |
| --- | --- | --- | --- |
| Policy | Type Into | CurrentRow("kotvenyszam").ToString() | kotvenyszam |
| Claim type | Select Item | CurrentRow("kartipus").ToString() | kartipus |
| Date | Type Into | CurrentRow("karesemeny_datum").ToString() | karesemeny-datum |
| Amount | Type Into | CurrentRow("becsult_osszeg").ToString() | becsult-osszeg |
| Description | Type Into | CurrentRow("karleiras").ToString() | Inspect current HTML/target |

Indicate each target separately and verify current selectors. Four Type Into activities clear fields before typing; Select Item string exactly matches an option. Click Bejelentés rögzítése; Check App State `A bejelentést rögzítettük`, timeout about10seconds. Appears→Click Új bejelentés rögzítése; absent→Throw `New Exception("A bejelentés nem mentődött; ellenőrizd a portál hibaüzenetét.")`. Fail visibly rather than skip a row. Don't use Piszkozat mentése (deliberately changingid).

Observe1rowrun, inspect all fields, reset own trial if permitted, restore full range and run10. Capture actual robot Output and UI evidence. If interrupted after submission, inspect saved rows before resuming; restarting blindly creates duplicates. Any code-only/mock browser fill is not an actual UiPath run.

## Acceptance

At clean baseline list has20samples+10own=30, IDs startK-GY. Check first **and last** spreadsheet policy, amount, type plus total added10; inspect all rows if mismatches. Export own practice cases CSV when available and preserve credential-free evidence. Keep runnable project and input copies, selector notes, run start/end/result and artifact index. Writing ugyszam back to Excel is optional later expansion, not today's required output. No email, real insurance operation, publishing or graded submission is part of this exercise.
