"""Run the installed official UiPath CLI with explicit per-process project context.

No MCP/vendor patch, installation, credentials or automatic retries. This launcher
does not make a failed workflow successful merely because the CLI exits zero.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


def official_cli():
    launcher = shutil.which('uip')
    node = shutil.which('node')
    if not launcher or not node:
        raise ValueError('Install the official @uipath/cli and Node; neither is installed by this launcher.')
    installed = Path(launcher).resolve()
    entry = (installed.parent/'node_modules/@uipath/cli/dist/index.js'
             if installed.suffix.lower() == '.cmd' else installed)
    package = entry.parent.parent/'package.json'
    if not entry.is_file() or not package.is_file():
        raise ValueError('Cannot resolve the installed official UiPath npm entry point.')
    if json.loads(package.read_text(encoding='utf-8'))['name'] != '@uipath/cli':
        raise ValueError('The resolved entry point is not @uipath/cli.')
    # Invoke Node directly, avoiding cmd.exe interpolation of project/file paths.
    return [node, str(entry)]


def envelope(stdout):
    decoder = json.JSONDecoder()
    for match in reversed(list(re.finditer(r'(?m)^\{', stdout))):
        try:
            value, _ = decoder.raw_decode(stdout[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and 'Result' in value:
            return value
    return None


def successful(action, result):
    if not result or result.get('Result') != 'Success':
        return False
    data = result.get('Data')
    if not isinstance(data, dict):
        return False
    if action == 'build':
        return data.get('Success') is True
    if action == 'validate':
        # --min-severity error requests errors only; unknown shapes fail closed.
        return data.get('message') == 'No diagnostics found.'
    if 'hasErrors' in data:
        return (data['hasErrors'] is False and data.get('errorMessage') is None
                and data.get('debugState') in (None, 'Completed'))
    return data.get('errors') == [] and data.get('output') == 'Session ended'


def execute(action, project, workflow, evidence, timeout=120, skip_build=False):
    project = Path(project).resolve(strict=True)
    if not project.is_dir() or not (project/'project.json').is_file():
        raise ValueError('Project must be a directory containing project.json.')
    command = official_cli() + ['rpa', action]
    if action == 'build':
        command.append(str(project))
    else:
        file = (project/workflow).resolve(strict=True)
        if not file.is_relative_to(project) or file.suffix.lower() not in ('.xaml', '.cs'):
            raise ValueError('Workflow must be an existing XAML/CS file inside the project.')
        command += ['--file-path', str(file), '--project-dir', str(project)]
        if action == 'validate':
            command += ['--min-severity', 'error']
        elif skip_build:
            command.append('--skip-build')
    command += ['--timeout', str(timeout), '--output', 'json']
    evidence = Path(evidence).resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    (evidence/'invocation.json').write_text(json.dumps({'command':command, 'cwd':str(project)}, indent=2), encoding='utf-8')
    # The real process argv AND cwd identify this project, including relative I/O.
    completed = subprocess.run(command, cwd=project, capture_output=True, shell=False)
    # Some packager warnings use the Windows code page. Preserve the original
    # bytes even when a mixed-encoding stream cannot be displayed as UTF-8.
    (evidence/'stdout.log').write_bytes(completed.stdout)
    (evidence/'stderr.log').write_bytes(completed.stderr)
    stdout = completed.stdout.decode('utf-8', errors='replace')
    stderr = completed.stderr.decode('utf-8', errors='replace')
    result = envelope(stdout)
    passed = completed.returncode == 0 and successful(action, result)
    record = {'action':action, 'transport':'official CLI', 'mcp_used':False,
              'cli_exit_code':completed.returncode, 'success':passed, 'result':result}
    (evidence/'result.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return subprocess.CompletedProcess(command, completed.returncode, stdout, stderr), record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('validate', 'build', 'run'))
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--file', default='Main.xaml')
    parser.add_argument('--evidence', type=Path, required=True, help='New directory; existing evidence is never overwritten')
    parser.add_argument('--timeout', type=int, default=120)
    parser.add_argument('--skip-build', action='store_true', help='Run only: use only after an unchanged successful build')
    args = parser.parse_args()
    if args.timeout < 1 or (args.skip_build and args.action != 'run'):
        parser.error('Use a positive timeout; --skip-build is only for run.')
    try:
        completed, record = execute(args.action, args.project, args.file, args.evidence,
                                    args.timeout, args.skip_build)
    except (OSError, ValueError) as exc:
        parser.exit(2, str(exc)+'\n')
    sys.stdout.write(completed.stdout)
    sys.stderr.write(completed.stderr)
    print('Verified success: '+str(record['success'])+'; evidence: '+str(args.evidence.resolve()))
    return 0 if record['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
