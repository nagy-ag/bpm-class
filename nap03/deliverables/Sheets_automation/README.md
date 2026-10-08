# Google Sheets course automation

[Live course sheet](https://docs.google.com/spreadsheets/d/REDACTED_AUTHOR_SHEET_ID/edit) · [Bound Apps Script](https://script.google.com/u/0/home/projects/REDACTED_AUTHOR_SCRIPT_ID/edit)

Verified2026-10-07: actual bound Apps Script runs wrote BTC/ETH, refreshed their timestamps, then added SOL. Native Google Sheets exports confirm A1:C3/A1:C4, numeric positive EUR prices and native date cells. Full editor source readback matches the saved working code. The user privately supplied the CMC Script Property and completed Google authorization; no key was inserted into code, sheet cells, URLs or logs.

| Run | Sheet timestamp (Bucharest) | Verified rows |
| --- | --- | --- |
| First | 2026-10-07 18:25:28.199 | BTC, ETH |
| Refresh | 2026-10-07 18:28:12.522 | BTC, ETH |
| Mini | 2026-10-07 18:30:05.905 | BTC, ETH, SOL |

Sources: [two coins](cmc_sheets_secure.gs), [three coins](cmc_sheets_secure_sol.gs). Evidence: [first run](sheets_btc_eth_run1.json), [refresh](sheets_btc_eth_run2.json), [Solana](sheets_sol_run.json), [actual Solana table](sheets_sol_table.png), [actual Solana execution](sheets_sol_execution.png).

Exactly one Time-driven / Hour timer / Every hour trigger was saved for arfolyamFrissites. Its actual Time-Driven execution completed at18:43:39 Bucharest in4.34s. The safe log identifies execution=time_driven, three rows, fetched15:43:41.948Z/provider15:43:41.744Z. Native export verifies all three typed quotes and an advanced date timestamp. See [timed export check](sheets_hourly_run.json) and [actual execution](sheets_hourly_execution.png). The user confirmed permanent deletion; the agent then observed Showing0triggers. [Cleanup proof](sheets_hourly_trigger_removed.png). No practice trigger remains.

To refresh manually, select arfolyamFrissites in the bound editor and click Run. ARFOLYAMOK A:C is reserved for script output. The exported source contains only the property name; the user controls its value in Google. Do not export the Script Properties page or copy its value into project files.
