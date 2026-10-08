# Local portal: prepared input and remaining user actions

Current handoff: [Logged portal draft and exact next action](PORTAL_LOGGED_HANDOFF.md). Real UI activities and evidence logging have now been prepared separately in Portal_Logged_Trial.xaml. Use that handoff; the manual build route below is retained as historical context. Targets are still unconfigured and no portal robot has been run.

Updated 2026-10-07. This is a preparation handoff, not evidence of a portal submission or completion of the day4 assignment.

The installed Studio license and System/Excel/UIAutomation/Presentations packages already passed. The existing project is `BPA_Setup_Smoke/project.json`. Main.xaml and Workbook_Roundtrip.xaml retain their successful tests. Your saved Portal_Brave_Check.xaml contains the attached Brave application and an empty Do body; it still needs field-level targets and processing activities.

## Prepared and actually tested

`BPA_Setup_Smoke/Portal_Input_Preview.xaml` was created/configured through native Studio. Select this tab and use the Run dropdown → Run File to repeat the data-only test. It reads:

- Workbook local path: `"../../readiness_2026-10-06/karbejelentesek_input.xlsx"`
- SheetName: `"bejelentesek"`
- Range: `"A1:F2"` (headers plus one data row)
- Add headers: Yes
- Output DataTable: `dt`

It writes a separate `Portal_Input_Preview.xlsx`, sheet `VerifiedData`, with headers. Observed Run File finished in00:00:07. All headers and populated first-row values match. The blank ugyszam is written as an empty string, equivalent to the source blank cell. Input and all56supplied nap04 source files are unchanged. Evidence: `portal_input_preview_verified.json`.

This preview workflow has no browser activity. It does not submit anything or generate a case number.

## Remaining local Studio work for the user

Correction on2026-10-07: manual indication is one authoring route, not a technical requirement for every field. UiPath selectors are editable text/XML and support HTML attributes such as id. The HTML source can therefore supply candidate selectors offline. Such candidates still need live validation in the user's connected UiPath/browser environment. No complete selector-configured portal workflow has been produced or verified here. See [UiPath selectors](https://docs.uipath.com/activities/other/latest/ui-automation/about-selectors) and [full/partial selectors](https://docs.uipath.com/activities/other/latest/ui-automation/full-versus-partial-selectors).

Providing the HTML file alone does not verify targeting. Studio needs matching browser/form descriptors, and the actual run must be checked. The agent's tool explicitly blocked control of this fileURL and indirect workarounds; the user performs these local browser actions and the portal robot run. The steps below describe the manual-indication route.

1. Keep the copied portal at `C:/Users/nagya/dev/school/BPA/nap04/working/readiness_2026-10-06/gyakorlo_karportal.html`. Use your existing logged-in Brave tab. There is no need to log in again while it remains authenticated.
2. Preserve the tested preview: in Studio, Save As `Portal_Input_Preview.xaml` to a new `UrlapRobot.xaml` in this same project. In that new copy, remove its Write Range Workbook activity. Keep the configured Read Range Workbook and the sequence-scoped `dt` variable. Do not change Main.xaml or the tested preview.
3. After Read Range, add Use Application/Browser and manually indicate the existing authenticated portal tab. Within its Do, add For Each Row in Data Table, DataTable `dt`, row variable `CurrentRow`. All form actions below belong inside this loop body. Reuse the same tab for each row.
4. Add the four Type Into activities and one Select Item activity below, manually indicating each field. Each indication must select the individual field, not the whole browser. Set clear/empty field before typing for every Type Into. If only the browser window can be selected, stop: browser extension/native-host communication is not yet verified.

| Field | Activity | VB expression | HTML ID for checking the selected target |
| --- | --- | --- | --- |
| Kötvényszám | Type Into | `CurrentRow("kotvenyszam").ToString()` | `kotvenyszam` |
| Kártípus | Select Item | `CurrentRow("kartipus").ToString()` | `kartipus` |
| Káresemény dátuma | Type Into | `CurrentRow("karesemeny_datum").ToString()` | `karesemeny-datum` |
| Becsült összeg | Type Into | `CurrentRow("becsult_osszeg").ToString()` | `becsult-osszeg` |
| A kár rövid leírása | Type Into | `CurrentRow("karleiras").ToString()` | `karleiras` |

5. After filling the fields, add Click and manually select **Bejelentés rögzítése**. Add Check App State for **A bejelentést rögzítettük**, with approximately10seconds timeout. In Target appears, add Click for **Új bejelentés rögzítése**. In Target does not appear, add Throw with `New Exception("A bejelentés nem mentődött; ellenőrizd a portál hibaüzenetét.")`. The draft button is not used.
6. Save and validate the new workflow. Before running, inspect the current claims list to establish its baseline and check whether the first practice row is already present. If a previous submission is uncertain, inspect the saved list before retrying to avoid duplicate records.
7. Select UrlapRobot.xaml and use Run File yourself. For this setup test, keep `A1:F2`. Verify successful Output, the confirmation and exactly one newly saved record. Match its policy `TR-402318`, type `vízkár`, date `2025-11-03`, amount1850 and description to the actual first input row. Copy text from the workbook rather than retyping it from these notes.
8. Provide the Studio Output and saved-record screenshots for review. No password, token or browser storage is needed. The full ten-row run is a separate course exercise: change Range to `""` only after the one-row test passes and the starting records are reconciled. Do not claim20+10=30 unless the clean20-record baseline was verified. Preserve evidence before any user-performed practice-record cleanup.

Current resume point: user selects a field-level target in Studio. The data preview is verified; browser connection, field selectors, submission and readback remain unverified. The agent must not run this portal workflow indirectly.
