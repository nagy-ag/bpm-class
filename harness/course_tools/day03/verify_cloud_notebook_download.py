"""Inspect actual user-downloaded course notebook; never executes its cells."""
import ast
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
from bpa_access import read_env

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('download', type=Path, help='Actual saved .ipynb file; no cells are executed.')
parser.add_argument('--output', type=Path, default=ROOT / '.bpa/work/nap03/notes/notebook_download_verification.json')
parser.add_argument('--reference', type=Path, default=ROOT / '.bpa/work/nap03/working/API_automation/BPA_Nap3_Zoho.ipynb')
args = parser.parse_args()
download = args.download
expected = args.reference
actual_bytes = download.read_bytes()
actual = json.loads(actual_bytes)
reference = json.loads(expected.read_text(encoding='utf-8'))
checks = []

def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})
    if not condition:
        raise SystemExit('Notebook check failed: ' + name)

check('Cell count matches preserved course notebook', len(actual['cells']) == len(reference['cells']) == 19)
for i, (a, b) in enumerate(zip(actual['cells'], reference['cells'])):
    check(f'Cell{i} type preserved', a['cell_type'] == b['cell_type'])
    source = ''.join(a['source'])
    other = ''.join(b['source'])
    if a['cell_type'] == 'code':
        check(f'Cell{i} Python source meaning preserved', ast.dump(ast.parse(source)) == ast.dump(ast.parse(other)))
        compile(source, f'<downloaded-cell-{i}>', 'exec')
        check(f'Cell{i} outputs empty and execution count cleared', not a.get('outputs') and a.get('execution_count') is None)
    else:
        check(f'Cell{i} lesson text preserved', source.strip() == other.strip())
values = read_env(ROOT / '.env.local') if (ROOT / '.env.local').exists() else {}
secret_values = [v for k, v in values.items() if v and any(t in k for t in ('KEY', 'SECRET', 'TOKEN', 'GRANT_CODE', 'CLIENT_ID'))]
check('Configured credential values absent from complete downloaded bytes',
      not any(v.encode('utf-8') in actual_bytes or v.encode('utf-16-le') in actual_bytes for v in secret_values))
report = {
    'status': 'passed', 'checked_at': date.today().isoformat(), 'checks': checks,
    'download_method': 'User-supplied local notebook file; this verifier does not assert cloud execution',
    'downloaded_filename': download.name, 'download_sha256': hashlib.sha256(actual_bytes).hexdigest(),
    'reference_sha256': hashlib.sha256(expected.read_bytes()).hexdigest(),
    'source_content_matches_preserved_notebook': True, 'cells_executed_by_verifier': False,
    'note': 'The downloaded filename is the original course name; verification establishes content equivalence, not a specific cloud file ID from metadata.'
}
out = args.output
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Passed {len(checks)} downloaded notebook checks; no cells executed.')
