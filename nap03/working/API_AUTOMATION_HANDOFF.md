# Nap03 API automation — prepared, cloud execution pending

2026-10-07. This package prepares D3-11 through D3-15. It does **not** complete those lessons or replace their actual Colab/CRM evidence. Earlier manual CRM and spreadsheet tasks remain in the day tracker.

Verified preparation: all notebook Python cells compile; no stored outputs or credential values; 17 offline tests pass; live CMC quote/Zoho read checks pass. Read-only searches found zero API Teszt and mini-example identities. No course lead was created by this preparation.

Open `BPA_Nap3_Zoho.ipynb` through Colab's Upload notebook option in the existing signed-in account. Run cells individually in order. The loader embeds the reviewed shared CourseAPI and two supporting modules, so no installation or credential-file upload is needed. Included Python files are reference sources; continue local requests with the canonical `nap03/working/bpa_access.py` at the BPA project root.

1. Execute the greeting and loader cells. Observe `Szia, BPA!` in a connected actual runtime.
2. The user privately runs/fills the masked credential prompts. Reuse the existing EU Client ID/Secret and refresh token (`r`); a fresh unused grant code (`g`) is an alternative. Never paste credentials into chat or code. Never upload `.env.local`. Token exchange uses the fixed EU accounts endpoint, body parameters and redirect rejection. CRM/CMC requests reuse the shared client and header credentials. Nothing saves tokens or keys to notebook outputs/files. Runtime reset requires private inputs again.
3. Run API Teszt once, then the distinct mini once. Both require HTTP201, one per-record SUCCESS/id and exact field readback. A previously saved exact record is reported as existing, not newly created. Conflicting/duplicate records or uncertain writes stop execution. Do not retry until the saved CRM state has been reconciled.
4. Fetch current BTC EUR. Enter a positive finite threshold below the current price for the positive run (`positive1`). The cell fetches again and reports its actual branch. Verify the new ÁRJELZÉS record by returned ID in CRM.
5. Enter a threshold above the current price for the negative run (`negative1`). Verify the actual price and negative outcome: no CRM write attempted, matching identity absent both before and after. The optional equality assertions are explicitly offline and cannot replace either live branch.
6. Open API Teszt in CRM and inspect Timeline / Lead Created, all returned fields and both other fictional records. Save course-only evidence and execution observations. The JSON export contains only fictional lesson fields/results; it does not export credentials.
7. Run the cleanup cell, clear all notebook outputs before exporting/sharing, and retain a clean notebook plus separate reviewed evidence. No scheduled job, notification or graded submission is included.

The stable run labels prevent accidental routine reruns in the same notebook; they are not a server-side transaction or uniqueness guarantee. An interrupted/uncertain write requires CRM reconciliation, including after a runtime reset or delayed search indexing. Never change a label merely to bypass such a stop.

The memory token cell is a security adaptation of the supplied token/refresh scripts. It preserves automatic refresh within this runtime. It does not automate account/password sign-in. Private inputs must be completed before the agent can continue without inspecting them.

Reference contracts: [Zoho insert records](https://www.zoho.com/crm/developer/docs/api/v8/insert-records.html), [Zoho search records](https://www.zoho.com/crm/developer/docs/api/v8/search-records.html). Search candidates are independently compared by exact fictional email identity.
