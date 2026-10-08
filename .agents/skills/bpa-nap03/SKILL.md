---
name: bpa-nap03
description: Complete or resume BPA nap03 API, Excel or Sheets, manual Zoho CRM, Colab lead creation and conditional CMC-to-Zoho exercises, using the course's EU credential helpers.
---

# BPA nap03

If using the official UiPath CLI for the CMC auto-refresh project, follow SETUP.md's pinned optional tooling installation and read its installed upstream uipath-rpa skill and required references before authoring/validation. The tool cache is not redistributed; do not use author-machine cache paths. Native run evidence remains required.

Locate BPA (current installation `<repository-root>`); read root `AGENTS.md`, `PROGRESS.md`, `AUTOMATION.md`, `nap03/README.md` and current `nap03/nap03/index.html`. Check root `course_skill_manifest.json` before using cached requirements.

Read [references/tasks.md](references/tasks.md) and the current page/supplied script for the selected block. It covers all six blocks and both spreadsheet paths. Excel **or** Sheets satisfies the quote-table choice; don't force both unless requested. Colab is explicitly part of the API lesson; a local Python equivalent may prepare/debug the solution but is separate from completing its Colab interaction.

Use `$bpa-course-access` for prerequisites, then reuse `harness/course_tools/day03/bpa_access.py` and `zoho_tokens.ps1`. Do not fork credential infrastructure or expose secrets from `.env.local`. Read API signatures before importing. Preserve nested source scripts; adapt working copies to safe credential/header handling.

Work in outer `nap03/working`, `notes`, `deliverables`, preserving Hungarian labels and fictional example identities. Check existing records/evidence before mutations. API helper refreshes tokens and retries reads only; uncertain writes require readback before retry. No real records, emails or automatic workflow triggers.

Update progress at execution start. Save runnable credential-free notebook/scripts, the chosen refreshable spreadsheet, secret-free quote/CRM/branch evidence and `deliverables/README.md`. Report platform execution and local logic validation separately; mark complete only after selected spreadsheet path, manual CRM, Colab/API and both chain branches actually satisfy their checks.

## Required task progress

Before executing any task, read root `TASK_PROGRESS.md` and `nap03/notes/TASK_PROGRESS.md`. Claim the task and follow its ordered steps. Mark the first unfinished applicable step `in_progress` before acting; immediately record verified evidence or the exact blocker afterward, then update the next step. Do not advance past unfinished dependencies or count preparation as platform execution. Track mini-exercises/scenarios separately and justify alternative/optional exclusions. Add new tasks/steps before execution. Preserve other agents' active claims. At handoff, save the precise resume point and reconcile the tracker with root `PROGRESS.md`. This workflow is mandatory for this course.

## Portable checkout workflow

Read `harness/WORKFLOWS.md` and `SETUP.md` in the repository root. On a new installation run `python -m harness.cli init`. The versioned PROGRESS/TASK_PROGRESS files are the author's reference evidence. Use `.bpa/PROGRESS.md` and `.bpa/progress.json` for this user's current claims, ordered steps and evidence, and `.bpa/work/napXX/{working,notes,deliverables}` for new work. Use `python -m harness.cli step` to enforce claim-before-execution and prerequisite order. Never copy historical done status or access/entitlement to a new user.

Use `python -m harness.cli prepare PROJECT` for new UiPath working copies. Restore packages and validate each copy in Studio. Historical working scripts are reference authoring/verification tools; inspect their output paths before invoking and adapt writes to the local work area. Portal UI/robot execution is user-started only; never launch it or proxy restricted pages. Preserve all reference results and completed-run locks. Use your own service accounts and URLs; no transferred login sessions.

## Local-only lesson folders

The GitHub checkout excludes every root napXX folder. Import this user’s own ZIPs only through an explicit `$bpa-import-lessons` invocation before reading/executing their lessons. Missing local sources are a prerequisite, not completed work. Shared task acceptance templates are in `harness/task_templates.json`; do not require unpublished historical day trackers to initialize fresh local progress. After import and the user’s solve request, read the current lessons and start a source/import-specific revision plan. Reusable helpers are retained under `harness/course_tools/dayXX` (see its README); robot code is in `harness/project_templates`, but actual course assets are required locally. Old paths/evidence in reference notes describe the author’s local runs and do not imply those files are distributed or present on another laptop.
