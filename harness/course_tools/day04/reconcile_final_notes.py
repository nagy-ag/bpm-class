"""Reconcile current summary and repair historical evidence by bounded task block."""
import json
import re
import shutil
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
AUDIT = ROOT / 'nap04/working/final_audit_20261007'
tracker = ROOT / 'TASK_PROGRESS.md'
backup = AUDIT / 'TASK_PROGRESS_before_evidence_repair.md'
if not backup.exists():
    shutil.copy2(tracker, backup)
s = tracker.read_text(encoding='utf-8-sig')
evidence = {
    'setup-04': ['Actual user-started trial evidence preserved under portal_runs/20261007_090716_e48528aa65244dd6943e7c5de428f202: verification.json passes19checks; caseK-GY-4147/TR-402318/logs/snapshot/screenshots reviewed. No agent portal action.', 'Actual CSV(2) post_export_reconciliation.json verifies3prior records unchanged, exactly1added,4own total, all5fields exact and unique case IDs. Reservation retained.'],
    'setup-03': ['Current lesson/project and official authoring guidance reviewed before offline preparation. Preserved existing Main/Workbook_Roundtrip/input hashes; portal_logging_preparation_verified.json records safe offline authoring boundary.', 'Prepared actual UIA activities, per-run snapshots/CSV/screenshot/readback logging and False premature-run guard. Actual file-only logger ran7seconds,3events/Hungarian+quote roundtrip passed; nineTODO targets and five expected missing-target build errors documented. No portal execution at preparation stage.'],
    'setup-02': ['Existing Windows/VB BPA_Setup_Smoke and copied input reviewed; Main, Workbook_Roundtrip and user Brave attachment preserved. See setup README and portal_input_preview_verified.json.', 'Native Studio Save As/configuration prepared Portal_Input_Preview.xaml, ReadRange A1:F2 headers and WriteRange VerifiedData;0browser actions. Subsequent actual7second Run File verified all populated first-row values.'],
    'setup-01': ['Native Office_Readiness.xlsx edited20to28 plus22; formula recalculated42to50, saved/closed/reopened and cache/formula verified. See nap04/working/setup_2026-10-06/README.md.', 'Native local Power Query imported refresh_input.csv2rows then refreshed revision2 Alpha15/Beta25/Gamma30,3rows. Saved table/Mashup connection verified; excel_refresh_passed.png preserved.'],
    'access-01': ['Approved local credential loaded programmatically without displaying values; canonical helper and ignored.env.local documented in AUTOMATION.md.', 'Actual live BTC/ETH/SOL EUR checks passed finite positive-value validation; readiness_2026-10-06/quotes.json and READINESS.md preserve public response/evidence.'],
    'access-02': ['User saved authorized fresh Self Client grant in ignored.env.local; historical live exchange reported in AUTOMATION.md/PROGRESS.md. No grant value recorded here.', 'Live EU OAuth exchange saved generated tokens and cleared consumed grant; subsequent forced renewal/CRM reads passed. Canonical bpa_access.py/zoho_tokens.ps1 and readiness crm_test.json retained.'],
    'access-03': ['User signed in privately after timeout; no Moodle password/cookies read or stored. Dated READINESS.md and PROGRESS.md preserve the handoff.', 'Actual authenticated course9525 and nap04 lesson navigation passed after private sign-in. Historical session evidence only; does not promise current or unattended sign-in.'],
    'access-04': ['User-approved BPAcourseautomation Community organization created; Community Plan/oneProStudio entitlement and later native Studio Community/Pro license recorded in AUTOMATION.md and setup README.', 'Official UiPath installer downloaded, UiPath signature validated, and user explicitly authorized free user-mode Studio/Robot install/license acceptance. Historical installation evidence recorded in PROGRESS.md; actual installed26.0.203start screen and later runs verified.'],
    'access-05': ['Authenticated Colab home observed without reading credentials; access inventory and dated readiness evidence retained.', 'Actual connected Python3 BPA_Readiness_Check smoke ran greeting/arithmetic/strict-threshold assertions; readiness_2026-10-06/colab_run.png preserved. Actual course API notebook executions tracked separately under nap03.'],
    'verify-01': ['Current223source files and course capability map reviewed; source manifest/five skills/task trackers and READINESS.md identify required browser/API/Office/UiPath/file/model capabilities.', 'Actual CMC positive finite EUR quotes, EU CRM module reads and forced OAuth refresh passed without displaying credentials; nap03/working/readiness_2026-10-06/quotes.json, crm_test.json and READINESS.md preserve the evidence.'],
}
for task, entries in evidence.items():
    pattern = rf'(^### {re.escape(task)} — [^\n]*\n.*?)(?=^### |\Z)'
    m = re.search(pattern, s, re.M | re.S)
    assert m, task
    block = m.group(1)
    for step, ev in enumerate(entries, 1):
        row = rf'(?m)^(\| {step} \| .*? \| done \| ).*( \|)$'
        block, count = re.subn(row, lambda x: x.group(1) + ev + x.group(2), block, count=1)
        assert count == 1
    s = s[:m.start()] + block + s[m.end():]
