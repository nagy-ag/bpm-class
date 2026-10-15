# Workflow contract for every agent

Read root [AGENTS.md](../AGENTS.md), [TASK_PROGRESS.md](../TASK_PROGRESS.md), [SETUP.md](../SETUP.md), the selected repo skill and current supplied lesson. [SKILLS.md](../SKILLS.md) maps instruction ownership; this file owns portable execution paths and procedures. Source drift check:

```powershell
python .agents/skills/bpa-course-access/scripts/inspect_course.py --root .
```

For lesson maintenance, apply the invocation/source-replacement boundary in [AGENTS.md](../AGENTS.md) and the procedure in [LESSON_UPDATES.md](LESSON_UPDATES.md). Newly imported days use their current requirements and source-specific revision plans.

## Own progress and outputs

Run `python -m harness.cli init` once. It never overwrites credentials or existing local progress. Versioned trackers/results are reference evidence from the author's 2026-10-06/07 runs. They are not a colleague's completion. All applicable steps start pending in `.bpa/PROGRESS.md`; underlying state and append-only event records are `.bpa/progress.json` and `.bpa/events.jsonl`.

Every root napXX folder is local-only, including historical day trackers and outputs. Shared acceptance definitions are preserved in `harness/task_templates.json`; initialization does not require those excluded day files. Use current locally imported source requirements when planning revision tasks. Reusable authored helpers and tests are under `harness/course_tools/dayXX`; robot code templates are under `harness/project_templates`. Preparation stops before creating a partial copy if required local course inputs are missing. Source assets and completed native workbooks/decks are not copied into the shared harness.

Follow the mandatory execution sequence in root `TASK_PROGRESS.md`. The commands below implement that sequence for this user's local tracker.

```powershell
python -m harness.cli status
python -m harness.cli step D1-01 1 in_progress --owner colleague-chat --dependencies-checked --evidence "Read current lesson; prerequisites checked"
python -m harness.cli step D1-01 1 done --owner colleague-chat --evidence "Actual result and path to verification evidence"
```

Use the actual task ID shown by status. Evidence must be specific, not the example wording. A documented unchosen alternative still requires claiming its step before `not_applicable`. For new requirements, add a task and ordered acceptance steps to local progress before acting. Current tasks' requirements are preserved from the reviewed source; historical instructions about preserving original completed rows describe reference runs, not a fresh baseline. Re-read sources to set the new user's baseline.

Add new tasks with `python -m harness.cli add-task .bpa/new-task.json`. Its JSON contains `id`, `title`, `requirements`, `dependencies` and `steps` (ordered acceptance strings); duplicate IDs are rejected. Transfer ownership with `python -m harness.cli handoff TASK --owner OLD --to-owner NEW --evidence "Exact resume step and pending check"`. Prior evidence stays intact.

New drafts/notes/final files go under `.bpa/work/napXX/working`, `notes`, `deliverables`; fresh robots under `.bpa/projects`. Credentials remain in root `.env.local`. The root author trackers remain unchanged during a colleague's course execution. Export a reviewed credential-free deliverable only on that user's instruction. Local state is ignored because it can contain private accounts, URLs and run data. The harness tests, validators, reference fixtures and verification reports are tracked.

After source updates, preserve those earlier tasks/paths as history. Only on the user's explicit solve request, use `start-revision` with a task plan read from the current lessons. Follow emitted revision-specific work paths and task IDs. Stale task transitions are rejected; completion from an old source cannot count for an updated one. If an import conflicts with an active claim, its owner must stop execution and use `harness.cli release TASK --owner OWNER --evidence "Exact resume state; coordinated source update"` before replacement; all step/evidence history is preserved. Never release another agent's claim on its behalf.

## Access and execution

