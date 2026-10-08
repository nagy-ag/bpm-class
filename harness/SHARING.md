# Public/private boundary

Tracked: supplied lessons and assets; all five course skills; ordered task acceptance definitions; reusable scripts, regression tests and verifiers; fictional exercise inputs; BPMN/native BIMP exports; credential-free quote data; clean notebook/Apps Script source; UiPath workflows and captured target resources; safe reference run reports, screenshots and output workbooks/decks. Historical reports retain their original dates and scope. Author-machine paths in reference files are provenance, not executable defaults for a colleague.

Ignored: .env.local and variants, private fresh .bpa state/work, .venv/node_modules, compiled caches, Studio .local/.project build state, Office lock files, previous lesson-bundle backup ZIPs and obsolete machine-specific aggregate handoff ZIPs. Source course ZIP assets are tracked. Required Studio .objects/.screenshots are tracked.

Raw Zoho/Google/Colab account screenshots are individually excluded because they include personal account context. Their reusable tests and credential-free measured verification reports remain tracked. Exclusion does not erase original local evidence. Cloud account URLs/IDs in public textual reference evidence are replaced with explicit redaction markers; original private copies remain locally backed up. Redaction changes published bytes, not the recorded checks' scope. Hashes made before sharing refer to original local bytes.

Supplied material ownership remains with its author; no blanket open-source license is applied to those files. UiPath/Office installers, activation, user plugin caches, session data and account credentials are not redistributed.

Before publication, stage intended files, then run `python harness/audit_share.py --staged`. It inspects staged bytes, nested ZIP/Office archives and known local secret values without printing values. It also rejects forbidden runtime/credential paths. This technical check does not prove that a future screenshot contains no private data; review new screenshots before staging.

Own new-user evidence remains local until separately reviewed for sharing. Never use Git history as a secret store. If a key is published, revoke/rotate it; removing it only from the latest tree is insufficient.
