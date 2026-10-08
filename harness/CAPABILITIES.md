# Capabilities to verify in the new Codex chat

| Capability | Setup / agent acceptance |
| --- | --- |
| Local shell/files | Open the clone as a local Windows project. Read AGENTS.md, run offline doctor and source check. Use the new user's approved workspace permissions. |
| Codex browser | Use the app's in-app browser tool first. Select a known tab or create a harmless public-page tab through its documented API, read current tool documentation and verify page state. Do not assume a shell HTTP request proves browser control. |
| Native computer | Install/enable official Computer Use in Plugins, including server and skill toggles. Read that installation's whole skill and its required guidance/confirmation/API docs. On the author's Windows provider the supported entrypoint is persistent node_repl importing `@oai/sky`; it is provided by the plugin, not an npm dependency to install from this repository. Initialize exactly as its current skill says and test a harmless app read/action. Never search for/launch a helper executable or invent a custom protocol. |
| Other browser provider | If a unified browser/Computer Use tool is exposed, use only that tool's documented entrypoint and observed state. It can expose browser control while native app APIs are disabled; this does not prove the separate Windows plugin is unavailable. Check the actual installed provider before reporting a blocker. |
| Office | Activated desktop apps plus matching activities. Native COM can configure/inspect a fresh local query without secret values; the lesson's real UiPath/Office runs still need execution evidence. Prefer structured integration when it fits; visual checks need permitted app control or user evidence. |
| UiPath | Studio/Robot and own entitlement, project packages restored, actual successful execution. Optional pinned CLI is authoring support; it does not license Studio or certify a run. |
| Portal | Official UiPath browser extension and user-granted file URL permission; current user-captured targets. Agent authors/verifies offline and the user starts portal UI/robots. No proxy or secondary automation to defeat a restricted page. |
| Cloud/API | Own accounts, private sign-in, current authenticated page or safe API check. No sessions/keys/permissions transferred by Git. |

Record an unavailable capability's exact observed failure and keep independent tasks moving. Do not assert everything works from installed-file discovery. Never lower browser, app or OS security policy to make a test pass. Account sign-ins and sensitive permission prompts stay with the user.

No general desktop MCP server, global allow-all config or copied plugin binaries are installed by setup.ps1. The supported provider supplies its own runtime, tools and policy. This preserves the same permission boundary as the author's course workflow.

Product references: [Computer Use setup and app access](https://learn.chatgpt.com/docs/computer-use), [built-in browser](https://learn.chatgpt.com/docs/browser). Checked 2026-10-08; follow your installed provider's current documentation if it differs.
