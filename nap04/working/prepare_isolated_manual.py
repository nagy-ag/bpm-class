"""Offline practice-copy preparation only; never launch browser or robot."""
from pathlib import Path
import hashlib
import json
import re
import openpyxl

ROOT = Path(__file__).resolve().parents[2]
source = ROOT/'nap04/working/readiness_2026-10-06/gyakorlo_karportal.html'
folder = ROOT/'nap04/working/manual_reset_20261007'
folder.mkdir(exist_ok=True)
original = source.read_bytes()
text = original.decode('utf-8')
old_key = 'bpa_nap04_sajat_ugyek_v1'
new_key = 'bpa_nap04_manual_reset_20261007_v1'
assert text.count(old_key) == 1
old_title = 'Meridian Biztosító | Kárrendszer (gyakorló példány)'
new_title = old_title + ' – MANUAL RESET TEST'
old_badge = '>Gyakorló példány</'
new_badge = '>MANUAL RESET TEST</'
assert text.count(old_title) == text.count(old_badge) == 1
changed = text.replace(old_key,new_key).replace(old_title,new_title).replace(old_badge,new_badge)
assert changed.replace(new_key,old_key).replace(new_title,old_title).replace(new_badge,old_badge) == text
target = folder/'manual_reset_portal.html'
target.write_bytes(changed.encode('utf-8'))
assert source.read_bytes() == original
wb = openpyxl.load_workbook(ROOT/'nap04/nap04/docs/karbejelentesek_input.xlsx',data_only=True)
sheet = wb['bejelentesek']
headers = [c.value for c in sheet[1]]
row = dict(zip(headers,[c.value for c in sheet[2]]))
assert row['kotvenyszam'] == 'TR-402318'
match = re.search(r'var LISTA\s*=\s*(\[.*?\]);',text,re.S)
assert match, 'Locate unchanged sample cases'
seeds = json.loads(match.group(1))
assert len(seeds) == 20
report = {'status':'prepared_offline_not_executed','source_sha256':hashlib.sha256(original).hexdigest(),
          'copy_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
          'exact_changes':['added-case storage namespace','window title','visible practice badge'],
          'restoring_three_changes_recovers_original':True,'seed_count':len(seeds),
          'original_storage_key':old_key,'isolated_storage_key':new_key,
          'first_input_row':row,'browser_opened_by_agent':False,'portal_executed_by_agent':False,
          'resume':'User opens copy privately, confirms visible MANUAL RESET TEST and20total/0own before entering anything. Never reset original completed portal.'}
(folder/'preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,default=str))
