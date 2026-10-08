from pathlib import Path
import csv,json,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'deliverables'; NOTES=ROOT/'notes'
def write(name,text): (NOTES/name).write_text(text.strip()+'\n',encoding='utf-8')
def to_minutes(value):
    n,unit=value.split()[:2]; return float(n)*{'seconds':1/60,'minutes':1,'hours':60,'days':1440}.get(unit,1)
summaries=[]
for file in sorted(OUT.glob('*_tablak.json')):
    tables=json.loads(file.read_text(encoding='utf-8')); stem=file.stem.removesuffix('_tablak')
    with (OUT/(stem+'_eredmenyek.csv')).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f)
        for index,table in enumerate(tables): writer.writerow(['table',index]); writer.writerows(table); writer.writerow([])
    general=tables[0]
    stats=next(t for t in tables if t and t[0]==['','Minimum','Maximum','Average'])
    resources=next(t for t in tables if t and t[0][0]=='Resource')
    activities=next(t for t in tables if t and t[0][0]=='Name' and len(t[0])>4)
    rows=activities[2:]
    biggest=max(rows,key=lambda r:float(r[3].split()[0])*({'s':1/60,'m':1,'h':60}.get(r[3].split()[1],1)))
    summary={'forgatokonyv':stem,'esetszam':int(general[0][0].split()[-1]),'atlag_munkaidoben':stats[2][3],'atlag_naptari':stats[1][3],'atlag_munkaido_perc':to_minutes(stats[2][3]),'atlag_naptari_perc':to_minutes(stats[1][3]),'futas_hossza_kerekitve':general[2][0].removeprefix('Total simulation time '),'koltseg_EUR':general[1][0].removeprefix('Total cost ').removesuffix(' EUR'),'legnagyobb_atlagos_varakozas_helye':biggest[0],'legnagyobb_atlagos_varakozas':biggest[3],'eroforras_kihasznaltsag_szazalek':dict(resources[1:])}
    summaries.append(summary)
(OUT/'szimulacios_osszehasonlitas.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'szimulacios_osszehasonlitas.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(summaries[0])); writer.writeheader()
    for row in summaries: writer.writerow({**row,'eroforras_kihasznaltsag_szazalek':json.dumps(row['eroforras_kihasznaltsag_szazalek'],ensure_ascii=False)})
def mdtable(items):
    text='| Forgatókönyv | Átlag munkaidőben | Átlag naptári | Kihasználtság | Legnagyobb átlagos várakozás | Futás hossza |\n| --- | --- | --- | --- | --- | --- |\n'
    for r in items:
        util='; '.join(k+': '+v+'%' for k,v in r['eroforras_kihasznaltsag_szazalek'].items())
        text+=f"| {r['forgatokonyv']} | {r['atlag_munkaidoben']} | {r['atlag_naptari']} | {util} | {r['legnagyobb_atlagos_varakozas_helye']}: {r['legnagyobb_atlagos_varakozas']} | {r['futas_hossza_kerekitve']} |\n"
    return text
