# Shared course code, local course material

Root `napXX/` folders are excluded from GitHub. Reusable authored Python/PowerShell helpers and tests formerly inside those folders are retained here under `day01` through `day04`. Robot code templates are in `harness/project_templates`; current lesson assets must be imported locally. No lesson bundle, completed workbook, deck, portal state, run log or teacher screenshot is required by code-only CI.

Portable entrypoints (from checkout root):

```powershell
python harness/course_tools/day03/bpa_access.py check
python harness/course_tools/day03/fetch_cmc_power_query.py --solana
python harness/course_tools/day03/build_course_notebook.py
python harness/course_tools/day03/verify_cloud_notebook_download.py DOWNLOADED.ipynb
python harness/course_tools/day04/setup_2026-10-06/verify_portal_run.py --help
python harness/course_tools/day04/setup_2026-10-06/verify_portal_batch.py --help
```

API helpers read only this user's root `.env.local` and never print credentials. Notebook generation is offline, writes to `.bpa/work/nap03/working/API_automation`, and does not execute cells. Its download verifier accepts `--reference` for an explicitly chosen local notebook. Actual cloud execution remains separate.

The other retained scripts are historical authoring/reconciliation/verifier implementations, not automatic setup commands. They may refer to original local day paths, observed case IDs, old evidence or a specific platform/runtime. Read them and parameterize/adapt inputs/outputs for current requirements before running. Do not replay historical account writes, portal operations, batch enablement or package cleanup. Live tools still require the currently exposed capability and its applicable skill; no archived helper bypasses those limits. Local originals remain preserved under the ignored day folders.

Offline API and portal regression suites run directly from these code directories and create synthetic fixtures at runtime. `harness/tests/fixtures.py` creates the minimal synthetic Office/input files used to check project preparation. Those fixtures are not actual coursework or native-app execution evidence.
