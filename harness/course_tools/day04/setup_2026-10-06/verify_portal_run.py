"""Verify saved user-run evidence offline. Does not control a browser or UiPath."""
import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

from openpyxl import load_workbook


def read_csv(path, delimiter=","):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream, delimiter=delimiter))


def verify(folder, export):
    checks = []

    def check(name, condition):
        checks.append({"check": name, "passed": bool(condition)})
        if not condition:
            raise ValueError(name)

    check("Evidence directory exists", folder.is_dir())
    events = read_csv(folder / "events.csv")
    check("No logged failure or uncertainty", not any(row["event"] == "stopped_requires_review" for row in events))
    required = ["run_started", "input_read", "policy_reserved", "submit_attempted", "confirmation_seen", "case_id_read", "ui_sequence_complete", "run_finished_pending_readback"]
    names = [row["event"] for row in events]
    positions = [names.index(name) if names.count(name) == 1 else -1 for name in required]
    check("All required checkpoints occurred once and in order", -1 not in positions and positions == sorted(positions))
    fields = [row["detail"] for row in events if row["event"] == "field_activity_completed"]
    check("Five field activities occurred in expected order", fields == ["kotvenyszam", "kartipus", "karesemeny_datum", "becsult_osszeg", "karleiras"])
    book = load_workbook(folder / "input_snapshot.xlsx", read_only=True, data_only=True)
    rows = list(book["Input"].values)
    book.close()
    check("Actual input snapshot contains one row", len(rows) == 2)
    expected = dict(zip(rows[0], rows[1]))
    case_id = (folder / "case_id.txt").read_text(encoding="utf-8-sig").strip()
    check("Actual case ID has expected format", re.fullmatch(r"K-GY-\d+", case_id))
    check("Case-ID event agrees with saved file", next(row["case_id"] for row in events if row["event"] == "case_id_read") == case_id)
    check("Submission event identifies the actual input policy", next(row["policy"] for row in events if row["event"] == "submit_attempted") == str(expected["kotvenyszam"]))
    for name in ("01_before.png", "02_filled.png", "03_confirmation.png"):
        screenshot = folder / name
        check("PNG evidence exists: " + name, screenshot.is_file() and screenshot.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n" and screenshot.stat().st_size > 1000)
    saved_rows = read_csv(export, delimiter=";")
    check("Export has expected schema", bool(saved_rows) and set(saved_rows[0]) == {"ugyszam", "kotvenyszam", "kartipus", "karesemeny_datum", "becsult_osszeg", "karleiras"})
    matching = [row for row in saved_rows if row["ugyszam"] == case_id]
    check("Export contains exactly one row for this case ID", len(matching) == 1)
    actual = matching[0]
    for column in ("kotvenyszam", "kartipus", "karesemeny_datum", "karleiras"):
        check("Saved value agrees: " + column, actual[column] == str(expected[column]))
    check("Saved estimated amount agrees", Decimal(actual["becsult_osszeg"]) == Decimal(str(expected["becsult_osszeg"])))
    check("Policy occurs once in own-record export", sum(row["kotvenyszam"] == actual["kotvenyszam"] for row in saved_rows) == 1)
    return {"status": "passed", "scope": "one-row user-operated UiPath trial; not ten-row coursework", "case_id": case_id, "policy": actual["kotvenyszam"], "export_sha256": hashlib.sha256(export.read_bytes()).hexdigest(), "checks": checks, "screenshots_require_visual_review": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_folder", type=Path)
    parser.add_argument("export_csv", type=Path)
    args = parser.parse_args()
    try:
        report = verify(args.run_folder, args.export_csv)
    except Exception as error:
        print(json.dumps({"status": "incomplete_or_failed", "reason": str(error), "action": "Inspect saved records before any retry; no browser action was performed."}, ensure_ascii=False, indent=2))
        sys.exit(2)
    (args.run_folder / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
