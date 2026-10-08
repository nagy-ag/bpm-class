"""Read saved user-run batch evidence only. Never controls browser or UiPath."""
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re

from openpyxl import load_workbook
from verify_portal_run import read_csv, verify as verify_row

SCHEMA = {'ugyszam', 'kotvenyszam', 'kartipus', 'karesemeny_datum', 'becsult_osszeg', 'karleiras'}
FIRST_POLICY = 'TR-402318'
FIRST_CASE = 'K-GY-4147'


def input_rows(path, sheet):
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        values = list(workbook[sheet].values)
    finally:
        workbook.close()
    rows = [dict(zip(values[0], row)) for row in values[1:]]
    # UiPath writes an empty DataTable case-ID cell as ""; openpyxl reads
    # the supplied empty cell as None. Normalize only this unused column.
    for row in rows:
        if row.get('ugyszam') == '':
            row['ugyszam'] = None
    return rows


def agrees(actual, expected):
    return (all(actual[key] == str(expected[key]) for key in
                ('kotvenyszam', 'kartipus', 'karesemeny_datum', 'karleiras'))
            and Decimal(actual['becsult_osszeg']) == Decimal(str(expected['becsult_osszeg'])))


def verify(folder, baseline, export, source, before_total, after_total):
    checks = []

    def check(name, condition):
        checks.append({'check': name, 'passed': bool(condition)})
        if not condition:
            raise ValueError(name)

    expected = input_rows(source, 'bejelentesek')
    check('Ten unique source policies', len(expected) == 10 and len({row['kotvenyszam'] for row in expected}) == 10)
    check('All original case-ID cells remain empty', all(not row['ugyszam'] for row in expected))
    check('First source policy is the previously verified trial', expected[0]['kotvenyszam'] == FIRST_POLICY)
    before = read_csv(baseline, delimiter=';')
    after = read_csv(export, delimiter=';')
    for label, rows in [('Baseline', before), ('Post-run export', after)]:
        check(label + ' schema and unique case IDs', bool(rows) and all(set(row) == SCHEMA for row in rows)
              and len({row['ugyszam'] for row in rows}) == len(rows)
              and all(re.fullmatch(r'K-GY-\d+', row['ugyszam']) for row in rows))
    first = [row for row in before if row['kotvenyszam'] == FIRST_POLICY]
    check('Baseline preserves the exact first case once', len(first) == 1 and first[0]['ugyszam'] == FIRST_CASE and agrees(first[0], expected[0]))
    pending = {row['kotvenyszam']: row for row in expected[1:]}
    check('Baseline contains no pending input policies', not any(row['kotvenyszam'] in pending for row in before))
    check('Current full source snapshot agrees with supplied ten rows', input_rows(folder / 'input_snapshot.xlsx', 'Input') == expected)
    events = read_csv(folder / 'events.csv')
    names = [event['event'] for event in events]
    check('Parent checkpoint sequence complete without failure',
          all(names.count(name) == 1 for name in ('run_started', 'input_read', 'batch_finished_pending_readback'))
          and names.index('run_started') < names.index('input_read') < names.index('batch_finished_pending_readback')
          and 'stopped_requires_review' not in names)
    check('Exactly nine expected row evidence directories',
          {path.name for path in folder.iterdir() if path.is_dir()} == set(pending))
    row_reports = []
    for policy, row in pending.items():
        item = verify_row(folder / policy, export)
        check('Row evidence is for expected policy ' + policy, item['policy'] == policy)
        snapshot = input_rows(folder / policy / 'input_snapshot.xlsx', 'Input')
        check('Row snapshot exactly matches source ' + policy, snapshot == [row])
        row_reports.append(item)
    before_by_id = {row['ugyszam']: row for row in before}
    after_by_id = {row['ugyszam']: row for row in after}
    check('All earlier own records preserved byte-for-field',
          all(after_by_id.get(key) == row for key, row in before_by_id.items()))
    new_ids = set(after_by_id) - set(before_by_id)
    check('Exactly nine new saved cases agree with row evidence', len(new_ids) == 9
          and new_ids == {row['case_id'] for row in row_reports})
    for row in expected:
        matches = [actual for actual in after if actual['kotvenyszam'] == row['kotvenyszam']]
        check('One exact saved record for ' + row['kotvenyszam'], len(matches) == 1 and agrees(matches[0], row))
    check('Own-record count increases by nine', len(after) == len(before) + 9)
    check('User-reported page totals increase by nine',
          type(before_total) is int and type(after_total) is int and before_total >= len(before)
          and after_total >= len(after) and after_total == before_total + 9)
    check('User-reported seed count stays20', before_total - len(before) == 20 and after_total - len(after) == 20)
    return {'status': 'automated_checks_passed_visual_review_pending',
            'scope': 'Cumulative user-operated batch; preserves existing fixtures, not a clean20+10 run',
            'previously_verified': {'policy': FIRST_POLICY, 'case_id': FIRST_CASE},
            'new_cases': len(new_ids), 'matching_input_cases': 10,
            'own_count_before': len(before), 'own_count_after': len(after),
            'page_total_before_user_reported': before_total, 'page_total_after_user_reported': after_total,
            'baseline_sha256': hashlib.sha256(baseline.read_bytes()).hexdigest(),
            'export_sha256': hashlib.sha256(export.read_bytes()).hexdigest(),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'checks': checks, 'per_row': row_reports,
            'screenshots_require_visual_review': True,
            'completion_requires': 'Review all per-row screenshots and exact user execution/total observations before marking coursework complete.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_folder', type=Path)
    parser.add_argument('baseline_csv', type=Path)
    parser.add_argument('export_csv', type=Path)
    parser.add_argument('source_xlsx', type=Path)
    parser.add_argument('--before-total', type=int, required=True)
    parser.add_argument('--after-total', type=int, required=True)
    args = parser.parse_args()
    try:
        report = verify(args.run_folder, args.baseline_csv, args.export_csv, args.source_xlsx,
                        args.before_total, args.after_total)
    except Exception as error:
        print(json.dumps({'status': 'incomplete_or_failed', 'reason': str(error),
                         'action': 'Inspect saved records before any retry; no browser action performed.'}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    (args.run_folder / 'batch_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
