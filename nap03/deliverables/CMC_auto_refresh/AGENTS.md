# CMC native refresh robot

Read ../.agents/skills/uipath-rpa/SKILL.md before edits. Windows/VB, native Excel3.6.1 and System26.8.2. No portal/browser operations.

Main.xaml performs one bounded canonical Python fetch, then opens CMC_Auto_Refresh.xlsx in a separate Excel process, refreshes its actual Power Query connections and saves/closes it. The inline VB bridge only starts the existing Python fetch; it does not read secrets or perform UI actions. The Python client reads the ignored root .env.local and writes credential-free quotes.json. Never place keys in XAML, command arguments, logs or workbooks.

Use validate then build after changes; inspect actual run output and verify_cmc_workbook.py. Main.xaml is safe to rerun for quote updates. No permanent scheduler is installed. Preserve the original nap03/deliverables/CMC_arfolyamok_SOL.xlsx.
