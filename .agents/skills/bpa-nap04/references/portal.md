# Claims form robot — block6

Read `nap04/nap04/pages/06_urlap_robot.html`, `docs/gyakorlo_karportal.html` and `docs/karbejelentesek_input.xlsx`. Copy assets into outer `working/` before any edits; keep portal at a stable absolute path. This is a local fictional practice page, never a real insurer or production endpoint.

## Browser prerequisite

Follow the live-operation boundary in [AGENTS.md](../../../../AGENTS.md) and the fresh-baseline/trial/batch procedure in [harness/WORKFLOWS.md](../../../../harness/WORKFLOWS.md#portal-fresh-baseline-then-trial-then-batch). User-provided target captures and exported evidence support offline authoring/verification. Browser opening alone does not establish captured targets.

Portal teaching login is public dummy `gyakorlo`/`Meridian2026`, not the user's account. It starts with20sample cases and persists added practice cases in browser local storage. Counts and target evidence must come from the user's actual run.

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

The user performs live Studio indication and robot runs. Verify the resulting one-row trial and batch using the shared procedure above; these task-specific activity settings do not authorize agent launch.

## Acceptance

At clean baseline list has20samples+10own=30, IDs startK-GY. Check first **and last** spreadsheet policy, amount, type plus total added10; inspect all rows if mismatches. Export own practice cases CSV when available and preserve credential-free evidence. Keep runnable project and input copies, selector notes, run start/end/result and artifact index. Writing ugyszam back to Excel is optional later expansion, not today's required output. No email, real insurance operation, publishing or graded submission is part of this exercise.
