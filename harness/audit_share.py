"""Inspect staged/tracked bytes for local credentials; never print values."""
import argparse
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def known_secrets(root):
    path = root / '.env.local'
    if not path.exists():
        return []
    values = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        m = re.fullmatch(r'\s*([A-Z_]+)\s*=(.*)', line)
        if m and not m[1].endswith('EXPIRES_AT') and any(word in m[1] for word in ('KEY', 'SECRET', 'TOKEN', 'GRANT_CODE')):
            value = m[2].strip().strip('"\'')
            if len(value) >= 8:
                values.extend((value.encode(), value.encode('utf-16le')))
    return values


def inspect_bytes(name, raw, secrets, depth=0):
    errors = []
    if any(secret in raw for secret in secrets):
        errors.append({'path': name, 'reason': 'known credential bytes found'})
    # Strong provider formats only; course demo literals are not treated as actual keys.
    if re.search(rb'(?<![\w-])(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-proj-[A-Za-z0-9_-]{40,})(?![\w-])', raw):
        errors.append({'path': name, 'reason': 'provider credential format found'})
    if raw.startswith(b'PK\x03\x04'):
        if depth >= 8:
            return errors + [{'path': name, 'reason': 'archive nesting limit; manual review required'}]
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                if sum(item.file_size for item in archive.infolist()) > 256 * 1024 * 1024:
                    return errors + [{'path': name, 'reason': 'archive expansion limit; manual review required'}]
                for item in archive.infolist():
                    if not item.is_dir():
                        errors.extend(inspect_bytes(name + '::' + item.filename, archive.read(item), secrets, depth + 1))
        except (zipfile.BadZipFile, RuntimeError):
            errors.append({'path': name, 'reason': 'unreadable archive; manual review required'})
    return errors


def audit(root=ROOT, staged=False):
    args = ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z'] if staged else ['git', 'ls-files', '-z']
    paths = subprocess.check_output(args, cwd=root).decode('utf-8').split('\0')
    secrets = known_secrets(root)
    errors = []
    count = 0
    entries = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=root).split(b'\0')
    objects = {}
    for entry in filter(None, entries):
        info, path = entry.split(b'\t', 1)
        _mode, oid, stage = info.split()
        if stage != b'0':
            raise ValueError('Resolve index conflicts before sharing audit.')
        objects[path.decode('utf-8')] = oid
    selected = list(filter(None, paths))
    oids = list(dict.fromkeys(objects[p] for p in selected))
    process = subprocess.run(['git', 'cat-file', '--batch'], cwd=root,
                             input=b'\n'.join(oids) + b'\n' if oids else b'', capture_output=True, check=True)
    stream = io.BytesIO(process.stdout)
    blobs = {}
    for oid in oids:
        header = stream.readline().split()
        if len(header) != 3 or header[1] != b'blob':
            raise ValueError('Unreadable staged object; abort publication.')
        blobs[oid] = stream.read(int(header[2]))
        if stream.read(1) != b'\n':
            raise ValueError('Invalid Git object framing.')
    for name in selected:
        parts = PurePosixPath(name).parts
        if re.fullmatch(r'nap[0-9]+', parts[0]):
            errors.append({'path': name, 'reason': 'local-only course folder must not be shared'})
        if (PurePosixPath(name).name.startswith('.env') and name != '.env.example') or any(
                part in {'.bpa', '.venv', 'node_modules', '__pycache__', '.local', '.project', '.codex'} for part in parts):
            errors.append({'path': name, 'reason': 'private/runtime path staged'})
        raw = blobs[objects[name]]
        errors.extend(inspect_bytes(name, raw, secrets))
        count += 1
    return {'scope': 'staged Git bytes' if staged else 'tracked Git index bytes',
            'files': count, 'secret_values_disclosed': False, 'passed': not errors, 'findings': errors}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--staged', action='store_true')
    p.add_argument('--report', type=Path)
    a = p.parse_args()
    result = audit(staged=a.staged)
    print(json.dumps(result, indent=2))
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(json.dumps(result, indent=2), encoding='utf-8')
    raise SystemExit(0 if result['passed'] else 1)
