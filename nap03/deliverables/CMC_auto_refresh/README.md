# Automatic CMC → native Excel refresh

Verified2026-10-07: two actual UiPath runs fetched BTC/ETH/SOL using the canonical secure client, refreshed the native Power Query in Excel, saved and closed the working workbook. No intermediate user input. Both saved books exactly match their fetched snapshots; prices and both provider/fetched timestamps advanced. [Verification](verification.json).

Fetched UTC:15:49:20.983856 →15:51:18.620359. Runtime67s/62s. The actual CLI uses hasErrors=false/errorMessage=null and output={} rather than the newer Session ended envelope; raw run evidence is retained. The first filtered runtime omitted its verdict fields, so its saved workbook was independently checked against the actual snapshot.

To refresh again, open `C:/Users/nagya/dev/school/BPA/nap03/working/cmc_auto_refresh/CMC_Auto_Refresh` in Studio and run Main.xaml. It performs one fetch and one native refresh. Source root .env.local stays outside the project. No keys are in XAML or workbook. Original course workbooks are preserved.

This is the approved Python-fetch + native Power Query adaptation. Direct CMC web authentication inside Power Query remains an explicitly failed privacy-firewall probe. No permanent local scheduler was installed. Locked/logged-out Windows execution or an unattended Orchestrator service was not tested; native Office, UiPath, a local session and network access are required.

Source: [Main.xaml](Main.xaml), [project](project.json). Actual artifacts: [first workbook](run1.xlsx), [first check](run1.verification.json), [second workbook](run2.xlsx), [second check](run2.verification.json), [runtime](run2.json), [build](build.json). Credential-free quote snapshots are preserved alongside the books. The curated package excludes generated caches.
