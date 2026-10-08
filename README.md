# BPA class automation harness

Reusable Codex skills, ordered workflows, UiPath code templates and verification tools for the BPA course. **Root napXX folders are local-only and excluded from GitHub.** Import your own lesson ZIPs after cloning. Start on another Windows laptop with **[SETUP.md](SETUP.md)**.

```powershell
git clone https://github.com/nagy-ag/bpm-class.git
cd bpm-class
./harness/setup.ps1
```

Open the folder in Codex, then ask: **“Use $bpa-course-access and SETUP.md to verify my setup. Use my fresh .bpa progress.”**

| Included | Location |
| --- | --- |
| Seven repo skills, including two explicit maintenance commands | [.agents/skills](.agents/skills) · [catalog](SKILLS.md) |
| Ordered execution contract | [AGENTS.md](AGENTS.md) · [WORKFLOWS.md](harness/WORKFLOWS.md) |
| Setup, own progress and fresh project copies | [harness](harness) |
| Blank credential fields | [.env.example](.env.example) |
| Local-only Hungarian lessons/assets | Import own ZIPs into napXX/napXX; never tracked |
| Shared automation code and task plans | [course tools](harness/course_tools) · [robot templates](harness/project_templates) · [task templates](harness/task_templates.json) |
| Historical reference summary (day artifacts stay local) | [reference progress](PROGRESS.md) |
| Tests and reusable verifiers | `python harness/verify.py` · [verification guide](harness/VERIFICATION.md) |
| Sharing exclusions | [SHARING.md](harness/SHARING.md) |

New-user progress/work start fresh in ignored .bpa; the author's completion is reference evidence. Tests and reusable verifiers remain versioned under harness. Course folders, secrets, account UI captures, downloaded caches and completed course artifacts are excluded. Preparing robots requires locally imported lesson assets; missing inputs stop preparation with an exact message.

Each laptop needs its own Codex capabilities, accounts, Office activation, UiPath licensing/packages and browser extension permissions. Sign-ins are private and portal runs are user-started. Native Power Query uses the verified Python-fetch → public JSON adaptation. A clone does not transfer permissions or certify execution on another laptop.

Supplied lessons/assets and third-party tools retain original ownership. No new license is granted to course materials or commercial products. Final graded submissions need the user's specific instruction.

For updated lesson ZIPs: **`$bpa-import-lessons nap05.zip`** stages/extracts first, safely replaces only source lessons and records new-version coursework as unfinished. Earlier completed tasks/results remain intact. **`$bpa-audit-injections nap05`** separately inspects source instructions without executing them. Both are explicit-only. See [lesson maintenance](harness/LESSON_UPDATES.md).
