"""Run portable offline checks; never access services, browsers or robots."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    checks = []
    manifest = json.loads((ROOT / 'course_skill_manifest.json').read_text(encoding='utf-8'))
    from harness.lessons import catalog, snapshot
    imported = catalog(ROOT)['days']
    unavailable = []
    for name, day in manifest['days'].items():
        if name in imported:
            continue  # Imported bytes have separate provenance; reviewed hashes are NOT reset.
        if not (ROOT / name / name).exists():
            unavailable.append(name)
            continue  # Course bundles are intentionally local-only, not a failed code test.
        for item in day['files']:
            path = ROOT / item['path']
            checks.append({'check': item['path'], 'passed': path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']})
    for name, current in imported.items():
        record = json.loads((ROOT / current['record']).read_text(encoding='utf-8'))
        checks.append({'check': f'{name} imported source bytes',
                       'passed': snapshot(ROOT / name / name) == record['files'],
                       'runbook_review': current['runbook_review']})
    for skill in ['bpa-course-access', 'bpa-nap01', 'bpa-nap02', 'bpa-nap03', 'bpa-nap04',
                  'bpa-import-lessons', 'bpa-audit-injections']:
        path = ROOT / '.agents/skills' / skill / 'SKILL.md'
        text = path.read_text(encoding='utf-8')
        checks.append({'check': skill, 'passed': text.startswith('---\n') and f'name: {skill}\n' in text and 'harness/WORKFLOWS.md' in text})
    suites = [('.', ['harness.tests.test_portable', 'harness.tests.test_legacy_tracker', 'harness.tests.test_lessons']),
              ('harness/course_tools/day03', ['test_bpa_access', 'test_api_exercises']),
              ('harness/course_tools/day04/setup_2026-10-06', ['test_verify_portal_batch'])]
    for cwd, modules in suites:
        result = subprocess.run([sys.executable, '-m', 'unittest', '-v', *modules], cwd=ROOT / cwd,
                                capture_output=True, text=True, encoding='utf-8', errors='replace')
        checks.append({'check': ' / '.join(modules), 'passed': result.returncode == 0, 'output': result.stdout + result.stderr})
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Offline only; no new-laptop platform run claimed',
              'local_lesson_sources_unavailable': unavailable,
              'passed': all(c['passed'] for c in checks), 'checks': checks}
    out = ROOT / '.bpa/verification/offline.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for check in checks:
        if not check['passed']:
            print(json.dumps(check, ensure_ascii=True))
    print(f"Offline checks: {len(checks)}; passed={result['passed']}. Report: .bpa/verification/offline.json")
    if unavailable:
        print('Local-only lessons not installed/source-verified: ' + ', '.join(unavailable))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
