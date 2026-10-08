"""Verify the two actual native runs and preserve a curated source package."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'nap03/working'))
from bpa_access import read_env

reports = [json.loads((HERE / f'run{i}.verification.json').read_text('utf-8')) for i in (1,2)]
assert all(r['passed'] for r in reports)
rows = [r['rows'] for r in reports]
assert all({x['CMC_ID'] for x in rr} == {1,1027,5426} for rr in rows)
stamps = [rr[0]['FetchedUTC'] for rr in rows]
provider = [rr[0]['ProviderTimestamp'] for rr in rows]
assert stamps[1] > stamps[0] and provider[1] > provider[0]
assert any(a['Ár (EUR)'] != b['Ár (EUR)'] for a,b in zip(*rows))
run_text = (HERE / 'run2.json').read_text('utf-8-sig')
data = json.loads(run_text[run_text.index('{'):])['Data']
assert data['hasErrors'] is False and data['errorMessage'] is None
assert 'execution ended in:' in run_text and 'native Excel refresh saved' in run_text

dest = ROOT / 'nap03/deliverables/CMC_auto_refresh'
dest.mkdir(exist_ok=True)
project = HERE / 'CMC_Auto_Refresh'
for filename in ('Main.xaml','project.json','AGENTS.md','CMC_Auto_Refresh.xlsx'):
    shutil.copy2(project / filename, dest / filename)
for i in (1,2):
    for suffix in ('xlsx','verification.json','quotes.json','json'):
        shutil.copy2(HERE / f'run{i}.{suffix}', dest / f'run{i}.{suffix}')
shutil.copy2(HERE / 'build.json', dest / 'build.json')
safe_values = [v for v in read_env().values() if len(v) >= 8]
needles = [v.encode(enc) for v in safe_values for enc in ('utf-8','utf-16-le')]
for file in dest.iterdir():
    if not file.is_file():
        continue
    pieces = [file.read_bytes()]
    if file.suffix == '.xlsx':
        with zipfile.ZipFile(file) as z:
            pieces += [z.read(n) for n in z.namelist()]
    assert not any(n in p for n in needles for p in pieces), 'Credential scan failed'
summary = {
    'status':'passed','date':'2026-10-07','actual_native_excel_runs':2,
    'fetched_utc':stamps,'provider_timestamp':provider,
    'provider_and_fetched_timestamps_advanced':True,'numeric_prices_changed':True,
    'rows_each':3,'credential_scan':'passed; workbook decoded mashup scanned by verify_cmc_workbook.py',
    'original_workbook_sha256':hashlib.sha256((ROOT/'nap03/deliverables/CMC_arfolyamok_SOL.xlsx').read_bytes()).hexdigest(),
    'cli_runtime_shape':'Actual CLI returned hasErrors=false/errorMessage=null with output={} and streamed execution-ended log. No Session ended string was returned; this version differs from the current skill flat-envelope example.',
    'first_run_filter_limit':'First run filter retained output only; actual workbook/quote equality independently verified. Second run preserves complete actual hasErrors verdict.',
    'scheduler_installed':False,'unattended_limits':'Finite local execution only. Needs installed licensed Office/UiPath, local Windows session, network/API access and existing secure env. No logged-out/locked-host service test.'}
(dest/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