tracker.write_text(s, encoding='utf-8')

p = ROOT / 'PROGRESS.md'
s = p.read_text(encoding='utf-8-sig')
end = s.find('\nExpanded verification update:')
assert end > 0
latest = '''## 2026-10-07 final automation verification

All supplied nap01–nap04 required exercises and selected alternatives are verified, including the exact isolated manual/reset portal exercise and final empty form. Nap04 final handoff audit reviewed5Windows/VBprojects,12actual prior run outcomes and306delivery files including decompressed archives. A clean additive archive byte-verifies324files, excluding transient caches/Office locks while retaining target resources and completed-run guards. [Final handoff](nap04/deliverables/HANDOFF.md), [archive](nap04/deliverables/BPA_nap04_verified_projects_20261007.zip), [audit](nap04/working/final_audit_20261007/handoff_verification.json).

The original portal remains13own/33total with all ten source policies exact and existing records/reservations preserved; it is the recorded cumulative adaptation, not a clean30-case batch. Separate MANUAL RESET TEST ended20sample/0own and an empty form; user screenshots and CSV(5)/(7) verify exact first-row manual entry and reset. [Evidence](nap04/deliverables/PortalRobot/manual_reset_20261007/README.md). No agent portal action or robot rerun occurred.

Expanded tests passed: native BIMP exports/reimport and both heat maps65checks; Colab clean download51checks; Sheets BTC/ETH/SOL and actual hourly execution (practice trigger removed); two automatic canonical CMC fetch→native Excel Power Query refresh/save runs. Direct credential-from-env CMC Power Query failed Formula.Firewall with privacy retained, so the approved Python+Power Query adaptation is used. Website re-login is excluded by the user. Later unpublished assignments and graded submissions are outside this verified scope.

Six nap02 local result pages: user reports all six opened and seem fine; substantive content/assets are being checked offline against saved evidence, with direct agent browser inspection unavailable for local pages. Older checkpoints below are historical and do not describe current completion.
'''
s = latest + s[end:]
s = re.sub(r'(?m)^\| \[nap01\].*$', '| [nap01](nap01/README.md) | Introduction and setup | Completed |7/7tasks verified; [index](nap01/deliverables/README.md). |', s)
s = re.sub(r'(?m)^\| \[nap03\].*$', '| [nap03](nap03/README.md) | APIs, spreadsheets, and CRM | Completed |17tracked course tasks verified, plus native download and automatic refresh; [index](nap03/deliverables/README.md). Credential-safe Python+Power Query adaptation retained. |', s)
s = re.sub(r'(?m)^\| \[nap04\].*$', '| [nap04](nap04/README.md) | UiPath automation | Completed |15/15required tasks verified; [handoff](nap04/deliverables/HANDOFF.md). Original33case cumulative batch and isolated manual/reset evidence preserved. |', s)
p.write_text(s, encoding='utf-8')
save = {'date': '2026-10-07', 'repaired_root_task_blocks': list(evidence), 'method': 'Anchored task blocks, first two evidence cells only; statuses unchanged; backed up previous tracker.', 'cause': 'Old updater matched from a shared ### task to end-of-file and replaced repeated step numbers in later tasks.', 'helper_fix': 'Anchor task heading; stop at next heading/anchor; limit row substitution to1.', 'root_summary_reconciled': True}
(AUDIT / 'tracking_reconciliation.json').write_text(json.dumps(save, indent=2), encoding='utf-8')
print('Reconciled current summary and10historical root evidence blocks; original tracker preserved.')
