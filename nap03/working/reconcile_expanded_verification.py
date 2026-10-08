"""Reconcile current verified evidence; preserve older checkpoint history."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
p = ROOT/'nap03/working/sheets_preparation_checkpoint.json'
c = json.loads(p.read_text('utf-8'))
c.update(status='manual_mini_hourly_verified_trigger_removed',source_executed=True,
         trigger_created=True,trigger_actual_execution_verified=True,trigger_removed_verified=True,
         current_trigger_count=0,next='Sheets route complete; see deliverables/Sheets_automation/README.md')
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')

p = ROOT/'PROGRESS.md'
s = p.read_text('utf-8')
start = s.index('Latest expanded verification:')
end = s.index('\n\n', start)
s = s[:start] + ('Latest expanded verification2026-10-07: native BIMP exports/reimport and both heat maps passed65checks; clean Colab download passed51checks. Additional Google Sheets BTC/ETH refresh, SOL and actual hourly Time-Driven execution all passed; user removed the practice trigger and fresh inventory shows0. Two actual canonical CMC fetch → native Excel Power Query refresh/save runs passed without intermediate user input, with changed prices/advanced provider and fetched timestamps. [Sheets evidence](nap03/deliverables/Sheets_automation/README.md), [automatic Excel evidence](nap03/deliverables/CMC_auto_refresh/README.md). Final nap03 handoff scan passed59files. Six local result views and exact portal manual/reset user actions remain pending; a separate MANUAL RESET TEST portal copy is prepared offline and awaits20case baseline confirmation. Original33-case batch/locks preserved. Nap04 remains13/15required; final sign-off depends on D4-11. No website re-login or graded submission attempted. Older checkpoints below are historical.') + s[end:]
p.write_text(s,encoding='utf-8')

p = ROOT/'nap03/deliverables/README.md'
s = p.read_text('utf-8')
note = ('Expanded verification2026-10-07 complete: [native Sheets manual/SOL/hourly route](Sheets_automation/README.md) and [automatic CMC-to-native-Excel refresh](CMC_auto_refresh/README.md) both verified. Practice Google trigger removed; zero remain. Two finite local Excel cycles changed prices/provider timestamps and saved three correct rows each; no persistent local schedule. [Final59-file handoff check](handoff_verification.json) passed. Earlier scope/checkpoints below are historical.\n\n')
p.write_text(note+s,encoding='utf-8')

p = ROOT/'nap04/notes/TASK_PROGRESS.md'
s = p.read_text('utf-8')
marker = '<a id="d4-12"></a>'
addition = ('D4-11 resume2026-10-07: separate [manual reset copy](../working/manual_reset_20261007/manual_reset_portal.html), dedicated storage key and visible MANUAL RESET TEST badge prepared/verified offline under D4-P02. User asked to open it in Brave and confirm20cases before any entry. No live baseline/manual/reset evidence yet. Preserve original33cases and all locks. Follow staged [handoff](../working/manual_reset_20261007/HANDOFF.md); do not rerun the already completed robot batch.\n\n')
s = s.replace(marker,addition+marker,1)
p.write_text(s,encoding='utf-8')
print('Latest progress, evidence indexes and exact portal resume point reconciled')
