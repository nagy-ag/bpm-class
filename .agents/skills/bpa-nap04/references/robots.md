# Desktop robot runbooks

Source prefix `nap04/nap04/`. Read each page before execution. Create actual Process projects under outer `working/`; Windows compatibility, VB.NET expressions. Packages: Excel→UiPath.Excel.Activities, browser→UiPath.UIAutomation.Activities, PPT→UiPath.Presentations.Activities; choose stable compatible versions, not guessed latest pins.

## 1 — pages/01_studio_terkep.html

`Nap04_gyakorlas`, Message Box `"Működik!"`, Run/Ctrl+F5 (F5 Debug). Observe dialog and successful Output completion. Identify canvas, Explorer/project files, Properties, Output/Errors; use current panel controls to restore hidden panels. Literal strings need quotes; variable expressions don't. Compile errors/package wait are not successful runs.

## 2 — pages/02_elso_robot.html

Same project: Input Dialog title Bemutatkozás, label Hogy hívnak?, output `nev` String scope Main; Message Box `"Szia, " & nev & "! Ez az első robotod."`. Second dialog Számoljunk/Hány e-mailt írsz naponta?, `darab` String. Initial output `"Évente kb. " & (CInt(darab)*250).ToString() & " e-mail."`; 20→5000. The250days are a lesson assumption. Demonstrate failure on `sok`, then preserve repaired version.

Repair with `napiDarab` Int32; If `Integer.TryParse(darab, napiDarab) AndAlso napiDarab >= 0 AndAlso napiDarab <= 1000000`. Then output `(napiDarab*250).ToString()`, Else `"0 és 1 000 000 közötti egész számot adj meg."`. Remove old unconditional CInt box. Run5→1250; `sok`, -1, blank→friendly message, no conversion exception. Test upper boundary if changing validation; multiplication stays withinInt32 here. Keep sample interactions fictional, not personal workload facts.

## 3 — pages/03_excel_robot.html

Copy `docs/ugyfelek.xlsx`: sheet Ugyfelek, columns Nev/Varos/EvesDij/Minosites,12data rows. `ExcelRobot`: Read Range Workbook full range `""`, headersOn→dt System.Data.DataTable. Check12, then remove temporary diagnostic box. For Each Row in Data Table dt, row CurrentRow, **inside Body** Assign:

```vb
CurrentRow("Minosites") = If(CDbl(CurrentRow("EvesDij")) >= 100000, "kiemelt", "normál")
```

Write Range Workbook after loop to new `ugyfelek_minositve.xlsx`, Ugyfelek, A1, dt, headersOn; folder exists and file closed. Workbook activities need no Excel app. Verify12data+header,6kiemelt/6normál, other values preserved, original unchanged.

Mini: new output `ugyfelek_minositve_v2.xlsx`, threshold150000; verify3kiemelt annual amounts152000,231000,187300 and12rows. Preserve both outputs. A helper may independently inspect results, but actual robot run is required.

## 4 — pages/04_excel_ppt.html

Desktop Excel+PowerPoint required. Copy Raw_data.xlsx→Riport_adatok.xlsx and Dickinson_Sample_Slides.pptx→Riport_eredmeny.pptx. Data sheet us-500, A1:D244=243records, columns State/Quantity/UnitPrice/Total. Deck9slides. Use the available Add Chart To PowerPoint Presentation From Excel template **or** equivalent described native workflow; no need to do both.

Template-free `RiportRobot`: Use Excel File reference Excel; Insert Chart column chart with headers, data A1:B13=first12records (not grouped State totals), target sheet us-500, Save for Later Use `diagram`. Get Excel Chart diagram, Copy to clipboard. Still inside Excel scope: Use PowerPoint Presentation reference PowerPoint; Paste Item Into Slide9, select large **content** placeholder, not title. Set slide9 Layout Title and Content in working deck first; title `Az első 12 rekord mennyisége`. Don't disturb clipboard between copy/paste.

Run, require no Output error and12bars in Excel/slide9, save/open both results. Mini with fresh copies and A1:B7=first6records, verify6bars. Dataset isn't quarterly; don't manufacture quarterly comparison. Close Office files before run. Simple paste/insert can add charts repeatedly: fresh copies for retries, keep12/6versions separately. Verify saved chart and visible presentation, not just a zip member count.

## 5 — pages/05_fajlrendezo.html

Extract `docs/gyakorlo_mappa.zip` into an isolated working exercise directory;20files. Never point at real Downloads/Desktop. `Fajlrendezo`: Create Folder PDF/Excel/Word **before** For Each File in Folder; top-only (Include subfoldersOff), all files, CurrentFile. Three If bodies test `.Extension.ToLower()` for.pdf/.xlsx/.docx, Move File CurrentFile.FullName to `Path.Combine(exerciseRoot, category, CurrentFile.Name)`. Include full original filename; move, not copy.

Run: PDF6,Excel4,Word5; rootPNG3/TXT2; total20. Mini createKepek and.png rule→3images, only2TXTroot. Run again→no moves. Verify filenames/content hashes across movement, counts and successful robot logs; lower-case comparison catches uppercase extension. Collision: preserve existing result, use a fresh separately named extraction; don't merge archives or overwrite unknown destination files. Any recursive cleanup/move must resolve and remain within that exercise workspace.

## 7 — pages/07_zaras.html

Save reasoned choices for five scenarios: quote→API plus scheduled script/robot; API-less300HRrecords→consider export first, thenRPA; large credit approval→human with prepared data; webshop→courier API if supported;40PDFinvoice totals→document processing with checks, OCR/AI only when scan/extraction needs it. No real HR/credit/invoice data required. Explain access, structure, error handling and human responsibility.

Day5/6 previews are not full assignment specs. Fetch published requirements when requested; no inferred deadlines, grades or submissions. Home video playlists are resources, not evidence the user watched.

## Project handoff

Each robot: clean runnable project, input/output paths or arguments, dependency versions, observed successful runs and test cases, output links. Include interactive repaired robot, both classified workbooks,12/6chart reports, sorter final directory/counts, portal project/evidence from companion reference, and decision notes. Keep original sources and partial drafts; blocked platform steps remain pending.
