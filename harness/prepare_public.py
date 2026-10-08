"""One-time public text redaction with private backups; source bundles untouched."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = ROOT / '.bpa/public-redactions.json'
    redactions = json.loads(config.read_text(encoding='utf-8')) if config.exists() else {}
    paths = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
    changed = []
    for name in sorted(set(filter(None, paths))):
        if any(name.startswith(f'nap0{n}/nap0{n}/') for n in range(1, 5)) or name == 'harness/prepare_public.py':
            continue
        path = ROOT / name
        if path.suffix not in {'.md', '.json', '.py', '.ps1', '.gs', '.html', '.ipynb', '.txt', '.xml'}:
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            continue
        result = text
        for old, new in redactions.items():
            result = result.replace(old, new)
        if result != text:
            backup = ROOT / '.bpa/private_export_backup' / name
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_bytes(raw)
            path.write_text(result, encoding='utf-8')
            changed.append(name)
    report = {'scope': 'Public textual reference export; original private bytes backed up locally',
              'files_redacted': changed, 'source_bundles_modified': False}
    out = ROOT / 'harness/reports/public_redactions.json'
    out.parent.mkdir(exist_ok=True)
    # Preserve initial inventory if a subsequent idempotent pass changes nothing.
    if changed or not out.exists():
        out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'Redacted {len(changed)} textual reference files; private backups preserved.')


if __name__ == '__main__':
    main()
