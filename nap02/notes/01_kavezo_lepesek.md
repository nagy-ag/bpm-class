# Kávézó – XOR-folyamat, lépésről lépésre

1. Nyisd meg a https://demo.bpmn.io/ szerkesztőt. Új rajzhoz válaszd a create lehetőséget.
2. A kezdő esemény neve: **Vendég rendel**. Fűzd hozzá: **Rendelés felvétele** → **Kávé elkészítése**.
3. A kávé elkészítése után helyezz el XOR-kaput: **Helyben fogyasztja?**
4. Az **igen** ág: **Csészébe kiöntés**. A **nem** ág: **Elviteles pohárba töltés**. Mindkét nyíl kapjon címkét.
5. Vezesd össze a két ágat egy második XOR-kapuval. Ez nem vár mindkét ágra: az adott rendeléshez kiválasztott ág után folytatja a folyamatot.
6. Fűzd hozzá: **Fizetés** → **Vendég kiszolgálva** (záró esemény). Mentsd **kave_xor.bpmn** néven.

## Elkészült fájl és ellenőrzés

- Kimenet: [kave_xor.bpmn](../deliverables/kave_xor.bpmn).
- A mellékelt oktatói referenciamodell szerkeszthető másolatából készült; az eredeti változatlan maradt. A modellben a bejövő és kimenő kapcsolat-hivatkozások is szerepelnek.
- Egy kezdő esemény, öt tevékenység, két XOR-kapu, egy záró esemény, kilenc sorrendáramlás.
- Igen út: Vendég rendel → Rendelés felvétele → Kávé elkészítése → Helyben fogyasztja? → Csészébe kiöntés → XOR-összevezetés → Fizetés → Vendég kiszolgálva.
- Nem út: ugyanez, a Csészébe kiöntés helyett Elviteles pohárba töltés.
- A munkapéldány megnyitása sikerült a bpmn.io-ban. A böngészős letöltés időtúllépéssel végződött; a végleges fájl helyben mentve.
- Ez az 1. blokk modellezési eredménye. A szimuláció a 4. blokkban következik.