write('02_webshop_lepesek.md','''# 2. blokk – Webshop

1. Rendelés beérkezik → Rendelés rögzítése → Fizetési link küldése.
2. Eseményalapú kapu után két fogadó köztes esemény versenyez: Fizetés megérkezik vagy 48 óra letelt. A timer tényleges értéke PT48H.
3. Fizetés után Csomag összekészítése → Futárnak átadás. Időtúllépés után Rendelés törlése → Rendelés lezárva fizetés nélkül.
4. A bővítésben a futárnak átadás után külön Átvétel visszaigazolása üzenetre várunk.
5. Csak a visszaigazolás után indul a második eseményalapú kapu. 14 nap letelt (P14D) → Rendelés teljesítve; Visszaküldési igény érkezik → Visszáru kezelése → Rendelés lezárva visszaküldéssel.
6. A kapuk az elsőként bekövetkező eseményt követik; itt nincsenek igen/nem döntési ágak vagy elágazási valószínűségek.

Fájlok: [egyszerű modell](../deliverables/webshop_egyszeru.bpmn), [bővített modell](../deliverables/webshop_visszakuldes.bpmn), [ellenőrzött ábra](../deliverables/02_webshop_preview.jpg).

Az egyszerű modell az oktatói referencia szerkeszthető másolata; a bővítés külön készített folyamat. A bővítést bpmn.io-ban sikeresen megnyitottuk. Az eredeti tananyag változatlan.
''')
write('03_meridian_lepesek.md','''# 3. blokk – Meridian kárfelvétel

1. Meridian Biztosító medence: Automata feldolgozás és Kárügyintéző sávok.
2. Űrlap beérkezik (üzenet-kezdő esemény) → Automatikus ellenőrzés → Hiánytalan a bejelentés?
3. Igen: Kárakta létrehozása → Visszaigazolás küldése (Send Task) → Ügyintéző kijelölése → Kárügy megnyitva.
4. Nem: Hiánypótlás kérése (Send Task) → Pótlás megérkezik (fogadó üzenet-esemény) → vissza ugyanahhoz az Automatikus ellenőrzéshez.
5. Az Ügyfél külön, összecsukott medence. Négy üzenetáramlás: kitöltött űrlap, hiánypótló levél, pótolt adat, visszaigazoló e-mail.
6. Sorrendáramlás csak a biztosító medencéjén belül halad; szervezetek között üzenetáramlás van. A sávhatár nem medencehatár.

A strukturált űrlap kötelező mezőkkel, listákkal és mellékletekkel szabályalapú ellenőrzést tesz lehetővé. Szabad szöveghez vagy képekhez AI segíthet, de az egyedi kárügy érdemi elbírálásának emberi ellenőrzése szükséges. Ez a modell a kárfelvételt és a kárügy megnyitását írja le, nem a kárkifizetésről való döntést.

Fájl: [meridian_karfelvetel.bpmn](../deliverables/meridian_karfelvetel.bpmn). Az oktatói referencia szerkeszthető másolatából készült, explicit incoming/outgoing kapcsolatokkal. A modell bpmn.io-ban megnyílt, mindkét sáv és négy üzenetáramlás látható. [Ábra](../deliverables/03_meridian_preview.jpg).
''')
write('04_kave_szimulacio.md','''# 4. blokk – Kávézó, négy BIMP-futás

Mérés: 2026-10-05, valódi BIMP Academic futások. Minden futás 100 befejezett eset. Kezdés: hétfő 09:00; munkarend hétfő–péntek 09:00–17:00; pénznem EUR; bemelegedési kizárás 0. Az érkezés exponenciális, 6 vagy 3 perces átlaggal. Pultos: 8 EUR/óra; Barista: 9 EUR/óra. Kapu: igen 60%, nem 40%.

| Tevékenység | Erőforrás | Eloszlás | Átlag/szórás percben |
| --- | --- | --- | --- |
| Rendelés felvétele | Pultos | Normal | 1.5 / 0.4 |
| Kávé elkészítése | Barista | Normal | 3.2 / 0.8 |
| Csészébe kiöntés | Barista | Fixed | 0.6 |
| Elviteles pohárba töltés | Barista | Fixed | 0.6 |
| Fizetés | Pultos | Normal | 1 / 0.3 |

'''+mdtable([r for r in summaries if r['forgatokonyv'].startswith('kave')])+'''

## Értelmezés

A barista vendégenként átlagosan 3.8 percet, a pultos 2.5 percet dolgozik. Hatperces érkezésköznél az elméleti terhelés 63.3% és 41.7%; háromperces érkezésköznél 126.7% és 83.3%. A 126.7% igény/kapacitás arány: tényleges kijelzett kihasználtság nem haladhatja meg a 100%-ot.

A csúcs alapváltozatának átlagos munkaidős átfutása 1.9 óra volt, a második baristával 12.5 perc, a második pultossal 1.3 óra. A plusz barista oldja fel a fő kapacitáshiányt; utána a pultos válik erősebben terheltté. A kétpultos változatban a barista kihasználtsága 99.24%, és a kiöntés előtt marad a nagy sor.

A 6 perces alaphelyzet 20.9 perces naptári átfutása meghaladta a 11.3 perces munkaidős átfutást, mert egy eset átnyúlt a következő munkanapra. A feladatok Duration eredményoszlopa a várakozást is tartalmazza; a külön Waiting time oszlopból olvassuk a sort.

A futások külön véletlen minták; a pontos különbségek egy-egy mérésből származnak, nem konfidenciaintervallumok. A paraméterezett BPMN-ek azonos beállításokat őriznek, ismételt futáskor más számok várhatók.

## Mentés és ellenőrzés

- Négy paraméterezett modell: kave_01_alap_szimulacio.bpmn, kave_02_csucs_szimulacio.bpmn, kave_03_ket_barista_szimulacio.bpmn, kave_04_ket_pultos_szimulacio.bpmn.
- Futásonként *_bimp.txt: a megjelenített eredményoldal; *_tablak.json és *_eredmenyek.csv: a megjelenített táblák veszteségmentes másolata.
- A böngészős Save scenario letöltés időtúllépést adott. A BPMN-paramétereket helyben mentettük az official QBP sémának megfelelően, a BIMP [hivatalos forráskódja](https://github.com/qbpsimulator/bimp-ui) alapján. A CSV a látható táblákból készült, nem a szolgáltatás natív exportja.
- A heat-map gomb nem nyitott új nézetet ebben a böngészőben. A várakozási és időtartam táblákat ellenőriztük; a feladatidők és a sor helye így rögzítve vannak.
''')
write('05_raktar_elemzes.md','''# 5. blokk – Atlas Market raktár, mérés és javaslat

Három valódi BIMP Academic futás 2026-10-05-én, mindegyikben 135 befejezett eset. Hétfői kezdés 06:00, napi hétfő–vasárnap 06:00–22:00 rendelkezésre állás, exponenciális érkezésköz 7 perc. Warm-up és tail kizárás 0%. Éjszakai túlóra nincs az alapmodellben; a fennmaradó feladatok a következő napon folytatódnak.

Erőforrások: Adminisztrátor 2 fő, 12 EUR/óra; Targoncás 8 vagy 10 fő, 14 EUR/óra; Raktáros 36 fő, 10 EUR/óra. A megadott létszám egyidejű kapacitás; műszakbeosztás és szünet külön nincs modellezve.

Feladatok Normal átlag/szórás, mindenütt perc: Kapuregisztráció 4/1, Lerakodás 40/10, Áruátvételi ellenőrzés 50/15, Kárjegyzőkönyv és félretétel 25/10, Betárolás 20/5, Készletrögzítés 7/2. Sérült tétel: igen 8%, nem 92%. B változatban kizárólag a nappali Betárolás lesz Fixed 0 perc; az éjszakai munka külön költség.

## Kapacitásbecslés

Alap: 135 × (40+20) = 8100 targonca-perc igény; 8 × 16 × 60 = 7680 perc kapacitás. Hiány 420 perc; igény/kapacitás 105.47%. A változat: 9600 perc kapacitás, 84.38% terhelés. B: nappal 135 × 40 = 5400 perc, 70.31% terhelés, plusz 2700 perc éjszakai betárolás.

'''+mdtable([r for r in summaries if r['forgatokonyv'].startswith('raktar')])+'''

## Az utolsó kamion befejezése

A BIMP a teljes futás hosszát ezen a nézeten kerekítve mutatja: alap 1.2 nap; A és B 1.1 nap. A kezdés 2026-10-05 06:00, ezért mindhárom futás utolsó kamionfolyamata a következő nap reggelén/délelőttjén fejeződött be. A kerekített értékek alapján az alapváltozat kb. 2026-10-06 10:48, A és B kb. 2026-10-06 08:24; ezek becslések, nem percre pontos időbélyegek. Egy tized nap kerekítési pontossága önmagában körülbelül ±72 percet jelent. A 135 exponenciális érkezés nem garantáltan esik egy napra; az utolsó befejezésben az érkezési mintázatnak is szerepe van.

## Költség és üzleti javaslat

Első lépésként az A változatot javaslom: a két további nappali targoncakapacitás megszünteti a számított tartós hiányt, és a mért munkaidős átlagot 3.1 óráról 2.2 órára csökkentette. A gépek és a kezelők egyidejű rendelkezésre állása egyaránt szükséges. Tervezett többlet munkaerőköltség az egyszerű 16 órás kapacitásfeltevéssel: 2 × 16 × 14 = 448 EUR/nap, gép- és egyéb költségek nélkül.

B 2.1 órás munkaidős átfutást adott, de az áru végleges betárolásának munkája nem tűnik el. 2700 perc = 45 munkaóra, 14 EUR/órával legalább 630 EUR közvetlen munkaköltség. Négyórás ablakban 45/4 = 11.25, tehát legalább 12 egyidejű targoncakapacitás kell. Tizenkét teljes négyórás kapacitás költsége 672 EUR, ami még nem tartalmaz éjszakai pótlékot, gépköltséget és biztonsági tartalékot. A B-ben mért 2721.9 EUR nappali feladatköltséghez az áthelyezett munkát külön hozzá kell számítani. A készletrögzítés ekkor előzetes átvételi rögzítés; a készlet fizikai hozzáférhetősége csak a későbbi betárolással teljes.

A BIMP összköltsége az elvégzett feladatok erőforrásköltségét mutatja (alap 3353 EUR, A 3304.8 EUR, B nappal 2721.9 EUR), nem a teljes rendelkezésre álló műszak bérét. A kisebb A futásköltség ezért nem bizonyít olcsóbb személyzetet; a feladatidők és ágak véletlenszerűen is változnak.

A raktárosok mért átlagos kihasználtsága 15.91–18.56%; ebből önmagában létszámcsökkentést nem javaslok. Vizsgálni kell az egyéb feladatokat, csúcsterhelést és a beosztást. A változatok külön véletlen minták, ezért a pontos üzleti döntéshez további ismétlések és valós időadatok szükségesek.

## Fájlok

Az alapmodell mellett három külön paraméterezett BPMN, három megjelenített eredményoldal, három JSON-tábla és három CSV készült. A paraméterekből generált BPMN-t a BIMP betöltötte; ellenőriztük a 06:00 kezdést, a napi munkarendet, a perceket, a létszámokat és a 92/8 ágakat. A Download CSV / Save scenario export helyett a látható táblák és a dokumentált QBP paraméterek helyben mentett példánya áll rendelkezésre.
''')
write('06_hibavadaszat.md','''# 6. blokk – Hibavadászat és nyolcpontos ellenőrzés

## Talált hibák és javítások

1. **hibas_1:** AND elágazás után XOR összevezetés állt. Mindkét ág külön tokent engedhetett a feladásra. Az összevezetés AND lett: a csomag feladása csak a számla és az áru elkészülte után indul, egyszer.
2. **hibas_2:** hiányzott az XOR kérdése, mindkét ág címkéje és az egyik feladat neve; a fedezetértékbecslés árva volt. Az értékbecslés az adatrögzítés és a döntés közé került. Kérdés: Hitel jóváhagyható? Igen → Hitel folyósítása; nem → Elutasító levél küldése. Mindkét ágnak elnevezett záró eseménye van. Az értékbecslés minden kérelemhez való elhelyezése a gyakorló javítás modellezési feltevése; tényleges banki szabályt nem állít.
3. **hibas_3:** nem volt záró esemény vagy kilépés; a döntés kérdés és címkék nélkül állt, a jóváhagyási lépés pedig visszaküldött a levélíráshoz. Most: vizsgálat → levél írása/javítása → vezetői jóváhagyás → Jóváhagyta a vezető? Igen → jóváhagyott válasz elküldése → Panasz lezárva. Nem → vissza a levél javításához. A vezetői jóváhagyás minden javítás után megismétlődik.

## Ellenőrzőlista

- Elnevezett kezdő esemény van.
- Minden út elérhet elnevezett záró eseményt.
- Nincs árva elem; a kezdő kivételével van bejövő, a záró kivételével van kimenő kapcsolat.
- Minden tevékenység cselekvést megnevező nevet kapott.
- Minden elágazó XOR kérdésként elnevezett.
- Minden elágazó XOR ág címkézett.
- A párhuzamos ágak AND összevezetésben zárulnak.
- Az AND ágak nem döntési címkéket kaptak.

Mindhárom javított modellre teljesül a lista, és mindhárom megnyílt bpmn.io-ban. Az elérhetőség ellenőrzése nem bizonyítja, hogy egy üzleti jóváhagyási ciklus valaha pozitív választ kap; a panaszfolyamatnak van helyes kilépési útja, de a külső döntés továbbra is szükséges.

Fájlok: [hibas_1_javitva.bpmn](../deliverables/hibas_1_javitva.bpmn), [hibas_2_javitva.bpmn](../deliverables/hibas_2_javitva.bpmn), [hibas_3_javitva.bpmn](../deliverables/hibas_3_javitva.bpmn). Képernyőképek és gépi szerkezeti ellenőrzés a deliverables mappában.

Az 5. napi első beadandó banki modell, BIMP-szimuláció, változatok összevetése és üzleti javaslat lesz. A konkrét paraméterek, leadási fájlok és határidő az 5. napi csomagból/Moodle-ből jönnek; ezt a nap02 csomag nem tartalmazza.
''')
index='''# nap02 – Elvégzett munka, 2026-10-05

Mind a hat blokk feladata elkészült. Az eredeti nap02/ tananyaghoz nem nyúltunk. A modellek bpmn.io-ban, a négy kávézó- és három raktárforgatókönyv BIMP Academic-ben ellenőrizve.

| Blokk | Eredmény | Útmutató / elemzés | Nyitva hagyott böngészőtab |
| --- | --- | --- | --- |
| 1. Kávézó | [kave_xor.bpmn](kave_xor.bpmn) | [Lépések](../notes/01_kavezo_lepesek.md) | 2: kávézómodell |
| 2. Webshop | [Egyszerű](webshop_egyszeru.bpmn), [visszaküldés](webshop_visszakuldes.bpmn) | [Lépések](../notes/02_webshop_lepesek.md) | 5: visszaküldési modell |
| 3. Meridian | [meridian_karfelvetel.bpmn](meridian_karfelvetel.bpmn) | [Lépések](../notes/03_meridian_lepesek.md) | 6: két sáv és ügyfélmedence |
| 4. Kávézó-szimuláció | Négy paraméterezett BPMN és valódi futási táblák | [Mérési elemzés](../notes/04_kave_szimulacio.md) | 3: BIMP, csúcs + két pultos |
| 5. Raktár | Három paraméterezett BPMN és valódi futási táblák | [Összevetés és javaslat](../notes/05_raktar_elemzes.md) | 4: BIMP, külön betárolás |
| 6. Hibavadászat | Három javított BPMN | [Hibanapló és ellenőrzőlista](../notes/06_hibavadaszat.md) | 7: javított panaszfolyamat |

Összesített [CSV](szimulacios_osszehasonlitas.csv), [JSON](szimulacios_osszehasonlitas.json), [modell-ellenőrzés](modell_ellenorzes.json).

A hat tab balról jobbra a blokkhoz rendelve: 1, 4, 5, 2, 3, 6. A modellező tabok címe azonos, a vásznon lévő modell azonosítja őket. A helyi HTML-leckék file: URL-jét az in-app böngésző biztonsági szabálya nem engedi, ezért a tabokon az elkészült modellek és az élő eredményoldalak maradnak.

A szolgáltatás letöltési eseménye időtúllépéssel végződött; a modelleket és a látható eredménytáblákat helyben mentettük. A heat-map felugró nézet nem nyílt meg, a várakozási táblákból elvégzett elemzés rendelkezésre áll. Az utolsó kamion időpontját csak a felületen kijelzett kerekített futáshossz pontosságával lehet megadni; az elemzés ezt jelzi.
'''
(OUT/'README.md').write_text(index,encoding='utf-8')
progress=(ROOT.parent/'PROGRESS.md').read_text(encoding='utf-8-sig')
progress=re.sub(r'\| \[nap02\].*\n','| [nap02](nap02/README.md) | BPMN modeling and simulation | Completed | All six blocks: [deliverable index](nap02/deliverables/README.md). Four café and three warehouse BIMP runs; models, repairs, CSVs and analysis saved. Export/popup limitations recorded. |\n',progress)
progress+='\n## nap02 completed — 2026-10-05\n\nCompleted all six blocks at user request. Seven BIMP runs finished (100 café or 135 warehouse instances each). Six in-app tabs retained for the six blocks. Deliverable index records parameterized models, measured result tables, comparisons, repairs, and browser export/heat-map limitations.\n'
(ROOT.parent/'PROGRESS.md').write_text(progress,encoding='utf-8')
print('Reports and CSVs saved for',len(summaries),'completed BIMP runs.')
