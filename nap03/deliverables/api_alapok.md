# API-alapok – nap03

Ellenőrizve: 2026-10-07. Forrás: a jelenlegi 01_api_alapok.html és cmc_pelda_valasz.json. Az alábbi árak kitalált tanórai példák, nem élő árfolyamok.

Az API (Application Programming Interface) két alkalmazás közötti adatcserét tesz lehetővé. A szolgáltató címe `https://pro-api.coinmarketcap.com`, a végpont (endpoint) `/v1/cryptocurrency/quotes/latest`. Az `id=1,1027` a Bitcoint és az Ethereumot választja ki; a `convert=EUR` euróban kéri az értékeket.

A GET adatot kér le. A POST például új CRM-rekordot hoz létre. A fejléc (header) hitelesítési és tartalomtípus-adatokat vihet; a törzs (body) a küldött üzleti adatot tartalmazza. Ebben a projektben a CMC-kulcs kizárólag az `X-CMC_PRO_API_KEY` fejlécben megy a CMC API-jának, soha nem az URL-ben vagy a munkafüzetben. A Zoho OAuth-tokenje az Authorization fejlécbe kerül; a fiktív lead mezői a POST JSON-törzsébe.

A JSON objektum mezőit név alapján, a lista elemeit index alapján érjük el. Itt a `data` objektum, a `"1"` és `"1027"` szöveges kulcsok, nem listaindexek. Python-útvonalak:

```python
btc = response["data"]["1"]["quote"]["EUR"]["price"]      # 73102.78
eth = response["data"]["1027"]["quote"]["EUR"]["price"]   # 2500.0
btc_change = response["data"]["1"]["quote"]["EUR"]["percent_change_24h"]  # -1.37
```

Az `error_code == 0` sikeres API-választ jelöl; az `error_message: null` ilyenkor normális. A HTTP-státuszt és a válasz tartalmát is ellenőrizni kell. CRM-írásnál az egyes rekordok sikerét és a kapott azonosító visszaolvasását is vizsgáljuk. Az automatizálás a hibás adatot is ismételten továbbíthatja, ezért a siker nem pusztán a hálózati kérés elküldése.

A példában a `percent_change_24h = 2.1` jelentése 2,1%. Excel százalékformátum előtt ezt 100-zal osztjuk, vagy literális százalékjelet használunk. A 2.1 értékre közvetlenül alkalmazott százalékformátum hibásan 210%-ot mutatna.
