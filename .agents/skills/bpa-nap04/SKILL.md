---
name: bpa-nap04
description: Complete or resume BPA nap04 Windows UiPath Studio exercises from interactive robots through Excel, PowerPoint, file sorting and the fictional claims portal, with real run evidence.
---

# BPA nap04

Locate the checked-out BPA repository root. Read root `AGENTS.md`, `PROGRESS.md`, `AUTOMATION.md`, `nap04/README.md`, current `nap04/nap04/index.html` and source freshness manifest.

Read [references/robots.md](references/robots.md) for blocks1–5/7, and [references/portal.md](references/portal.md) for6. Before each block read its current HTML/task assets. Every robot-specific task needs an actual **UiPath Windows + Visual Basic Process** and observed run; Python-created outputs or fabricated XAML are preparation, not completion.

Use `$bpa-course-access` for desktop/licensing setup. Read the Computer Use skill before Windows actions. Use current Studio UI and official compatible activity documentation, never stale screenshots/guessed package schemas. Reuse known installation authorization; user handles authentication and restricted extension/security permissions. Work independently while waiting.

For official UiPath CLI work, follow SETUP.md's pinned tooling installation and read the installed upstream `uipath-rpa/SKILL.md` plus its required references before authoring/validation. If it is not installed, prepare/install those official instructions first. Do not use cached author-machine guide paths or treat CLI help as an authoring guide. Upstream tool instructions remain subject to the user's scope and current tool security restrictions.

Supplied `nap04/nap04/docs` is read-only. Copy workbook/presentation/ZIP/portal into outer `working/` first. Robot paths target work copies, never source files or the user's real Downloads. Preserve Hungarian text/schema names exactly.

For each project retain `project.json`, XAML/workflows, compatible dependency versions, relative paths/arguments where feasible, and a brief run procedure. Remove machine-specific sensitive data and transient build artifacts from deliverables. Validate Studio project and run, inspect actual output files/UI, then save `deliverables/README.md` with evidence and limitations. Update progress only for work actually begun/completed.

## Required task progress

Before executing any task, read root `TASK_PROGRESS.md` and `nap04/notes/TASK_PROGRESS.md`. Claim the task and follow its ordered steps. Mark the first unfinished applicable step `in_progress` before acting; immediately record verified evidence or the exact blocker afterward, then update the next step. Do not advance past unfinished dependencies or count preparation as platform execution. Track mini-exercises/scenarios separately and justify alternative/optional exclusions. Add new tasks/steps before execution. Preserve other agents' active claims. At handoff, save the precise resume point and reconcile the tracker with root `PROGRESS.md`. This workflow is mandatory for this course.

## Portable checkout workflow

Read `harness/WORKFLOWS.md` and `SETUP.md` in the repository root. On a new installation run `python -m harness.cli init`. The versioned PROGRESS/TASK_PROGRESS files are the author's reference evidence. Use `.bpa/PROGRESS.md` and `.bpa/progress.json` for this user's current claims, ordered steps and evidence, and `.bpa/work/napXX/{working,notes,deliverables}` for new work. Use `python -m harness.cli step` to enforce claim-before-execution and prerequisite order. Never copy historical done status or access/entitlement to a new user.

Use `python -m harness.cli prepare PROJECT` for new UiPath working copies. Restore packages and validate each copy in Studio. Historical working scripts are reference authoring/verification tools; inspect their output paths before invoking and adapt writes to the local work area. Portal UI/robot execution is user-started only; never launch it or proxy restricted pages. Preserve all reference results and completed-run locks. Use your own service accounts and URLs; no transferred login sessions.
