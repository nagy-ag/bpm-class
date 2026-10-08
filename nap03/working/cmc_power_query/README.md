# CMC + Power Query adaptation

Direct native Power Query from the credential store failed Excel's privacy firewall. This is the user's approved fallback, with privacy protection retained.

From the BPA root, fetch public BTC/ETH quotes:

```powershell
python nap03/working/fetch_cmc_power_query.py
```

For the Solana mini:

```powershell
python nap03/working/fetch_cmc_power_query.py --solana
```

Then refresh the saved Excel query. `quotes.json` is replaced atomically; dated response files retain request and provider timestamps. The source M is `../cmc_local_import.pq`. It contains no credential values. Excel60minute refresh imports the local snapshot only; it does not start Python or make a new CMC request.

Native workbook creation, actual load/refresh and credential scans passed. Final workbooks and timestamp/price evidence are in ../../deliverables. Solana's two refreshes were89.244seconds apart. Sixty-minute Excel refresh imports the latest local snapshot; it does not fetch CMC. Both workbooks follow the active snapshot's coin list when refreshed.
