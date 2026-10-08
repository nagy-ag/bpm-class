# RiportRobot — actual native Office run

The12-record workflow completed in20seconds with no execution errors. The saved Excel workbook and slide9both show12columns; native reopened screenshots and21independent data/OOXML checks confirm exact source quantities/categories, unchanged243source rows and original slide1–8paragraph text.

Open project.json in Windows/VB Studio. Packages: System26.8.2, Excel3.6.1, Presentations2.6.1. Main.xaml uses native Insert Chart → Copy Chart to Clipboard → PowerPoint Paste Into Slide, targeting the observed Content Placeholder2on slide9. The title is Az első12rekord mennyisége (with normal spaces in the actual file).

Actual outputs and verification are in reports_12; run/validation logs and reopened native screenshots are here. Original sources are untouched. The run_started.lock deliberately prevents repeating a completed copy and duplicating charts. For a new run, prepare a separate fresh working folder from the original assets and configure the native slide layout/title/content placeholder first. Do not delete the marker to retry an uncertain run.

The separate six-record mini completed in14seconds without errors. [reports_6](reports_6) passed21independent checks; native reopened Excel and PowerPoint both visibly show six bars. Excel also exposes the exact categories/quantities LA33, MI87, NJ58, AK82, OH38, OH54. The workbook was inspected in Protected View without changing its security state. Report_6.xaml, actual run/validation logs and both reopened screenshots are included. Main.xaml remains the twelve-record workflow; select Report_6.xaml for the mini. Both completed copies retain their run_started.lock markers: do not rerun them. This package is not a graded submission.
