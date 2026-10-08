# ExcelRobot

Open project.json in Studio; Windows/VB, System26.8.2 and Excel3.6.1.

Main.xaml:12customers,100000threshold. Executed output is output/ugyfelek_minositve.xlsx. [Verification](verification_100000.json), [actual run](../../working/excel_100000_run.json), [observed completion](../../working/excel_100000_dialog.jpg). Source and first3columns preserved.

The output guard prevents accidental overwrites. To rerun, preserve the existing result and choose a fresh destination or archive the output first.

Classify_150000.xaml: separate150000variant, actual UiPath run17seconds,12rows/3kiemelt verified. [Verification](verification_150000.json), [actual run](../../working/excel_150000_run.json), [completion](../../working/excel_150000_dialog.jpg). Both outputs preserved.
