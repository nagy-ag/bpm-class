# 3. blokk – Meridian kárfelvétel

1. Meridian Biztosító medence: Automata feldolgozás és Kárügyintéző sávok.
2. Űrlap beérkezik (üzenet-kezdő esemény) → Automatikus ellenőrzés → Hiánytalan a bejelentés?
3. Igen: Kárakta létrehozása → Visszaigazolás küldése (Send Task) → Ügyintéző kijelölése → Kárügy megnyitva.
4. Nem: Hiánypótlás kérése (Send Task) → Pótlás megérkezik (fogadó üzenet-esemény) → vissza ugyanahhoz az Automatikus ellenőrzéshez.
5. Az Ügyfél külön, összecsukott medence. Négy üzenetáramlás: kitöltött űrlap, hiánypótló levél, pótolt adat, visszaigazoló e-mail.
6. Sorrendáramlás csak a biztosító medencéjén belül halad; szervezetek között üzenetáramlás van. A sávhatár nem medencehatár.

A strukturált űrlap kötelező mezőkkel, listákkal és mellékletekkel szabályalapú ellenőrzést tesz lehetővé. Szabad szöveghez vagy képekhez AI segíthet, de az egyedi kárügy érdemi elbírálásának emberi ellenőrzése szükséges. Ez a modell a kárfelvételt és a kárügy megnyitását írja le, nem a kárkifizetésről való döntést.

Fájl: [meridian_karfelvetel.bpmn](../deliverables/meridian_karfelvetel.bpmn). Az oktatói referencia szerkeszthető másolatából készült, explicit incoming/outgoing kapcsolatokkal. A modell bpmn.io-ban megnyílt, mindkét sáv és négy üzenetáramlás látható. [Ábra](../deliverables/03_meridian_preview.jpg).
