"""Check actual logger-only evidence and offline draft structure, without UI access."""
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

base = Path(__file__).resolve().parent
project = base / "BPA_Setup_Smoke"
folders = list((base / "portal_runs").glob("logger_smoke_*"))
assert len(folders) == 1
folder = folders[0]
with (folder / "events.csv").open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
assert [row["event"] for row in rows] == ["logger_smoke_started", "logger_smoke_escaped", "logger_smoke_complete"]
assert rows[1]["detail"] == 'Comma, quote " Hungarian: vízkár'
assert all(row["policy"] == "LOGGER-SMOKE" and row["case_id"] == "NOT-A-PORTAL-CASE" for row in rows)
assert (folder / "last_event.txt").read_text(encoding="utf-8").strip().endswith('"Expected exactly three events"')
namespaces = {"a": "http://schemas.microsoft.com/netfx/2009/xaml/activities", "uix": "http://schemas.uipath.com/workflow/activities/uix"}
root = ET.parse(project / "Portal_Logged_Trial.xaml").getroot()
todos = [node.attrib["DisplayName"] for node in root.iter() if node.attrib.get("DisplayName", "").startswith("TODO Indicate")]
assert len(todos) == 9
assert root.find('.//a:Variable[@Name="targetsConfigured"]', namespaces).attrib["Default"] == "False"
assert root.find(".//uix:NApplicationCard", namespaces).attrib["OpenMode"] == "Never"
assert len(root.findall(".//uix:NTypeInto", namespaces)) == 4
assert len(root.findall(".//uix:NSelectItem", namespaces)) == 1
assert len(root.findall(".//uix:NClick", namespaces)) == 2
assert len(root.findall(".//uix:NGetText", namespaces)) == 1
expected = {
    "Main.xaml": "fb1527c4f78a1c6bdd15b83d0c342880d9970ca9afd5719718c7397a83f13786",
    "Workbook_Roundtrip.xaml": "7f874c02290212d2004bcd40e71403f5777fcefecac11131e9917aad6269fd64",
}
for name, digest in expected.items():
    assert hashlib.sha256((project / name).read_bytes()).hexdigest() == digest
input_path = base.parent / "readiness_2026-10-06/karbejelentesek_input.xlsx"
assert hashlib.sha256(input_path.read_bytes()).hexdigest() == "76aa238dd5d3fbf481d1d7a1f59005834adf3e404e1cfc275f2ede58222473b2"
report = {
    "date": "2026-10-07",
    "logger_actual_execution": "Session ended; errors=[]; Completed; 00:00:07",
    "logger_csv_rows": len(rows),
    "csv_quote_and_Hungarian_roundtrip": True,
    "logger_evidence_folder": str(folder),
    "draft_real_UIA_activities": True,
    "TODO_controls": todos,
    "premature_run_guard_enabled": True,
    "stub_build": "Blocked only by five expected missing-target errors; not runnable",
    "portal_execution": "Not performed",
    "existing_verified_files_and_input_unchanged": True,
}
(base / "portal_logging_preparation_verified.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
