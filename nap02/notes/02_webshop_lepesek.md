# 2. blokk – Webshop

1. Rendelés beérkezik → Rendelés rögzítése → Fizetési link küldése.
2. Eseményalapú kapu után két fogadó köztes esemény versenyez: Fizetés megérkezik vagy 48 óra letelt. A timer tényleges értéke PT48H.
3. Fizetés után Csomag összekészítése → Futárnak átadás. Időtúllépés után Rendelés törlése → Rendelés lezárva fizetés nélkül.
4. A bővítésben a futárnak átadás után külön Átvétel visszaigazolása üzenetre várunk.
5. Csak a visszaigazolás után indul a második eseményalapú kapu. 14 nap letelt (P14D) → Rendelés teljesítve; Visszaküldési igény érkezik → Visszáru kezelése → Rendelés lezárva visszaküldéssel.
6. A kapuk az elsőként bekövetkező eseményt követik; itt nincsenek igen/nem döntési ágak vagy elágazási valószínűségek.

Fájlok: [egyszerű modell](../deliverables/webshop_egyszeru.bpmn), [bővített modell](../deliverables/webshop_visszakuldes.bpmn), [ellenőrzött ábra](../deliverables/02_webshop_preview.jpg).

Az egyszerű modell az oktatói referencia szerkeszthető másolata; a bővítés külön készített folyamat. A bővítést bpmn.io-ban sikeresen megnyitottuk. Az eredeti tananyag változatlan.
