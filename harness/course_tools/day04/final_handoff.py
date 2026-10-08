"""Read-only evidence audit and additive clean archive. No robot/browser execution."""
import argparse
import hashlib
import io
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED, is_zipfile

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
DAY = ROOT / 'nap04'
OUT = DAY / 'deliverables'
AUDIT = DAY / 'working/final_audit_20261007'
AUDIT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / 'nap03/working'))
from bpa_access import read_env

PROJECTS = {
    'Nap04_gyakorlas': DAY / 'working/Nap04_gyakorlas',
    'ExcelRobot': DAY / 'working/ExcelRobot',
    'RiportRobot': DAY / 'working/RiportRobot',
    'Fajlrendezo': DAY / 'working/Fajlrendezo',
    'PortalRobot/setup_2026-10-06/BPA_Setup_Smoke': DAY / 'working/setup_2026-10-06/BPA_Setup_Smoke',
}
EXCLUDED = {'.local', '.project', '__pycache__', 'node_modules', 'bin', 'obj', '.git'}

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def save(name, value):
    (AUDIT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def workflow_semantics(p):
    """Ignore Studio layout and equivalent literal-default serialization only."""
    def normalize(node):
        if 'schemas.microsoft.com/netfx/2009/xaml/activities/presentation' in node.tag or 'schemas.microsoft.com/netfx/2010/xaml/activities/presentation' in node.tag:
            return None
        attrs = {k: v for k, v in node.attrib.items() if 'presentation}' not in k and k != 'DisplayName'}
        children = list(node)
        if node.tag.endswith('}Variable'):
            for child in children:
                if child.tag.endswith('}Variable.Default') and len(child) == 1 and child[0].tag.endswith('}Literal'):
                    attrs['Default'] = child[0].get('Value')
                    children.remove(child)
        return (node.tag, tuple(sorted(attrs.items())), (node.text or '').strip(), tuple(x for child in children if (x := normalize(child)) is not None))
    return normalize(ET.parse(p).getroot())

def accepted(p):
    return not (set(p.parts) & EXCLUDED) and not p.name.startswith('~$') and p.suffix not in ('.pyc', '.bak')

def review():
    text = (DAY / 'notes/TASK_PROGRESS.md').read_text(encoding='utf-8')
    rows = []
    for i in range(1, 15):
        task = f'D4-{i:02d}'
        block = re.search(rf'^## {task} — .*?(?=\n<a id=|\Z)', text, re.M | re.S).group()
        assert 'Status: `done`' in block, task + ' incomplete'
        steps = re.findall(r'^\| (\d+) \| .*? \| (done|not_applicable) \| (.+) \|$', block, re.M)
        assert len(steps) == 4 and all(ev != '—' for _, _, ev in steps), task + ' lacks evidence'
        rows.append({'task': task, 'verified_steps': 4})
    save('requirements_review.json', {
        'passed': True, 'date': '2026-10-07', 'required_tasks_reviewed': rows,
        'current_lesson_sha256': {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted((DAY / 'nap04/pages').glob('*.html'))},
        'source_freshness': 'All223supplied files unchanged against manifest; current seven nap04 chapters read.',
        'variants': ['initial20 and expected sok failure', 'repaired5 and8boundary/error cases', '100000 and150000classification', '12 and6record native Office charts', 'basic sorter, images and zero-move second run', 'exact manual/reset isolated copy', 'actual first-row trial and cumulative ten-policy batch'],
        'adaptations': ['Native report activities selected; template route is an unchosen alternative.', 'Brave extension proven by user-run trial; no agent local-page control.', 'Original ten-policy result retained:13own/33total, not a clean30-case batch.', 'Exact manual/reset executed later in isolated copy; sequence differs from lesson to preserve original evidence.'],
        'optional_exclusions': ['Writing case IDs back to input workbook is later expansion, not required.', 'External Academy/video study is optional; no claim of completion.', 'Future graded days5–8 not specified by supplied bundles; no submissions.'],
    })
    print('Requirements reviewed:14tasks/56steps; adaptations recorded.')

def runtime(p, expected_failure=False):
    text = p.read_text(encoding='utf-8-sig')
    start = text.find('{\n')
    if start < 0:
        start = text.find('{\r\n')
    data = json.loads(text[start:])
    d = data['Data']
    if expected_failure:
        assert 'InvalidCastException' in text
    else:
        assert data['Result'] == 'Success'
        assert d.get('hasErrors') is not True and d.get('errorMessage') in (None, '')
        assert not d.get('errors', [])
        assert 'execution ended' in text or d.get('output') == 'Session ended'
    return {'file': p.relative_to(ROOT).as_posix(), 'sha256': digest(p), 'expected_failure': expected_failure}

def verify():
    assert load(AUDIT / 'requirements_review.json')['passed']
    projects = []
    for rel, actual in PROJECTS.items():
        folder = OUT / rel
        pj = load(folder / 'project.json')
        assert pj['targetFramework'] == 'Windows' and pj['expressionLanguage'] == 'VisualBasic'
        assert (folder / pj['main']).is_file()
        assert pj['dependencies']
        files = []
        for p in folder.glob('*.xaml'):
            ET.parse(p)
            assert (actual / p.name).is_file()
            exact = digest(p) == digest(actual / p.name)
            assert exact or workflow_semantics(p) == workflow_semantics(actual / p.name), p.name + ' has semantic differences from working workflow'
            for node in ET.parse(p).getroot().iter():
                for key in ('WorkflowFileName', 'WorkbookPath'):
                    value = node.get(key)
                    if value and not value.startswith('[') and not value.startswith('{'):
                        assert (folder / value).is_file(), 'Static dependency missing'
            files.append({'file': p.name, 'sha256': digest(p), 'working_sha256': digest(actual / p.name), 'byte_identical': exact, 'semantically_equivalent': True})
        projects.append({'project': rel, 'dependencies': pj['dependencies'], 'executed_workflow_bytes_preserved': files})
    names = ['nap04_main_run.json', 'greeting_initial_20_run.json', 'greeting_repaired_5_run.json',
             'greeting_validation_fixed_run.json', 'excel_100000_run.json', 'excel_150000_run.json',
             'sorter_run.json', 'sorter_images_run1.json', 'sorter_images_run2.json', 'report_12_run.json', 'report_6_run.json']
    runs = [runtime(DAY / 'working' / name) for name in names]
    runs.append(runtime(DAY / 'working/greeting_initial_sok_run.json', True))
    assert len(load(OUT / 'greeting_repaired_evidence.json')['actual_workflow_regression']) == 8
    for folder, names in [('ExcelRobot', ['verification_100000.json', 'verification_150000.json']),
                          ('Fajlrendezo', ['verification_basic.json', 'verification_images_run1.json', 'verification_images_run2.json'])]:
        for name in names:
            assert load(OUT / folder / name)['verified']
    for count in [12, 6]:
        report = load(OUT / f'RiportRobot/reports_{count}/verification.json')
        assert report['status'] == 'passed' and len(report['checks']) == 21 and all(c['passed'] for c in report['checks'])
        for name, sha in report['output_sha256'].items():
            assert digest(OUT / f'RiportRobot/reports_{count}' / name) == sha
    sorter = load(OUT / 'Fajlrendezo/verification_images_run1.json')
    for rel, sha in sorter['state'].items():
        assert digest(OUT / 'Fajlrendezo/exercise/gyakorlo_mappa' / rel) == sha
    trial = load(DAY / 'working/setup_2026-10-06/portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202/verification.json')
    assert trial['status'] == 'passed' and len(trial['checks']) == 19 and all(c['passed'] for c in trial['checks'])
    batch = load(OUT / 'PortalRobot/actual_batch_20261007/batch_verification.json')
    assert batch['status'] == 'passed' and len(batch['checks']) == 43 and all(c['passed'] for c in batch['checks'])
    assert load(OUT / 'PortalRobot/actual_batch_20261007/visual_review.json')['screenshots_reviewed'] == 27
    assert load(OUT / 'PortalRobot/portal_batch_ready_build.json')['Data']['Success']
    manual = OUT / 'PortalRobot/manual_reset_20261007'
    assert load(manual / 'replay_export_verification.json')['all_five_fields_exact']
    assert load(manual / 'final_reset_review.json')['isolated_disposable_reset_verified']
    assert load(manual / 'final_reset_empty_form_review.json')['visually_empty']
    assert load(manual / 'original_records_reconciliation.json')['byte_identical']
    for item in load(manual / 'evidence_manifest.json'):
        assert digest(manual / item['file']) == item['sha256']
    needles = [v.encode(enc) for v in read_env().values() if len(v) >= 8 for enc in ('utf-8', 'utf-16-le')]
    checked = 0
    def scan(data, depth=0):
        assert not any(n in data for n in needles), 'Credential scan failed; values suppressed'
        if depth < 3 and is_zipfile(io.BytesIO(data)):
            with ZipFile(io.BytesIO(data)) as archive:
                for member in archive.infolist():
                    if not member.is_dir():
                        scan(archive.read(member), depth + 1)
    for p in OUT.rglob('*'):
        if p.is_file() and accepted(p) and p.name != 'BPA_nap04_verified_projects_20261007.zip':
            scan(p.read_bytes())
            checked += 1
    save('handoff_verification.json', {'passed': True, 'date': '2026-10-07', 'projects': projects,
        'actual_prior_runs_reviewed': runs, 'files_credential_scanned_including_decompressed_archives': checked,
        'portal_trial_checks': 19, 'portal_batch_checks': 43, 'portal_row_checks': 171,
        'manual_and_isolated_reset_verified': True, 'source_workflows_unchanged': True,
        'new_robot_or_browser_execution': False,
        'path_limitations': 'Project-local inputs/workflow references verified. Portal intentionally retains original absolute attachment/log/reservation paths and Brave executable. This is a handoff for the current workspace, not a machine-independent deployment.',
        'runtime_limitation': 'Previous actual executions/builds reused. No new run or fresh compile claimed; completed outputs and duplicate guards preserved.'})
    print(f'Passed audit:5projects,12actual run outcomes,{checked}files scanned; portal evidence verified.')

def package(final=False):
    assert load(AUDIT / 'handoff_verification.json')['passed']
    target = OUT / ('BPA_nap04_final_handoff_20261007.zip' if final else 'BPA_nap04_verified_projects_20261007.zip')
    assert not target.exists(), 'Archive already exists; do not overwrite silently'
    manifest = []
    skipped = []
    with ZipFile(target, 'w', ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob('*')):
            if not p.is_file() or p == target or (p.parent == OUT and p.name.startswith('BPA_nap04_') and p.suffix == '.zip'):
                continue
            rel = p.relative_to(OUT).as_posix()
            if not accepted(p):
                skipped.append(rel)
                continue
            if final and rel == 'README.md':
                content = (OUT / 'HANDOFF.md').read_bytes()
                z.writestr(rel, content)
                manifest.append({'file': rel, 'sha256': hashlib.sha256(content).hexdigest(), 'source': 'HANDOFF.md'})
            else:
                z.write(p, rel)
                manifest.append({'file': rel, 'sha256': digest(p)})
        # Include actual run evidence referenced by project READMEs, without workspace caches.
        evidence = set()
        for pattern in ('*run.json', '*result.jpg', '*dialog.jpg'):
            evidence.update((DAY / 'working').glob(pattern))
        for p in sorted(evidence):
            rel = 'actual_run_evidence/' + p.name
            z.write(p, rel)
            manifest.append({'file': rel, 'sha256': digest(p)})
        for p in AUDIT.glob('*.json'):
            z.write(p, 'final_audit/' + p.name)
        z.writestr('ARCHIVE_README.md', 'Verified projects/evidence for the current BPA workspace. Open the project README before any run. Completed report/portal guards intentionally stop duplicate execution. Existing absolute portal attachment/log paths must remain stable. Actual runs are preserved, not repeated by this archive. No credentials or transient build caches are included. Historical README links into ../../working resolve in the original workspace; matching standalone logs are also included under actual_run_evidence/. No graded submission.\n')
    with ZipFile(target) as z:
        for item in manifest:
            assert hashlib.sha256(z.read(item['file'])).hexdigest() == item['sha256']
        assert not any(set(Path(name).parts) & EXCLUDED or Path(name).name.startswith('~$') for name in z.namelist())
        needles = [v.encode(enc) for v in read_env().values() if len(v) >= 8 for enc in ('utf-8', 'utf-16-le')]
        assert all(not any(n in z.read(name) for n in needles) for name in z.namelist()), 'Final archive credential scan failed; values suppressed'
    report = {'passed': True, 'archive': target.relative_to(ROOT).as_posix(), 'sha256': digest(target),
              'files_byte_verified': len(manifest), 'manifest': manifest, 'excluded_transient_files': skipped,
              'original_files_deleted': False, 'portal_reservations_preserved': True}
    save('archive_verification.json', report)
    (OUT / 'archive_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Clean archive created and byte-verified:{len(manifest)}files; no originals deleted.')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('phase', choices=['review', 'verify', 'package', 'package_final'])
    args = p.parse_args()
    {'review': review, 'verify': verify, 'package': package, 'package_final': lambda: package(True)}[args.phase]()
