"""Isolated synthetic verifier fixtures, never actual portal run evidence."""
import csv
from pathlib import Path
import shutil
import tempfile
import unittest

from openpyxl import Workbook
from verify_portal_batch import input_rows, verify, SCHEMA

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'readiness_2026-10-06/karbejelentesek_input.xlsx'


def write_csv(path, rows, fields, delimiter):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)


def snapshot(path, rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Input'
    sheet.append(list(rows[0]))
    for row in rows:
        sheet.append(list(row.values()))
    workbook.save(path)
    workbook.close()


class BatchVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='BPA_synthetic_batch_verifier_')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run = self.root / 'synthetic_run'
        self.run.mkdir()
        self.expected = input_rows(SOURCE, 'bejelentesek')
        self.before = [dict(self.expected[0], ugyszam='K-GY-4147'),
                       dict(self.expected[0], ugyszam='K-GY-9990', kotvenyszam='TR-999999')]
        self.after = list(self.before)
        self.fields = list(self.before[0])
        self.baseline = self.root / 'synthetic_baseline.csv'
        self.export = self.root / 'synthetic_post.csv'
        snapshot(self.run / 'input_snapshot.xlsx', self.expected)
        write_csv(self.run / 'events.csv', [{'event': name} for name in
                  ['run_started', 'input_read', 'batch_finished_pending_readback']], ['event'], ',')
        for index, row in enumerate(self.expected[1:]):
            policy = row['kotvenyszam']
            case_id = f'K-GY-{10000 + index}'
            self.after.append(dict(row, ugyszam=case_id))
            folder = self.run / policy
            folder.mkdir()
            snapshot(folder / 'input_snapshot.xlsx', [row])
            (folder / 'case_id.txt').write_text(case_id, encoding='utf-8')
            for image in ['01_before.png', '02_filled.png', '03_confirmation.png']:
                # Signature/size fixture only; never valid visual execution evidence.
                (folder / image).write_bytes(b'\x89PNG\r\n\x1a\n' + b'SYNTHETIC_FIXTURE' * 100)
            names = ['run_started', 'input_read', 'policy_reserved']
            events = [{'event': name, 'policy': policy, 'case_id': '', 'detail': ''} for name in names]
            events.extend({'event': 'field_activity_completed', 'policy': policy, 'case_id': '', 'detail': field}
                          for field in ['kotvenyszam', 'kartipus', 'karesemeny_datum', 'becsult_osszeg', 'karleiras'])
            events.extend({'event': name, 'policy': policy, 'case_id': case_id, 'detail': ''}
                          for name in ['submit_attempted', 'confirmation_seen', 'case_id_read',
                                       'ui_sequence_complete', 'run_finished_pending_readback'])
            write_csv(folder / 'events.csv', events, ['event', 'policy', 'case_id', 'detail'], ',')
        self.save_exports()

    def save_exports(self):
        write_csv(self.baseline, self.before, self.fields, ';')
        write_csv(self.export, self.after, self.fields, ';')

    def verify(self, before_total=22, after_total=31):
        return verify(self.run, self.baseline, self.export, SOURCE, before_total, after_total)

    def test_complete_fixture_is_only_automated_pending_visual(self):
        report = self.verify()
        self.assertEqual(report['status'], 'automated_checks_passed_visual_review_pending')
        self.assertEqual(report['new_cases'], 9)
        self.assertTrue(report['screenshots_require_visual_review'])
        self.assertTrue(all(check['passed'] for check in report['checks']))

    def test_missing_row_folder_fails(self):
        shutil.rmtree(self.run / self.expected[-1]['kotvenyszam'])
        with self.assertRaisesRegex(ValueError, 'nine expected'):
            self.verify()

    def test_duplicate_case_id_fails(self):
        self.after.append(dict(self.after[-1]))
        self.save_exports()
        with self.assertRaisesRegex(ValueError, 'unique case IDs'):
            self.verify()

    def test_changed_prior_record_fails(self):
        self.after[1] = dict(self.after[1], karleiras='Changed synthetic prior record')
        self.save_exports()
        with self.assertRaisesRegex(ValueError, 'earlier own records'):
            self.verify()

    def test_incomplete_submission_log_fails(self):
        log = self.run / self.expected[1]['kotvenyszam'] / 'events.csv'
        log.write_text(log.read_text(encoding='utf-8-sig').replace('confirmation_seen', 'missing_fixture'), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'required checkpoints'):
            self.verify()

    def test_wrong_input_snapshot_fails(self):
        row = dict(self.expected[1], karleiras='Wrong synthetic snapshot')
        snapshot(self.run / row['kotvenyszam'] / 'input_snapshot.xlsx', [row])
        with self.assertRaises(ValueError):
            self.verify()

    def test_empty_case_id_serializations_agree(self):
        rows = [dict(row, ugyszam='') for row in self.expected]
        snapshot(self.run / 'input_snapshot.xlsx', rows)
        for row in rows[1:]:
            snapshot(self.run / row['kotvenyszam'] / 'input_snapshot.xlsx', [row])
        self.assertEqual(self.verify()['new_cases'], 9)

    def test_nonempty_case_id_snapshot_still_fails(self):
        rows = [dict(row) for row in self.expected]
        rows[1]['ugyszam'] = 'Unexpected'
        snapshot(self.run / 'input_snapshot.xlsx', rows)
        with self.assertRaisesRegex(ValueError, 'full source snapshot'):
            self.verify()

    def test_unreconciled_pending_baseline_fails(self):
        self.before.append(dict(self.after[2]))
        self.save_exports()
        with self.assertRaisesRegex(ValueError, 'no pending input policies'):
            self.verify()

    def test_total_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError, 'totals increase'):
            self.verify(after_total=30)

    def test_wrong_saved_value_fails(self):
        self.after[-1] = dict(self.after[-1], becsult_osszeg=999)
        self.save_exports()
        with self.assertRaisesRegex(ValueError, 'estimated amount'):
            self.verify()


if __name__ == '__main__':
    unittest.main()
