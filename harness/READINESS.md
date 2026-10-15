# Testing updated lesson capabilities

Coverage is assessed per current lesson main task, mini-exercise and selected platform. A passing probe or the harness unit-test count does not mean every task type ran in its required application. In particular, Windows Workbook runs do not establish Cross-platform PDF/email/browser execution, native Power Query, or native Excel/PowerPoint chart insertion. Preserve dated native evidence separately from current local checks and explicitly record excluded alternatives and user-started portal steps.

For actual project-aware robot validation/build/run, use the [official CLI launcher](UIPATH_CLI.md). The user accepted this route on 2026-10-15; it avoids the MCP argument-context defect without changing the vendor installation or MCP configuration.

`course_tools/readiness_updated.py` checks the imported nap01/nap03/nap07/nap08 requirements on isolated copies. It preserves nested lesson sources, does not start robots or browsers, and does not mark coursework complete. JSON/CSV files are diagnostics rather than assignment submissions. Native platform evidence must be recorded separately.

Use Python with `lxml`, `openpyxl`, `python-pptx`, `pypdf` and `pdfplumber` installed. On Codex desktop, use the Python path returned by `load_workspace_dependencies`; no new dependency installation was needed for the original run.

From the checkout root, choose a **fresh output directory under `.bpa`** for each complete replay:

```powershell
python -m harness.course_tools.readiness_updated local03 --out .bpa/readiness-replay
python -m harness.course_tools.readiness_updated local07 --out .bpa/readiness-replay
python -m harness.course_tools.readiness_updated pdf --out .bpa/readiness-replay
python -m harness.course_tools.readiness_updated email --out .bpa/readiness-replay
python -m harness.course_tools.readiness_updated web --out .bpa/readiness-replay
python -m harness.course_tools.readiness_updated errors --out .bpa/readiness-replay
```

The `errors` phase consumes the `pdf` phase's recorded extraction directory. Sorting and email moves affect isolated copies only; existing diagnostic CSVs are not overwritten. Portal and webshop HTML are passively parsed, never executed or served through a workaround.

The email probe logs lowercase normalized subjects, matching the lesson's `targy` value. Its ten-file decision mapping is checked independently of casing; CSV diagnostics still do not prove a UiPath-generated Excel log.

`live` is a separate explicit service check using the canonical `day03/bpa_access.py` helper and ignored root credential store. It fetches BTC/ETH/SOL quotes and creates, reads, updates and deletes one uniquely tagged disposable fictional CRM lead with email/workflow triggers disabled. Run it only within authorized fictional-course testing. It checkpoints uncertain write/cleanup state in `crm.json`; inspect/reconcile that file before any retry. Never reuse a previous live output directory or print credential values.

`verify-excel-robot` starts no robot. It checks previously captured CLI transcripts (`uipath-run-main.json`, `uipath-run-150000.json`), the two actual workbooks under `.bpa/projects/ExcelRobot/output`, byte identity with current nap07 input, exact row-by-row classifications, and separately captured native Excel evidence. The transcript files contain log lines followed by a JSON envelope. Its top-level `robot_execution=false` describes the verifier itself; the results explicitly identify the previously observed runs and their execution transport.

For actual robots, first use `python -m harness.cli prepare ExcelRobot`, then follow the relevant UiPath skill's validation/build/run gates and preserve existing outputs. The 2026-10-15 assessment verified MCP tool installation/build and direct official CLI validation/two runtime runs. MCP validation/run ignored `--project-dir` in that environment; do not label the direct CLI runs as MCP runtime success. See the local dated report for exact evidence and limits.

These probes are pinned to the inspected supplied data. A changed lesson must first be read and reviewed; an assertion mismatch is a reason to inspect expectations and source provenance, not edit teacher files or weaken checks automatically.
