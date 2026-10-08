"""Read-only final handoff checks; never emit credential values."""
import json
from pathlib import Path
from bpa_access import read_env

ROOT = Path(__file__).resolve().parents[2]
folder = ROOT/'nap03/deliverables'
needles = [v.encode(e) for v in read_env().values() if len(v) >= 8 for e in ('utf-8','utf-16-le')]
checked = 0
for path in folder.rglob('*'):
    if not path.is_file() or path.name.startswith('~$'):
        continue
    assert not any(n in path.read_bytes() for n in needles), 'Credential scan failed'
    checked += 1
    if path.suffix == '.ipynb':
        notebook = json.loads(path.read_text(encoding='utf-8'))
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                assert not cell.get('outputs') and cell.get('execution_count') is None
                compile(''.join(cell['source']), '<clean notebook>', 'exec')
positive = json.loads((folder/'API_automation/positive_verification.json').read_text(encoding='utf-8'))
negative = json.loads((folder/'API_automation/negative_verification.json').read_text(encoding='utf-8'))
assert positive['http_status'] == 201 and positive['exact_crm_readback'] and positive['crm_ui_verified']
assert not negative['crm_write_attempted']
assert negative['matching_records_before'] == negative['matching_records_after'] == negative['independent_readback_matching_records'] == 0
checkpoint = json.loads((folder/'API_automation/colab_execution_checkpoint.json').read_text(encoding='utf-8'))
assert checkpoint['cloud_save_verified'] and checkpoint['runtime_credentials_cleared'] and checkpoint['clean_cloud_all_outputs_empty']
download = json.loads((folder/'API_automation/notebook_download_verification.json').read_text(encoding='utf-8'))
assert checkpoint['download_verified'] and download['status'] == 'passed'
for name in ('sheets_btc_eth_run1.json','sheets_btc_eth_run2.json','sheets_sol_run.json','sheets_hourly_run.json'):
    assert json.loads((folder/'Sheets_automation'/name).read_text(encoding='utf-8'))['status'] == 'passed'
assert (folder/'Sheets_automation/sheets_hourly_trigger_removed.png').is_file()
assert json.loads((folder/'CMC_auto_refresh/verification.json').read_text(encoding='utf-8'))['status'] == 'passed'
for name in ('CMC_arfolyamok_BTC_ETH.verification.json','CMC_arfolyamok_SOL.verification.json','CMC_refresh_observations.json'):
    assert json.loads((folder/name).read_text(encoding='utf-8'))['passed']
report = {'passed':True,'files_scanned':checked,'clean_notebook':'No outputs; null execution counts; Python cells compile',
          'stored_actual_evidence':'Three actual Colab creates, both live branches, manual CRM and native Excel checks reviewed',
          'credential_scan':'Delivery bytes plus separate decoded/decompressed workbook mashup scans passed',
          'adaptation':'CMC Python header-authenticated fetch + native local JSON Power Query; no direct CMC refresh in workbook',
          'cloud_notebook_download_verified':True,'graded_submission':False,
          'additional_sheets_route':'Manual BTC/ETH refresh, SOL and actual Time-Driven run verified; practice trigger removed',
          'automatic_local_cmc_refresh':'Two actual canonical fetch/native Excel refresh-save executions verified'}
(folder/'handoff_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
