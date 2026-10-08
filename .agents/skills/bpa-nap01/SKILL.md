---
name: bpa-nap01
description: Complete or resume BPA nap01 introduction and setup exercises, including first BPMN models, CMC quotes, a fictional Zoho lead, UiPath smoke robot and AI prompt checks.
---

# BPA nap01

Locate the checked-out BPA repository root. Read root `AGENTS.md`, `PROGRESS.md`, `AUTOMATION.md`, `nap01/README.md`, and current `nap01/nap01/index.html`. Root `course_skill_manifest.json` tracks source version; reread changed lessons before relying on this reference.

Read [references/tasks.md](references/tasks.md), then each listed lesson as its chapter begins. All five chapter outputs/checks are covered. Preserve Hungarian labels/assets; work only in outer `nap01/working`, `notes`, `deliverables`.

Resume verified work. Existing café and routine deliverables were reopened; the routine is a sample, not the user's actual habits. Consult `PROGRESS.md` for status.

For access blockers use `$bpa-course-access` and `AUTOMATION.md`. Account/key/installation alone does not complete an exercise. Keep secrets out of notes/artifacts.

Update progress at execution start. Record artifact or fictional record, observed verification and remaining limitation per chapter. Save `nap01/deliverables/README.md` with outputs/evidence; mark complete only when required interactions and mini-exercises are verified. Never fabricate watched videos or user privacy preferences.

## Required task progress

Before executing any task, read root `TASK_PROGRESS.md` and `nap01/notes/TASK_PROGRESS.md`. Claim the task and follow its ordered steps. Mark the first unfinished applicable step `in_progress` before acting; immediately record verified evidence or the exact blocker afterward, then update the next step. Do not advance past unfinished dependencies or count preparation as platform execution. Track mini-exercises/scenarios separately and justify alternative/optional exclusions. Add new tasks/steps before execution. Preserve other agents' active claims. At handoff, save the precise resume point and reconcile the tracker with root `PROGRESS.md`. This workflow is mandatory for this course.

## Portable checkout workflow

Read `harness/WORKFLOWS.md` and `SETUP.md` in the repository root. On a new installation run `python -m harness.cli init`. The versioned PROGRESS/TASK_PROGRESS files are the author's reference evidence. Use `.bpa/PROGRESS.md` and `.bpa/progress.json` for this user's current claims, ordered steps and evidence, and `.bpa/work/napXX/{working,notes,deliverables}` for new work. Use `python -m harness.cli step` to enforce claim-before-execution and prerequisite order. Never copy historical done status or access/entitlement to a new user.

Use `python -m harness.cli prepare PROJECT` for new UiPath working copies. Restore packages and validate each copy in Studio. Historical working scripts are reference authoring/verification tools; inspect their output paths before invoking and adapt writes to the local work area. Portal UI/robot execution is user-started only; never launch it or proxy restricted pages. Preserve all reference results and completed-run locks. Use your own service accounts and URLs; no transferred login sessions.

## Local-only lesson folders

The GitHub checkout excludes every root napXX folder. Import this user’s own ZIPs only through an explicit `$bpa-import-lessons` invocation before reading/executing their lessons. Missing local sources are a prerequisite, not completed work. Shared task acceptance templates are in `harness/task_templates.json`; do not require unpublished historical day trackers to initialize fresh local progress. After import and the user’s solve request, read the current lessons and start a source/import-specific revision plan. Reusable helpers are retained under `harness/course_tools/dayXX` (see its README); robot code is in `harness/project_templates`, but actual course assets are required locally. Old paths/evidence in reference notes describe the author’s local runs and do not imply those files are distributed or present on another laptop.
