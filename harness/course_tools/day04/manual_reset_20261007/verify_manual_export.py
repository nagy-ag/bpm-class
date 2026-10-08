"""Offline read-only verification of the user-exported isolated manual case."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--replay', action='store_true')
args = parser.parse_args()
number = 7 if args.replay else 5
source = Path(f'C:/Users/nagya/Downloads/sajat_karbejelentesek ({number}).csv')
raw = source.read_bytes()
with source.open(encoding='utf-8-sig',newline='') as stream:
    reader = csv.DictReader(stream,delimiter=';')
    headers = reader.fieldnames
    rows = list(reader)
assert headers == ['ugyszam','kotvenyszam','kartipus','karesemeny_datum','becsult_osszeg','karleiras']
assert len(rows) == 1, 'Expected exactly one isolated own record'
expected = json.loads((HERE/'preparation.json').read_text('utf-8'))['first_input_row']
row = rows[0]
assert row['ugyszam'] == 'K-GY-4147'
for field in ('kotvenyszam','kartipus','karesemeny_datum','becsult_osszeg','karleiras'):
    assert row[field] == str(expected[field]), f'Incorrect field: {field}'
copy = HERE/source.name
shutil.copy2(source,copy)
assert copy.read_bytes() == raw
report = {'status':'passed','evidence_source':f'Actual user-downloaded CSV({number}), compared with supplied first input row',
          'export_sha256':hashlib.sha256(raw).hexdigest(),'preserved_export':copy.name,
          'own_records':1,'displayed_total_user_confirmed':21,'all_five_fields_exact':True,
          'case_id_matches_confirmation_screenshot':True,'record':row,
          'new_form_action_verified':args.replay,'reset_verified':False,
          'next':'User resets only isolated disposable case; verify20baseline and empty form' if args.replay else 'Confirm new-record button returned empty form before isolated practice reset'}
report_name = 'replay_export_verification.json' if args.replay else 'manual_export_verification.json'
(HERE/report_name).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
review_path = HERE/('replay_confirmation_review.json' if args.replay else 'manual_confirmation_review.json')
review = json.loads(review_path.read_text('utf-8'))
review['description_verification'] = f'Passed: actual CSV({number}) description exactly matches supplied workbook row'
review['all_five_saved_fields_verified'] = True
review_path.write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'passed','own_records':1,'displayed_total_user_confirmed':21,'all_five_fields_exact':True}))
