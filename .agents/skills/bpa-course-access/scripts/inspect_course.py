"""Inspect BPA source freshness or print a supplied lesson. Never reads secrets."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

def days(root):
    return sorted(p.name for p in root.glob('nap*') if p.is_dir()
                  and re.fullmatch(r'nap[0-9]{2,3}', p.name)
                  and (p / p.name / 'index.html').is_file())


class LessonText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if not self.hidden and tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'tr', 'pre', 'br'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
        if not self.hidden and tag in ('td', 'th'):
            self.parts.append(' | ')

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip() + ' ')

    def text(self):
        return '\n'.join(line.strip() for line in ''.join(self.parts).splitlines() if line.strip())


def within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def inspect(root: Path, day: str):
    root = Path(root).resolve()
    manifest = json.loads((root / 'course_skill_manifest.json').read_text(encoding='utf-8'))
    source = (root / day / day).resolve()
    reviewed = manifest['days'].get(day, {})
    expected = {entry['path']: entry['sha256'] for entry in reviewed.get('files', [])}
    current = {}
    for path in source.rglob('*'):
        if path.is_file():
            resolved = path.resolve()
            if not within(resolved, source):
                raise ValueError('A source file resolves outside its supplied bundle.')
            current[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    changed = sorted(name for name in current.keys() & expected.keys() if current[name] != expected[name])
    return {'day': day, 'supplied_files': len(current), 'changed': changed,
            'added': sorted(current.keys() - expected.keys()), 'missing': sorted(expected.keys() - current.keys()),
            'skill': reviewed.get('skill'), 'review_required': not reviewed or current != expected,
            'chapters': reviewed.get('chapters', [])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--day', help='Installed day, including newly imported napXX bundles')
    parser.add_argument('--lesson', help='index.html or pages/<filename>.html within the selected supplied day')
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / 'AGENTS.md').is_file() or not (root / 'harness').is_dir():
        parser.error('Choose the BPA project root.')
    available = days(root)
    if not available:
        parser.error('No local lesson bundles installed. Explicitly import your own course ZIP first.')
    if args.day and args.day not in available:
        parser.error('Choose an installed napXX lesson day.')
    if args.lesson:
        if not args.day:
            parser.error('--lesson requires --day.')
        bundle = (root / args.day / args.day).resolve()
        path = (bundle / args.lesson).resolve()
        allowed = path == bundle / 'index.html' or (path.parent == bundle / 'pages' and path.suffix == '.html')
        if not allowed or not within(path, bundle) or not path.is_file():
            parser.error('Choose an existing index.html or pages/*.html in the supplied bundle.')
        reader = LessonText()
        reader.feed(path.read_text(encoding='utf-8-sig'))
        print(reader.text())
        return 0
    results = [inspect(root, day) for day in ([args.day] if args.day else available)]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(r['changed'] or r['added'] or r['missing'] for r in results) else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError):
        print('Source inspection failed; check the root and source manifest.', file=sys.stderr)
        raise SystemExit(2)