| Area | Execution and acceptance |
| --- | --- |
| Source lessons | Open nested index.html as static content. No server or test runtime needed for reading. |
| APIs | Canonical `harness/course_tools/day03/bpa_access.py`; credentials read from root .env.local and sent only to the matching service. Run `check` only after keys are supplied. Fictional course CRM records only; read back fields and reconcile ambiguous writes before retry. |
| Moodle/cloud UI | In-app browser first, authenticated user sessions. If expired, user signs in privately. Never store website passwords/cookies or promise unattended login. Each user supplies their own Google sheet/script/notebook URLs in .bpa/config.json. |
| Desktop UI | Use only computer tools actually exposed to this chat, read their current skill/policy first. A repository cannot install or grant a Codex capability. If unavailable, perform permitted offline/native integration work and request only the precise missing user action. |
| Office | Native activated Excel/PowerPoint; real calculation, query refresh, chart insertion, save and reopen. File parsing or mocks alone do not prove native behavior. |
| UiPath | `python -m harness.cli prepare PROJECT`; restore compatible packages and use the installed official `uipath-rpa/SKILL.md` plus its required references before authoring/validation. Installation is in SETUP.md. For the accepted project-aware CLI route read [UIPATH_CLI.md](UIPATH_CLI.md). Capture semantic validation/build/run verdicts and compare actual outputs with inputs. |
| CMC workbook | Verified route is Python fetch with .env.local → credential-free JSON → native Power Query. Direct CMC/header/env PQ route hit Formula.Firewall and is not claimed verified. Run configure-cmc.ps1 on the fresh auto-refresh copy before Studio; never embed a CMC key in a workbook. |
| Portal | User-started only. Offline authoring/logging/readback verification permitted. No agent browser/desktop/robot action on the restricted local page and no localhost proxy. |

## Portal: fresh baseline, then trial, then batch

Prepare PortalRobot offline. Its Main intentionally stops; historical batch is renamed REFERENCE_ONLY and its baseline guard is false. It must never be treated as ready for the colleague. Keep current source input's ten policy/type/date/amount/description values; blank output case IDs.

1. User opens the prepared portal, signs in privately and captures current application/fields/buttons in Studio. Preserve target resources. Author offline against those captured targets.
2. User exports own-record CSV and reports total case count. Reconcile every existing input policy and uncertain reservation before any write. The supplied page starts with 20 sample records; its CSV contains only own records.
3. Prepare trial for one unsubmitted row with durable policy reservation, before/filled/confirmation screenshots, events and input snapshot. User runs the trial and exports CSV. Verify all five fields plus case ID and total change.
4. Build a fresh batch from the current reconciled baseline. Skip only rows proven complete by this user's exported CSV; never reuse author's K-GY case IDs or historical skip assumptions. Keep guard false until baseline, unique pending rows and reservations are verified. No automatic submit retry.
5. User runs batch and exports CSV; use tracked `verify_portal_run.py` / `verify_portal_batch.py` (read --help, parameterize actual paths) to verify records/logs/screenshots. Reconcile original baseline, every new row and total. Preserve reservations on success or uncertainty.
6. For manual/reset practice use a separately isolated persistence key and backup exports; user confirms clear/reset and returns screenshot/count. Preserve cumulative exercise evidence.

## Verification retained in Git

`python harness/verify.py` runs offline regression suites for API safety, conditional/no-write logic, portal evidence handling and portable setup/progress/project preparation. It also checks all supplied hashes, required skills and workflow XML. `harness/audit_share.py` scans Git's staged/tracked files and recursively expanded archives for credentials. Neither test command signs in, changes CRM, runs robots, changes browser permissions or proves new-laptop entitlement. Actual platform acceptance is listed in SETUP.md.

For a download of the historical 19-cell notebook produced by `build_course_notebook.py`, run `python harness/course_tools/day03/verify_cloud_notebook_download.py PATH_TO_DOWNLOAD.ipynb`. It verifies that fixed 19-cell structure, cleared outputs and credential absence offline; it does not execute cells or prove a cloud run. A current-source notebook with a different chapter/cell plan requires its own acceptance checks rather than forcing the old chain into it.

Legacy scripts in napXX/working are preserved as authoring and verification evidence. Some contain historical paths/dates and package snapshots. Read before invoking, supply current inputs, adapt outputs to .bpa and never replay historical reconciliation/package scripts as setup. Use the portable entrypoints above first.
