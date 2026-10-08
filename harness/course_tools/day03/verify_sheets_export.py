"""Read actual Google Sheets export; does not author a workbook or call APIs."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import zipfile
import openpyxl
from bpa_access import read_env

p = argparse.ArgumentParser()
p.add_argument('export', type=Path)
p.add_argument('report', type=Path)
p.add_argument('--solana', action='store_true')
p.add_argument('--previous', type=Path)
a = p.parse_args()
expected_names = ['Bitcoin', 'Ethereum'] + (['Solana'] if a.solana else [])
secrets = [v.encode(enc) for k,v in read_env().items() if v and len(v) >= 8
           and any(t in k for t in ('KEY','SECRET','TOKEN','GRANT_CODE','CLIENT_ID'))
           for enc in ('utf-8','utf-16-le')]
with zipfile.ZipFile(a.export) as z:
    assert not any(n in z.read(name) for name in z.namelist() for n in secrets), 'Credential scan failed'
wb = openpyxl.load_workbook(a.export, data_only=True)
s = wb['ARFOLYAMOK']
rows = list(s.iter_rows(min_row=1,max_col=3,values_only=True))
assert rows[0] == ('Kripto','Ár (EUR)','Frissítve'), 'Incorrect header'
data = [r for r in rows[1:] if any(v is not None for v in r)]
assert [r[0] for r in data] == expected_names, 'Incorrect coin rows'
assert all(type(r[1]) in (int,float) and r[1] > 0 for r in data), 'Prices must be positive numbers'
assert all(isinstance(r[2],datetime) for r in data), 'Timestamps must be native date values'
assert len({r[2] for r in data}) == 1, 'One request timestamp expected'
stamp = data[0][2].isoformat()
if a.previous:
    prior = json.loads(a.previous.read_text(encoding='utf-8'))
    assert stamp > prior['sheet_timestamp'], 'Timestamp did not advance'
report = {'status':'passed','native_google_sheets_export':True,'sheet':'ARFOLYAMOK',
          'range':f'A1:C{len(data)+1}','sheet_timestamp':stamp,
          'rows':[{'coin':r[0],'price_eur':r[1],'timestamp':r[2].isoformat()} for r in data],
          'numeric_prices_and_native_dates':True,'configured_credentials_absent':True,
          'refresh_timestamp_advanced':bool(a.previous),'export_filename':a.export.name}
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
