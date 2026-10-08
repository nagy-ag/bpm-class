# Modeling and repairs

Source prefix `nap02/nap02/`. Read each page and corresponding BPMN before editing copies. Preserve valid DI bounds/waypoints, unique IDs and consistent references.

## 1 — pages/01_kavezo.html

`kave_xor.bpmn`: `Vendég rendel` → `Rendelés felvétele` → `Kávé elkészítése` → XOR `Helyben fogyasztja?`; igen→`Csészébe kiöntés`, nem→`Elviteles pohárba töltés`; converge XOR→`Fizetés`→`Vendég kiszolgálva`. Compare `docs/kave_rendeles_xor.bpmn`. Question on split, both answer labels; merge doesn't wait for both alternatives. Keep baseline separate from parameterized models.

## 2 — pages/02_webshop.html

`webshop_egyszeru.bpmn`: `Rendelés beérkezik` → `Rendelés rögzítése` → `Fizetési link küldése` → event-based gateway followed immediately by intermediate catch events: payment message→packing→courier→completed end; timer `PT48H`→cancel→closed unpaid end. Compare `docs/webshop_rendeles_egyszeru.bpmn`. Include actual timer/message definitions; XOR data decision isn't an event race.

Extension `webshop_visszakuldes.bpmn`: after courier first receipt-confirmation message, then event gateway racing return request against `P14D`. Timer→completed; request→return handling→closed returned. Fourteen days start at receipt, not handoff. Preserve both versions and verify reachable ends.

## 3 — pages/03_karfelvetel.html

`meridian_karfelvetel.bpmn`, compare supplied model. Expanded insurer pool with `Automata feldolgozás` and `Kárügyintéző` lanes; black-box `Ügyfél (webes kárbejelentő űrlap)` pool.

Message start `Űrlap beérkezik`→`Automatikus ellenőrzés`→XOR `Hiánytalan a bejelentés?`. igen→`Kárakta létrehozása`→Send Task `Visszaigazolás küldése`→adjuster `Ügyintéző kijelölése`→`Kárügy megnyitva`. nem→adjuster Send Task `Hiánypótlás kérése`→message catch `Pótlás megérkezik`→existing automatic check.

Four message flows: customer→start; supplement request→customer; customer→supplement catch; acknowledgement→customer. Sequence flows cross lanes only within pool, never pools. Inspect lane membership, existing-check loop and dashed cross-pool messages in editor.

## 6 — pages/06_hibavadaszat.html

Read supplied `docs/hibas_1.bpmn`,2,3. Save `hibas_1_javitva.bpmn` etc with diagnosis/reasons:

1. Parallel split followed by XOR merge: parallel merge must synchronize invoice and picking before dispatch.
2. Add XOR question/answer labels, name unnamed activity as action, connect orphan appraisal to coherent credit-decision path; fix noun-only task names. Explain a minimal plausible placement; no unique lending policy is supplied.
3. Add controlled loop exit to a named end. A disconnected end doesn't repair an endless cycle.

Eight checks: named start; named ends; no isolated elements/appropriate incoming-outgoing; verb task names; branching XOR questions; labeled XOR alternatives; AND splits joined by AND; no decision labels on AND. Also check reachability, paths to ends, pool boundaries and DI references. Parse checks supplement editor reopen/semantic inspection.

Index café, both webshop versions, Meridian, three repairs/diagnosis and simulations. Day5 preview isn't its personalized assignment: fetch published case/parameters/deliverable/deadline requirements separately.
