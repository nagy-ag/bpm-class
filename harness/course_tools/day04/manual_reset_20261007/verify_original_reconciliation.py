"""Read-only comparison of user CSV(6) with the preserved actual batch CSV(4)."""
from pathlib import Path
import csv
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
fresh = Path('C:/Users/nagya/Downloads/sajat_karbejelentesek (6).csv')
prior = ROOT/'nap04/deliverables/PortalRobot/actual_batch_20261007/sajat_karbejelentesek (4).csv'
def load(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, delimiter=';')
        rows = list(reader)
        assert reader.fieldnames == ['ugyszam','kotvenyszam','kartipus','karesemeny_datum','becsult_osszeg','karleiras']
    assert len({r['ugyszam'] for r in rows}) == len(rows)
    return {r['ugyszam']:r for r in rows}
old, new = load(prior), load(fresh)
assert len(old) == len(new) == 13
assert old == new, 'Original saved records differ from verified batch; investigate before any write'
shutil.copy2(fresh,HERE/fresh.name)
report = {'status':'passed','date':'2026-10-07','scope':'Original readiness portal, actual fresh user-exported CSV(6)',
          'displayed_total_user_confirmed':33,'own_records':13,'all_prior_records_and_all_six_fields_unchanged':True,
          'new_or_missing_records':0,'fresh_sha256':hashlib.sha256(fresh.read_bytes()).hexdigest(),
          'prior_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
          'byte_identical':fresh.read_bytes()==prior.read_bytes(),'preserved_fresh_export':fresh.name,
          'original_data_loss_observed':False,'agent_portal_action':False,
          'next':'Leave original unchanged; user returns to manual_reset_20261007/manual_reset_portal.html and confirms MANUAL RESET TEST badge/current count before any submission.'}
(HERE/'original_records_reconciliation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
