# Repository skills

Open this repository as the local Codex project. `.agents/skills` is the sole maintained BPA skill location. Do not install additional copies under the user's global skills directory; those copies create duplicate discovery entries and drift. Restart Codex after removing old global entries if the catalog is stale.

| Invocation | Scope | Entrypoint |
| --- | --- | --- |
| `$bpa-course-access` | Shared setup and day routing | [.agents/skills/bpa-course-access/SKILL.md](.agents/skills/bpa-course-access/SKILL.md) |
| `$bpa-nap01` | Introduction, models, CMC/CRM and smoke robot | [.agents/skills/bpa-nap01/SKILL.md](.agents/skills/bpa-nap01/SKILL.md) |
| `$bpa-nap02` | BPMN and seven BIMP scenario variants | [.agents/skills/bpa-nap02/SKILL.md](.agents/skills/bpa-nap02/SKILL.md) |
| `$bpa-nap03` | API, Excel/Sheets, CRM and Colab; source-dependent legacy extension | [.agents/skills/bpa-nap03/SKILL.md](.agents/skills/bpa-nap03/SKILL.md) |
| `$bpa-nap04` | Native UiPath, Office, sorter and portal | [.agents/skills/bpa-nap04/SKILL.md](.agents/skills/bpa-nap04/SKILL.md) |
| `$bpa-import-lessons` | Explicit-only staged ZIP import; preserve old work and flag updated tasks unfinished | [.agents/skills/bpa-import-lessons/SKILL.md](.agents/skills/bpa-import-lessons/SKILL.md) |
| `$bpa-audit-injections` | Explicit-only passive instruction audit with contextual findings | [.agents/skills/bpa-audit-injections/SKILL.md](.agents/skills/bpa-audit-injections/SKILL.md) |

## Instruction ownership

Read the relevant authoritative file instead of copying its rules into every skill:

| Subject | Maintained source |
| --- | --- |
| Authorization, immutable sources, credentials, browser restrictions and surface cleanup | [AGENTS.md](AGENTS.md) |
| Ordered task claims, step transitions and handoff | [TASK_PROGRESS.md](TASK_PROGRESS.md) |
| Portable paths, local progress, revision routing and project preparation | [harness/WORKFLOWS.md](harness/WORKFLOWS.md) |
| Installation and new-laptop acceptance | [SETUP.md](SETUP.md) |
| Service access procedures / observed access inventory | [Access reference](.agents/skills/bpa-course-access/references/access.md) / [AUTOMATION.md](AUTOMATION.md) |
| Equivalent CLI/API results and user-assisted interaction | [Guided interaction](.agents/skills/bpa-course-access/references/guided-ui.md) |
| Lesson import transactions and source-specific revision plans | [harness/LESSON_UPDATES.md](harness/LESSON_UPDATES.md) |
| Exercise parameters and acceptance | The selected day skill's references and current supplied lesson |

For installed days without a dedicated entrypoint, including nap07/nap08, use `$bpa-course-access` with the current lessons and a source-specific task plan. Do not apply old nap04 chart ranges or Windows framework assumptions to a different day.

[course_skill_manifest.json](course_skill_manifest.json) records source hashes. Run the shared inspect_course.py after lesson updates and re-read changed requirements. Preserve Hungarian source bytes. Live accounts, tool availability and licensed apps need verification per laptop.

The maintenance invocation boundary is defined in `AGENTS.md`; commands and revision progress are in the lesson-maintenance source above. The import and injection-audit skills retain separate entrypoints because their authorized actions differ.
