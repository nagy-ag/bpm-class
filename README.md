# BPA class automation harness

Reusable Codex skills, ordered workflows, source lessons, UiPath projects and verification tools for nap01 through nap04. Start on another Windows laptop with **[SETUP.md](SETUP.md)**.

```powershell
git clone https://github.com/nagy-ag/bpm-class.git
cd bpm-class
./harness/setup.ps1
```

Open the folder in Codex, then ask: **“Use $bpa-course-access and SETUP.md to verify my setup. Use my fresh .bpa progress.”**

| Included | Location |
| --- | --- |
| Five repo skills | [.agents/skills](.agents/skills) · [catalog](SKILLS.md) |
| Ordered execution contract | [AGENTS.md](AGENTS.md) · [WORKFLOWS.md](harness/WORKFLOWS.md) |
| Setup, own progress and fresh project copies | [harness](harness) |
| Blank credential fields | [.env.example](.env.example) |
| Immutable Hungarian lessons/assets | nap01/nap01 through nap04/nap04 |
| Actual reference outputs and evidence | napXX/deliverables and notes · [reference progress](PROGRESS.md) |
| Tests and reusable verifiers | `python harness/verify.py` · [verification guide](harness/VERIFICATION.md) |
| Sharing exclusions | [SHARING.md](harness/SHARING.md) |

New-user progress/work start fresh in ignored .bpa; the author's completion is reference evidence. Tests and reusable verifiers remain versioned. Secrets, personal account UI captures, downloaded caches and obsolete aggregate archives are excluded.

Each laptop needs its own Codex capabilities, accounts, Office activation, UiPath licensing/packages and browser extension permissions. Sign-ins are private and portal runs are user-started. Native Power Query uses the verified Python-fetch → public JSON adaptation. A clone does not transfer permissions or certify execution on another laptop.

Supplied lessons/assets and third-party tools retain original ownership. No new license is granted to course materials or commercial products. Final graded submissions need the user's specific instruction.
