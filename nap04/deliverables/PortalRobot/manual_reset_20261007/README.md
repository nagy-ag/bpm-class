# Manual first-row and isolated reset — verified 2026-10-07

The user operated a disposable **MANUAL RESET TEST** copy. The exact first source row was submitted manually as K-GY-4147; CSV(5) and replay CSV(7) verify all five fields. The green confirmation-screen new-record button cleared the form. The user then reset only this isolated copy: the list screenshot shows **20 sample + 0 own = 20 cases**, and the final form screenshot shows placeholders, default claim type and empty description.

- [Final reset list](final_reset_list_user.png) and [review](final_reset_review.json)
- [Final empty form](final_reset_empty_form_user.png) and [review](final_reset_empty_form_review.json)
- [Manual field verification](manual_export_verification.json), [replay verification](replay_export_verification.json), [new-record clearing](new_record_clear_review.json)
- [Original records reconciliation](original_records_reconciliation.json): original CSV(6) equals preserved CSV(4), 13 own records / 33 total retained.

Earlier diagnostic screenshots/reviews are preserved as historical evidence, including retained form values and the wrong-copy duplicate warning. Their pending fields are historical, superseded by the final reviews above. This package does not launch a portal or a robot. All portal browser actions were user-performed. Do not rerun the original completed batch or remove its reservations. The isolated source is in `nap04/working/manual_reset_20261007/manual_reset_portal.html`; it is excluded here to avoid confusing the two portal copies.
