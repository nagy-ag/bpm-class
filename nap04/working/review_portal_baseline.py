"""Preserve and review the user-exported CSV offline; no browser interaction."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
SETUP = ROOT / 'nap04/working/setup_2026-10-06'
sys.path.insert(0, str(SETUP))
from verify_portal_run import read_csv, verify
from verify_portal_batch import input_rows, agrees, SCHEMA

source = Path.home() / 'Downloads/sajat_karbejelentesek (3).csv'
folder = SETUP / 'portal_baselines/pre_batch_export3_20261007'
folder.mkdir(exist_ok=True)
saved = folder / source.name
if saved.exists():
    assert saved.read_bytes() == source.read_bytes(), 'Preserved baseline differs; stop'
else:
    shutil.copy2(source, saved)
assert saved.read_bytes() == source.read_bytes()
rows = read_csv(saved, delimiter=';')
prior = read_csv(Path.home() / 'Downloads/sajat_karbejelentesek (2).csv', delimiter=';')
expected = input_rows(ROOT / 'nap04/working/readiness_2026-10-06/karbejelentesek_input.xlsx', 'bejelentesek')
assert len(rows) == 4 and rows == prior
assert all(set(row) == SCHEMA for row in rows)
assert len({r['ugyszam'] for r in rows}) == 4
assert len({r['kotvenyszam'] for r in rows}) == 4
first = [r for r in rows if r['kotvenyszam'] == expected[0]['kotvenyszam']]
assert len(first) == 1 and first[0]['ugyszam'] == 'K-GY-4147' and agrees(first[0], expected[0])
pending = {r['kotvenyszam'] for r in expected[1:]}
assert len(expected) == 10 and len(pending) == 9
assert not any(r['kotvenyszam'] in pending for r in rows)
locks = sorted(p.name for p in (SETUP / 'portal_runs/reservations').glob('*.lock'))
assert locks == ['TR-402318.lock'], 'Uncertain additional reservation; stop'
trial = SETUP / 'portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202'
trial_review = verify(trial, saved)
assert all(c['passed'] for c in trial_review['checks'])
manual = json.loads((SETUP / 'portal_baselines/pre_robot_20261007_085655/pre_robot_review.json').read_text(encoding='utf-8'))['manual_fixture']
assert rows[2] == manual
report = {
    'status': 'offline_baseline_passed',
    'source': str(source), 'preserved_csv': str(saved),
    'sha256': hashlib.sha256(saved.read_bytes()).hexdigest(),
    'source_modified_epoch': source.stat().st_mtime,
    'page_total_user_reported': 24, 'own_count': 4,
    'seed_count_inferred_from_user_total_minus_export': 20,
    'same_fields_as_export2': True, 'all_prior_records_unchanged': True,
    'first_input_verified_once': True, 'first_input_case': 'K-GY-4147',
    'pending_policies_absent': sorted(pending), 'reservation_files': locks,
    'manual_fixture': manual, 'first_trial_recheck': trial_review,
    'expected_after_remaining9': {'page_total': 33, 'own_count': 13, 'matching_lesson_inputs': 10},
    'limitations': ['Page total24 is user-reported, not agent live readback.',
                   'Cumulative preserved-fixture route differs from clean20+10=30 source exercise.',
                   'Manual setup fixture TR-900007 differs from first supplied policy; no reset performed.'],
    'no_live_portal_action': True
}
(folder / 'baseline_review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Baseline passed:4own,24user-reported total,9pending absent; first trial19checks pass; all earlier records preserved.')
