"""Preserve user-operated manual/reset evidence; never access the portal browser."""
import hashlib
import json
import shutil
from pathlib import Path

work = Path(__file__).resolve().parent
root = work.parents[2]
image = Path('C:/Users/nagya/AppData/Local/Temp/codex-clipboard-3a6ada29-0518-4701-94fa-7977ef56db9b.png')
shutil.copy2(image, work / 'final_reset_empty_form_user.png')
review = {
    'date': '2026-10-07',
    'evidence_source': 'User-supplied screenshot visually reviewed by assistant',
    'screenshot': 'final_reset_empty_form_user.png',
    'visible_badge': 'MANUAL RESET TEST',
    'visually_empty': True,
    'policy_placeholder': 'TR-123456',
    'date_placeholder': '2025-07-14',
    'amount_placeholder': 'pl. 2500',
    'claim_type': '- válassz -',
    'description_empty': True,
    'baseline_review': 'final_reset_review.json',
    'agent_portal_action': False,
    'acceptance': 'Manual exact first row, confirmation, new-record clearing, isolated reset and post-reset form verified. Original completed robot records preserved.',
}
(work / 'final_reset_empty_form_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding='utf-8')
target = root / 'nap04/deliverables/PortalRobot/manual_reset_20261007'
target.mkdir(parents=True, exist_ok=True)
names = [p for p in work.iterdir() if p.suffix in ('.json', '.png', '.csv', '.py') and p.name != Path(__file__).name]
manifest = []
for p in names:
    shutil.copy2(p, target / p.name)
    manifest.append({'file': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(target / 'evidence_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
(target / 'README.md').write_text('''# Manual first-row and isolated reset — verified 2026-10-07

The user operated a disposable **MANUAL RESET TEST** copy. The exact first source row was submitted manually as K-GY-4147; CSV(5) and replay CSV(7) verify all five fields. The green confirmation-screen new-record button cleared the form. The user then reset only this isolated copy: the list screenshot shows **20 sample + 0 own = 20 cases**, and the final form screenshot shows placeholders, default claim type and empty description.

- [Final reset list](final_reset_list_user.png) and [review](final_reset_review.json)
- [Final empty form](final_reset_empty_form_user.png) and [review](final_reset_empty_form_review.json)
- [Manual field verification](manual_export_verification.json), [replay verification](replay_export_verification.json), [new-record clearing](new_record_clear_review.json)
- [Original records reconciliation](original_records_reconciliation.json): original CSV(6) equals preserved CSV(4), 13 own records / 33 total retained.

Earlier diagnostic screenshots/reviews are preserved as historical evidence, including retained form values and the wrong-copy duplicate warning. Their pending fields are historical, superseded by the final reviews above. This package does not launch a portal or a robot. All portal browser actions were user-performed. Do not rerun the original completed batch or remove its reservations. The isolated source is in `nap04/working/manual_reset_20261007/manual_reset_portal.html`; it is excluded here to avoid confusing the two portal copies.
''', encoding='utf-8')
print(f'Preserved {len(manifest)} evidence files; final empty form reviewed.')
