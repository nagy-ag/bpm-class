---
name: bpa-course-access
description: Prepare or resume BPA course access, route supplied days and newly imported lessons, and check CMC, Zoho EU, Moodle, Office and UiPath prerequisites. Use for course setup or cross-day automation requests.
---

# BPA access and routing

Resolve the current checkout using `AGENTS.md` and `harness/cli.py`. Read the [skill and instruction map](../../../SKILLS.md), then [harness/WORKFLOWS.md](../../../harness/WORKFLOWS.md) for the shared execution contract. It links the authoritative authorization, progress, setup and revision procedures; do not copy those procedures into day skills.

Read [references/access.md](references/access.md) for the selected service or missing prerequisite. Observed access belongs in root `AUTOMATION.md`, separately from coursework evidence.

For CLI/API equivalence or any step requiring human participation, read [references/guided-ui.md](references/guided-ui.md). Surface cleanup is governed by root `AGENTS.md`.

Inspect source freshness with `python .agents/skills/bpa-course-access/scripts/inspect_course.py --root . --day nap03`; add `--lesson pages/05_zoho_api.html` to read allowed lesson text. Omit `--day` for all installed days. Compare the inspected version with `course_skill_manifest.json` before using cached task parameters.

Select the day entrypoint from `SKILLS.md`. A newly imported day without a dedicated runbook uses its current index, lesson/task assets and source-specific acceptance plan under the shared workflow. Similar exercise types do not make another day's ranges, slide targets, framework or completion transferable.
