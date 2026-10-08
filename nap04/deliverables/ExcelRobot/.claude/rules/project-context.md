# Project context

Windows/VB ExcelRobot; System26.8.2/Excel3.6.1. Main.xaml classifies12rows of input/ugyfelek.xlsx using100000 threshold and writes output/ugyfelek_minositve.xlsx. Actual desktop execution2026-10-07 passed in34seconds; output independently verified6kiemelt/6normal, unchanged first3columns/input. Existing-output guard deliberately refuses rerun; archive result or choose a fresh output before rerun. No browser activities.

Classify_150000.xaml writes separatev2result; actual headless UiPath Windows run17seconds passed,3kiemelt verified. Desktop designer stalled loading variant; closing that owned instance and using official default headless backend recovered.
