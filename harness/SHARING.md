# Public/private boundary

Tracked: seven repository skills, ordered task acceptance templates, authored Python/PowerShell helpers, regression tests/verifiers, UiPath code templates/target selectors, setup/workflow documentation and credential-free harness verification summaries. Code-only CI creates synthetic test assets. Historical root reports retain their dates/scope; their referenced local day artifacts are not distributed. Author-machine paths in historical helpers describe provenance and must be adapted before use.

Ignored: every root napXX folder, including supplied sources, lesson assets, completed coursework and day evidence; root ZIP downloads/lesson-downloads inbox; .env.local and variants; private .bpa state/work; .venv/node_modules; compiled caches and Studio build state. Importing lessons never opts their folders into Git. Original local files remain intact. Reusable code formerly inside day folders is preserved under harness/course_tools; authored robot code is in harness/project_templates, without teacher Office inputs/completed outputs or captured run screenshots.

Per-user evidence/account screenshots remain private. New public evidence requires review. Root imported-source provenance records contain hashes/file names and unfinished-version context, not supplied file contents or transferable completion. Another laptop imports its own ZIPs, uses its own accounts and keeps fresh progress in .bpa.

Supplied material ownership remains with its author; no blanket open-source license is applied to those files. UiPath/Office installers, activation, user plugin caches, session data and account credentials are not redistributed.

Before publication, stage intended files, then run `python harness/audit_share.py --staged`. It inspects staged bytes, nested ZIP/Office archives and known local secret values without printing values. It rejects root napXX folders even if force-added, as well as forbidden runtime/credential paths. Existing published day folders are removed by a normal deletion commit; earlier Git history is not rewritten by this workflow. This technical check does not prove that a future screenshot contains no private data; review new screenshots before staging.

Own new-user evidence remains local until separately reviewed for sharing. Never use Git history as a secret store. If a key is published, revoke/rotate it; removing it only from the latest tree is insufficient.
