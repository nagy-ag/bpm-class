"""Enable only the reviewed baseline guard; never executes the portal workflow."""
from pathlib import Path
from lxml import etree as E
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
SETUP = ROOT / 'nap04/working/setup_2026-10-06'
baseline_path = SETUP / 'portal_baselines/pre_batch_export3_20261007/baseline_review.json'
baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
assert baseline['status'] == 'offline_baseline_passed'
assert hashlib.sha256(Path(baseline['preserved_csv']).read_bytes()).hexdigest() == baseline['sha256']
assert sorted(p.name for p in (SETUP / 'portal_runs/reservations').glob('*.lock')) == ['TR-402318.lock']
prep = json.loads((SETUP / 'portal_batch_preparation.json').read_text(encoding='utf-8'))
project = SETUP / 'BPA_Setup_Smoke'
trial = project / 'Portal_Logged_Trial.xaml'
assert hashlib.sha256(trial.read_bytes()).hexdigest() == prep['source_trial_sha256']
old = '<Variable Name="batchBaselineReviewed" x:TypeArguments="x:Boolean" Default="False"/>'
new = old.replace('Default="False"', 'Default="True"')
paths = [project / 'Portal_Batch_Resume.xaml', ROOT / 'nap04/deliverables/PortalRobot/setup_2026-10-06/BPA_Setup_Smoke/Portal_Batch_Resume.xaml']
original = paths[0].read_bytes()
assert hashlib.sha256(original).hexdigest() == prep['batch_sha256']
assert paths[1].read_bytes() == original
text = original.decode('utf-8')
assert text.count(old) == 1
enabled = text.replace(old, new).encode('utf-8')
assert enabled.decode('utf-8').replace(new, old).encode('utf-8') == original
def targets(data):
    return [E.tostring(n, method='c14n') for n in E.fromstring(data).iter()
            if E.QName(n).localname in ('TargetAnchorable', 'TargetApp')]
assert targets(original) == targets(enabled)
for path in paths:
    path.write_bytes(enabled)
assert paths[0].read_bytes() == paths[1].read_bytes()
report = {'scope': 'Offline guard enablement only; user must initiate every portal run',
          'baseline': str(baseline_path), 'baseline_sha256': baseline['sha256'],
          'guard_before': False, 'guard_after': True, 'only_guard_changed': True,
          'captured_targets_unchanged': True, 'original_trial_unchanged': True,
          'batch_sha256': hashlib.sha256(enabled).hexdigest(),
          'actual_batch_executed': False, 'expected_after': baseline['expected_after_remaining9']}
(SETUP / 'portal_batch_ready.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Reviewed guard enabled in working/package copies; only guard changed; no workflow execution.')
