"""Reopen explicitly requested alternative while preserving the earlier route decision."""
from pathlib import Path
import re

p = Path('nap03/notes/TASK_PROGRESS.md')
s = p.read_text(encoding='utf-8')
for task in ('D3-05', 'D3-06', 'D3-07'):
    pattern = rf'(## {task} — .*?)(?=\n<a id=|\Z)'
    match = re.search(pattern, s, re.S)
    block = match.group(1)
    if 'Status: `not_applicable`' not in block:
        continue
    block = block.replace('Status: `not_applicable`', 'Status: `not_started`', 1)
    block = block.replace('Next step: None', 'Next step: 1', 1)
    block = block.replace('Scope: Sheets route. Dependencies: D3-02 selects Sheets.',
        'Scope: user-requested additional Sheets route. Dependencies: D3-02 Excel route remains complete; user now requests all alternatives.')
    block = block.replace('Scope: Sheets route.', 'Scope: user-requested additional Sheets route.')
    block = re.sub(r'\| not_applicable \| Excel selected; see \[route decision\]\(SPREADSHEET_ROUTE.md\)\. \|',
        '| not_started | Reopened2026-10-07: earlier exclusion was valid for Excel-only scope; user now requests this alternative too. |', block)
    block = block.replace('Handoff / exceptions:',
        'Prior scope: excluded2026-10-07 because Excel was chosen; reopened after explicit request to test all alternatives. Preserve completed Excel work.\n\nHandoff / exceptions:', 1)
    s = s[:match.start()] + block + s[match.end():]
    s = re.sub(rf'(?m)^(\| \[{task} — .*?\| .*? \| )not_applicable( \| )None( \|)$',
        r'\g<1>not_started\g<2>1\g<3>', s)
p.write_text(s, encoding='utf-8')
