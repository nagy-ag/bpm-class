# Project-aware UiPath validation and execution

The user accepted official CLI execution as an alternative to the UiPath MCP project-folder defect on 2026-10-15. Use this route for BPA robots. The official installation and Codex MCP configuration remain unchanged; this does not repair or claim success for MCP validation/run.

`python -m harness.course_tools.uipath_cli` invokes the installed official `@uipath/cli` entry point through Node. Every operation gets its own real process arguments and working directory. Validation/run receive an absolute `--project-dir` and workflow path; build receives its project directory as a positional argument. Paths with spaces are passed as arguments without a shell. The launcher contains no installation or credential-reading code; authentication remains with the official CLI.

Prepare a fresh project through the harness/current revision workflow first. From the checkout root, substitute that project's folder and a fresh evidence directory for each command:

```powershell
python -m harness.course_tools.uipath_cli validate --project '.bpa/projects/ExcelRobot' --file Main.xaml --evidence .bpa/cli-check/validate-main
python -m harness.course_tools.uipath_cli validate --project '.bpa/projects/ExcelRobot' --file Classify_150000.xaml --evidence .bpa/cli-check/validate-variant
python -m harness.course_tools.uipath_cli build --project '.bpa/projects/ExcelRobot' --evidence .bpa/cli-check/build
python -m harness.course_tools.uipath_cli run --project '.bpa/projects/ExcelRobot' --file Main.xaml --skip-build --evidence .bpa/cli-check/run-main
python -m harness.course_tools.uipath_cli run --project '.bpa/projects/ExcelRobot' --file Classify_150000.xaml --skip-build --evidence .bpa/cli-check/run-variant
```

These example output/evidence locations must be fresh. Earlier completed robot outputs are preserved; the Excel workflows deliberately reject overwriting them. Do not remove locks or outputs to force a rerun. A failed or uncertain run is never retried automatically. Inspect the recorded state before choosing a new work copy or resuming.

`--skip-build` is appropriate only after a successful build of unchanged files. Omit it after edits. The default tool timeout is 120 seconds; `--timeout` sets a positive value in seconds. Workflow arguments are not supported by this minimal launcher; use the official CLI directly when they are required.

Each new evidence directory contains `invocation.json`, byte-exact `stdout.log`, `stderr.log`, and a parsed `result.json`. Native packager warnings can use a Windows code page; original bytes are retained even if console display has replacement characters. Existing evidence directories are refused before any command executes. Successful validation requires the known no-diagnostics response, build requires `Data.Success=true`, and run checks the appropriate Helm or Desktop verdict. Unknown response shapes fail verification so they can be reviewed rather than silently accepted. Workflow outputs must still be checked against assignment requirements.

On the 2026-10-15 test, both unchanged Excel workflows validated, the project built, and both actual runs completed through this launcher in a project folder containing spaces. Independent readback verified all 12 rows/fields and 6/3 highlighted customers at the two thresholds. Local evidence is in `.bpa/uipath-project-cli-20261015/REPORT.md`. Earlier readiness evidence remains under its original path.

The course's portal constraint still applies: agents may author/check offline, but the user starts live portal runs. This launcher does not grant course completion, submission, account permissions or portal-operation authorization.

Official command references: [RPA project context](https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/uip-rpa), [build](https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/uip-rpa-build), [run/debug verdicts and options](https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/uip-rpa-run-debug).
