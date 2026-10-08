---
name: bpa-nap02
description: Complete, review or resume BPA nap02 BPMN and BIMP exercises for the café, webshop, Meridian claims and Atlas warehouse, including all three model repairs.
---

# BPA nap02

Locate BPA (current installation `<repository-root>`); read root `AGENTS.md`, `PROGRESS.md`, `nap02/README.md`, current `nap02/nap02/index.html` and relevant lesson. Check source freshness against root `course_skill_manifest.json`.

Use [references/models.md](references/models.md) for blocks1–3/6 and [references/simulations.md](references/simulations.md) for4–5. Nested `docs/` is read-only; work in outer `working/`, final outputs in `deliverables/`.

This day already has verified work: inspect `nap02/deliverables/README.md` and notes first. Preserve measured scenarios and export/heat-map limitations. A stochastic rerun is new evidence, not the original measurement.

Use bpmn.io/BIMP in-app first. `https://bimp.cs.ut.ee/simulator/` needs no account/key. Use `$bpa-course-access` for actual blockers. Existing outer scripts/QBP resources may preserve models/parameters; inspect before reuse. No runtime needed for static lessons.

Validate semantics plus visible editor import. Simulations require observed BIMP results for requested scenarios, not capacity estimates or a homemade substitute. Save models, parameters, measured CSV/tables, analysis and provenance; note unavailable downloads/views. Update `PROGRESS.md` for execution actually begun/completed.

## Required task progress

Before executing any task, read root `TASK_PROGRESS.md` and `nap02/notes/TASK_PROGRESS.md`. Claim the task and follow its ordered steps. Mark the first unfinished applicable step `in_progress` before acting; immediately record verified evidence or the exact blocker afterward, then update the next step. Do not advance past unfinished dependencies or count preparation as platform execution. Track mini-exercises/scenarios separately and justify alternative/optional exclusions. Add new tasks/steps before execution. Preserve other agents' active claims. At handoff, save the precise resume point and reconcile the tracker with root `PROGRESS.md`. This workflow is mandatory for this course.

## Portable checkout workflow

Read `harness/WORKFLOWS.md` and `SETUP.md` in the repository root. On a new installation run `python -m harness.cli init`. The versioned PROGRESS/TASK_PROGRESS files are the author's reference evidence. Use `.bpa/PROGRESS.md` and `.bpa/progress.json` for this user's current claims, ordered steps and evidence, and `.bpa/work/napXX/{working,notes,deliverables}` for new work. Use `python -m harness.cli step` to enforce claim-before-execution and prerequisite order. Never copy historical done status or access/entitlement to a new user.

Use `python -m harness.cli prepare PROJECT` for new UiPath working copies. Restore packages and validate each copy in Studio. Historical working scripts are reference authoring/verification tools; inspect their output paths before invoking and adapt writes to the local work area. Portal UI/robot execution is user-started only; never launch it or proxy restricted pages. Preserve all reference results and completed-run locks. Use your own service accounts and URLs; no transferred login sessions.
