# CoinMarketCap mini-feladat

A tényleges lekérés ideje: 2026-10-07 09:26:29 UTC. Pénznem: EUR.

| Kriptovaluta | Azonosító | EUR-ár a lekéréskor | JSON-útvonal |
| --- | --- | --- | --- |
| Bitcoin (BTC) | 1 | 74902.68393311542 | data → 1 → quote → EUR → price |
| Ethereum (ETH) | 1027 | 2328.532061121165 | data → 1027 → quote → EUR → price |

A `status.error_code` értéke 0; a `null` error_message normális sikeres válasznál. Mindkét ár szám, véges és pozitív. Ezek időponthoz kötött megfigyelések, nem rögzített árak.

A megadott nyilvános listings demót az alkalmazáson belüli böngésző `net::ERR_BLOCKED_BY_CLIENT` hibával blokkolta; nem állítunk sikeres demóeredményt. A saját kulcsos BTC/ETH lekérés ténylegesen sikerült. A kulcs a figyelmen kívül hagyott helyi konfigurációból HTTP-fejlécbe került, nem URL-be vagy beadandóba.

Az API meghatározott végponton fogad kérést; az `id` az eszközt, a `convert` a kért pénznemet választja ki. A válasz JSON, amelyben az objektumkulcsok mentén jutunk el az árhoz.

[Ellenőrzött megfigyelés](coinmarketcap_quotes.json). Új lekéréshez a projekt gyökeréből: `python nap01/working/cmc_quote_exercise.py`.
