---
name: bpa-course-access
description: Prepare or resume BPA course access, route supplied days and newly imported lessons, and check CMC, Zoho EU, Moodle, Office and UiPath prerequisites. Use for course setup or cross-day automation requests.
---

# BPA course access and routing

Locate BPA from the current workspace. Resolve the repository root from the current workspace; verify `AGENTS.md` and `harness/cli.py`. Read root `AGENTS.md`, `PROGRESS.md`, `AUTOMATION.md` and `SKILLS.md`. Current user and workspace instructions take precedence over this skill.

| Day | Skill | Outcome |
| --- | --- | --- |
| nap01 | `$bpa-nap01` | BPMN, accounts and tool setup |
| nap02 | `$bpa-nap02` | Models, seven simulation scenarios and repairs |
| nap03 | `$bpa-nap03` | Refreshable quotes, manual CRM, API writes and conditional chain |
| nap04 | `$bpa-nap04` | Actual Studio projects, robot runs and verified outputs |

Follow course order by default. Targeted later-day review need not rerun completed days. Read current lessons: root `course_skill_manifest.json` records the version used for these skills. If hashes differ, inspect new requirements and update affected guidance before using cached parameters.

Read [references/access.md](references/access.md) when access is missing or setup is requested. Install only prerequisites for the selected exercise path; reuse existing accounts.

Use `python <this-skill>/scripts/inspect_course.py --root <BPA-root> --day nap03` for source drift, or add `--lesson pages/05_zoho_api.html` to read the current supplied lesson as UTF-8 text. The helper reads only the source manifest and allowed lesson bundles; it never opens `.env.local`. Omit `--day` to inspect all installed days. A newly imported day has no reviewed runbook until its current lessons have been read and guidance prepared.

Check `python -m harness.cli lesson-status` before executing an updated day. Importing does not solve its tasks: only a user request to solve that update permits `start-revision` with a current-source task plan, preserving old completion and emitting separate revision paths. Follow `harness/LESSON_UPDATES.md`. Do not invoke either explicit-only maintenance skill merely to perform this check or because a ZIP exists. For a future day without a dedicated skill, use current supplied requirements and the shared ordered progress contract; never fabricate a cached runbook.

Maintain `PROGRESS.md` when execution begins/finishes. For blocked chapters distinguish prepared, actually executed, verified, and exact remaining user action; continue independent work. Use outer day `working/`, `notes/`, `deliverables/`; nested supplied bundles remain read-only.

The user delegated course exercises and fictional course CRM records. Check current authorization boundaries: this does not authorize real records, messages, purchases or final graded submissions. Prepare reviewable artifacts before asking for a particular graded submission.

Before marking a day complete, require its outputs and observed checks, and save an artifact index with evidence. Mocks, generated files and passing helper tests do not prove a browser, cloud script or UiPath robot ran.

## Required task progress

Before executing any task, read root `TASK_PROGRESS.md` and the relevant `napXX/notes/TASK_PROGRESS.md`. Claim the task and follow its ordered steps. Mark the first unfinished applicable step `in_progress` before acting; immediately record verified evidence or the exact blocker afterward, then update the next step. Do not advance past unfinished dependencies or count preparation as platform execution. Track mini-exercises/scenarios separately and justify alternative/optional exclusions. Add new tasks/steps before execution. Preserve other agents' active claims. At handoff, save the precise resume point and reconcile the tracker with root `PROGRESS.md`. This workflow is mandatory for this course.

## Portable checkout workflow

Read `harness/WORKFLOWS.md` and `SETUP.md` in the repository root. On a new installation run `python -m harness.cli init`. The versioned PROGRESS/TASK_PROGRESS files are the author's reference evidence. Use `.bpa/PROGRESS.md` and `.bpa/progress.json` for this user's current claims, ordered steps and evidence, and `.bpa/work/napXX/{working,notes,deliverables}` for new work. Use `python -m harness.cli step` to enforce claim-before-execution and prerequisite order. Never copy historical done status or access/entitlement to a new user.

Use `python -m harness.cli prepare PROJECT` for new UiPath working copies. Restore packages and validate each copy in Studio. Historical working scripts are reference authoring/verification tools; inspect their output paths before invoking and adapt writes to the local work area. Portal UI/robot execution is user-started only; never launch it or proxy restricted pages. Preserve all reference results and completed-run locks. Use your own service accounts and URLs; no transferred login sessions.

## Local-only lesson folders

The GitHub checkout excludes every root napXX folder. Import this user’s own ZIPs only through an explicit `$bpa-import-lessons` invocation before reading/executing their lessons. Missing local sources are a prerequisite, not completed work. Shared task acceptance templates are in `harness/task_templates.json`; do not require unpublished historical day trackers to initialize fresh local progress. After import and the user’s solve request, read the current lessons and start a source/import-specific revision plan. Reusable helpers are retained under `harness/course_tools/dayXX` (see its README); robot code is in `harness/project_templates`, but actual course assets are required locally. Old paths/evidence in reference notes describe the author’s local runs and do not imply those files are distributed or present on another laptop.
