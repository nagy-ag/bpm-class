# Nap04_gyakorlas

Open project.json in installed UiPath Studio (Windows, Visual Basic; System26.8.2). Main.xaml → Run File, then OK. Actual lesson execution verified2026-10-07 in39seconds. See ../../working/nap04_main_run.json and nap04_main_dialog.jpg.

Greeting_Initial.xaml is intentionally unvalidated:20→5000, sok throws. Greeting_Repaired.xaml is the final interactive version; Calculation_Validated.xaml is its shared calculation. Validation_Regression.xaml runs8 assertions against that same workflow without dialogs. All final workflows actually executed successfully. The explicit Assign after TryParse addresses observed ByRef value persistence in this engine.
