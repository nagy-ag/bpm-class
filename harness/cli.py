"""BPA portable setup. Offline by default; never starts robots or browsers."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from functools import wraps
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
STATES = {'not_started', 'in_progress', 'done', 'blocked', 'not_applicable'}
TASK_PATTERN = re.compile(r'^#{2,3} ([\w-]+) — ([^\n]+)\n(.*?)(?=^#{2,3} |^<a id=|\Z)', re.M | re.S)
STEP_PATTERN = re.compile(r'^\| (\d+) \| (.*?) \| (not_started|in_progress|done|blocked|not_applicable) \| (.*?) \|$', re.M)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix('.tmp')
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    pending.replace(path)


def task_definitions(root):
    tasks = []
    paths = [root / 'TASK_PROGRESS.md'] + [root / f'nap0{n}/notes/TASK_PROGRESS.md' for n in range(1, 5)]
    for path in paths:
        for match in TASK_PATTERN.finditer(path.read_text(encoding='utf-8-sig')):
            task_id, title, body = match.groups()
            if task_id == 'harness-01':
                continue  # Publishing this repository is not a colleague's exercise.
            steps = [{'number': int(n), 'action': action, 'state': 'not_started', 'evidence': ''}
                     for n, action, _old, _evidence in STEP_PATTERN.findall(body)]
            if not steps:
                continue
            dependencies = re.search(r'Dependencies: ([^\n]+)', body)
            requirements = re.sub(r'^Status: [^\n]*(?:\n|$)', '', body.split('| Step |')[0].strip(), flags=re.M).strip()
            tasks.append({'id': task_id, 'title': title,
                          'day': path.parts[-3] if path.parent.name == 'notes' else 'shared',
                          'requirements': requirements,
                          'dependencies': dependencies.group(1) if dependencies else '',
                          'owner': '', 'steps': steps})
    if not tasks or len({t['id'] for t in tasks}) != len(tasks):
        raise ValueError('Missing or duplicate task definitions.')
    return tasks


def render_progress(root, state):
    lines = ['# Local task progress', '', 'Private to this checkout. Reference completion is not copied.', '']
    for task in state['tasks']:
        pending = next((s for s in task['steps'] if s['state'] not in ('done', 'not_applicable')), None)
        lines += [f"## {task['id']} — {task['title']}", '',
                  f"Owner: {task['owner'] or 'unassigned'} · Next step: {pending['number'] if pending else 'complete'}", '',
                  task['requirements'], '', '| Step | Action / acceptance | Status | Evidence / blocker |',
                  '| --- | --- | --- | --- |']
        for step in task['steps']:
            ev = step['evidence'].replace('|', ' / ').replace('\n', ' ')
            lines.append(f"| {step['number']} | {step['action']} | {step['state']} | {ev or '—'} |")
        lines.append('')
    (root / '.bpa/PROGRESS.md').write_text('\n'.join(lines), encoding='utf-8')


def initialize(root=ROOT):
    root = Path(root).resolve()
    local = root / '.bpa'
    local.mkdir(exist_ok=True)
    if not (root / '.env.local').exists():
        shutil.copyfile(root / '.env.example', root / '.env.local')
    if not (local / 'config.json').exists():
        shutil.copyfile(root / 'harness/config.example.json', local / 'config.json')
    if not (local / 'progress.json').exists():
        state = {'schema': 1, 'created_utc': stamp(), 'tasks': task_definitions(root)}
        atomic_json(local / 'progress.json', state)
        render_progress(root, state)
    for day in range(1, 5):
        for kind in ('working', 'notes', 'deliverables'):
            (local / f'work/nap0{day}' / kind).mkdir(parents=True, exist_ok=True)
    return local


def state_lock(function):
    @wraps(function)
    def locked(root, *args, **kwargs):
        lock = root / '.bpa/progress.lock'
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise ValueError('Another update holds the progress lock; retry after it finishes. Preserve a stale lock until its owner is checked.') from None
        try:
            os.close(fd)
            return function(root, *args, **kwargs)
        finally:
            lock.unlink()
    return locked


@state_lock
def transition(root, task_id, number, state, evidence, owner, dependencies_checked=False):
    if state not in STATES - {'not_started'} or not evidence.strip() or not owner.strip():
        raise ValueError('State, owner and nonempty evidence are required.')
    path = root / '.bpa/progress.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    if task is None:
        raise ValueError('Unknown task; add its ordered acceptance steps before execution.')
    if task['owner'] and task['owner'] != owner:
        raise ValueError('Task belongs to another owner; coordinate handoff first.')
    step = next((s for s in task['steps'] if s['number'] == number), None)
    if step is None or any(s['number'] < number and s['state'] not in ('done', 'not_applicable') for s in task['steps']):
        raise ValueError('Missing step or unfinished prerequisite.')
    if step['state'] in ('done', 'not_applicable'):
        raise ValueError('Completed evidence is immutable; create a new task for a rerun.')
    if state in ('done', 'blocked', 'not_applicable') and step['state'] != 'in_progress':
        raise ValueError('Claim this step in_progress first.')
    if state == 'in_progress' and not dependencies_checked:
        raise ValueError('Read the requirements and confirm dependencies with --dependencies-checked.')
    task['owner'] = owner
    step.update(state=state, evidence=evidence, updated_utc=stamp())
    atomic_json(path, data)
    render_progress(root, data)
    with (root / '.bpa/events.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'utc': stamp(), 'task': task_id, 'step': number, 'state': state,
                                 'owner': owner, 'evidence': evidence}, ensure_ascii=False) + '\n')


def doctor(root=ROOT):
    def app(paths):
        return any(p.exists() for p in paths)
    programs = [Path(os.environ.get(k, 'C:/missing')) for k in ('ProgramFiles', 'ProgramFiles(x86)')]
    local = Path(os.environ.get('LOCALAPPDATA', 'C:/missing'))
    studio_paths = [local / 'Programs/UiPath/Studio/UiPath.Studio.exe'] + [p / 'UiPath/Studio/UiPath.Studio.exe' for p in programs]
    for base in [local / 'Programs/UiPathPlatform/Studio'] + [p / 'UiPathPlatform/Studio' for p in programs]:
        studio_paths.extend(base.glob('*/UiPath.Studio.exe'))
    checks = {
        'python_312_or_newer': sys.version_info >= (3, 12),
        'git_in_path': shutil.which('git') is not None,
        'local_state_initialized': (root / '.bpa/progress.json').is_file(),
        'credential_file_exists_values_not_inspected': (root / '.env.local').is_file(),
        'excel_executable_found': app([p / 'Microsoft Office/root/Office16/EXCEL.EXE' for p in programs]),
        'powerpoint_executable_found': app([p / 'Microsoft Office/root/Office16/POWERPNT.EXE' for p in programs]),
        'studio_executable_found': app(studio_paths),
    }
    for module in ('openpyxl', 'lxml', 'PIL', 'pptx', 'docx', 'yaml'):
        try:
            __import__(module)
            checks[f'python_{module}'] = True
        except ImportError:
            checks[f'python_{module}'] = False
    return {'scope': 'Offline discovery only; found executables do not prove activation or actual runs.',
            'checks': checks,
            'requires_live_verification': ['Codex browser tool exposed and working',
                'Native computer tool exposed/allowed, or precise user action handoff',
                'Office activated, edit/recalculate/refresh/save/reopen',
                'Studio licensed, packages restored, actual robot and Excel/PPT runs',
                'User browser extension and file permission; user-started portal trial',
                'Own authenticated Moodle/Google/Zoho sessions and own API access']}


@state_lock
def add_task(root, spec):
    path = root / '.bpa/progress.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    if not re.fullmatch(r'[A-Za-z0-9-]+', spec['id']) or any(t['id'] == spec['id'] for t in data['tasks']):
        raise ValueError('Use a new stable task ID.')
    if not spec.get('title') or not spec.get('steps') or not all(isinstance(s, str) and s.strip() for s in spec['steps']):
        raise ValueError('Title and ordered nonempty acceptance step strings are required.')
    data['tasks'].append({'id': spec['id'], 'title': spec['title'], 'day': spec.get('day', 'shared'),
        'requirements': spec.get('requirements', ''), 'dependencies': spec.get('dependencies', ''), 'owner': '',
        'steps': [{'number': n, 'action': action, 'state': 'not_started', 'evidence': ''}
                  for n, action in enumerate(spec['steps'], 1)]})
    atomic_json(path, data)
    render_progress(root, data)


@state_lock
def handoff(root, task_id, owner, to_owner, evidence):
    path = root / '.bpa/progress.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    if task is None:
        raise ValueError('Unknown task.')
    if task['owner'] != owner or not to_owner.strip() or not evidence.strip():
        raise ValueError('Current owner, new owner and exact resume evidence are required.')
    task['owner'] = to_owner
    atomic_json(path, data)
    render_progress(root, data)
    with (root / '.bpa/events.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'utc': stamp(), 'task': task_id, 'handoff_from': owner,
                                 'handoff_to': to_owner, 'evidence': evidence}) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'doctor', 'status'):
        commands.add_parser(name)
    add = commands.add_parser('add-task')
    add.add_argument('spec', type=Path)
    transfer = commands.add_parser('handoff')
    transfer.add_argument('task'); transfer.add_argument('--owner', required=True)
    transfer.add_argument('--to-owner', required=True); transfer.add_argument('--evidence', required=True)
    step = commands.add_parser('step')
    step.add_argument('task'); step.add_argument('number', type=int)
    step.add_argument('state', choices=sorted(STATES - {'not_started'}))
    step.add_argument('--owner', required=True)
    step.add_argument('--evidence', required=True)
    step.add_argument('--dependencies-checked', action='store_true')
    prepare = commands.add_parser('prepare')
    prepare.add_argument('project', choices=['Proba', 'Nap04_gyakorlas', 'ExcelRobot', 'RiportRobot', 'Fajlrendezo', 'PortalRobot', 'CMC_auto_refresh'])
    a = parser.parse_args()
    try:
        if a.command == 'init':
            initialize(); print('Created missing local files only. Own progress: .bpa/PROGRESS.md')
        elif a.command == 'doctor':
            result = doctor(); print(json.dumps(result, indent=2))
            if (ROOT / '.bpa').exists():
                atomic_json(ROOT / '.bpa/doctor.json', result)
        elif a.command == 'status':
            data = json.loads((ROOT / '.bpa/progress.json').read_text(encoding='utf-8'))
            for task in data['tasks']:
                pending = next((s for s in task['steps'] if s['state'] not in ('done', 'not_applicable')), None)
                print(f"{task['id']}: step {pending['number']} {pending['state']}" if pending else f"{task['id']}: complete")
        elif a.command == 'step':
            transition(ROOT, a.task, a.number, a.state, a.evidence, a.owner, a.dependencies_checked)
            print('Local ordered progress and event journal updated.')
        elif a.command == 'add-task':
            add_task(ROOT, json.loads(a.spec.read_text(encoding='utf-8-sig')))
            print('Added new task with pending acceptance steps.')
        elif a.command == 'handoff':
            handoff(ROOT, a.task, a.owner, a.to_owner, a.evidence)
            print('Ownership transferred; earlier evidence preserved.')
        elif a.command == 'prepare':
            from harness.projects import prepare_project
            print(prepare_project(ROOT, a.project))
    except (ValueError, FileNotFoundError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
