# BIMP parameters and evidence

Read current `pages/04_szimulacio.html` or `pages/05_raktar.html` and source model. Configure scenario→resources→tasks→gateways; match tasks by name, not UI order. All times **Minutes**. Split XOR probabilities total100%; merges get no new probabilities.

## Café: four runs

Use `kave_xor.bpmn` or supplied fallback copy. 100cases; Exponential interarrival mean6 baseline,3 peak; EUR; start09:00; Monday–Friday09:00–17:00 Default timetable. Initial-statistics exclusion blank per lesson. Pultos1 at8EUR/hour, Barista1 at9, both Default.

| Task | Resource | Distribution in minutes |
| --- | --- | --- |
| Rendelés felvétele | Pultos | Normal mean1.5/std0.4 |
| Kávé elkészítése | Barista | Normal3.2/0.8 |
| Csészébe kiöntés | Barista | Fixed0.6 |
| Elviteles pohárba töltés | Barista | Fixed0.6 |
| Fizetés | Pultos | Normal1/0.3 |

Cup60%, takeaway40%; fixed costs blank. Runs: baseline6,1/1; peak3,1/1; peak3,1/2; peak3,2/1 (cashier/barista). Restore previous extra resource before opposite intervention; don't test2/2 accidentally. Save distinct parameterized models/results.

Sanity: total active work6.3minutes, barista3.8, cashier2.5; baseline offered loads63%/42%, peak127%/83%. Offered load can exceed100%; realized reported utilization isn't capacity sufficiency. Extra cashier leaves barista overload. These are estimates, not measured results.

Record completed count, working/calendar mean cycle time, task waits, utilization/cost. Compare same definitions and stochastic variation. Inspect waiting and duration heat maps if available; calendar cycle includes closed-hours waits.

## Warehouse: three runs

Copy `docs/atlas_raktar_alap.bpmn`. 135cases, Exponential mean7Minutes, Monday06:00 start, warm-up/cool-down0%, EUR. Default Monday–Sunday06:00–22:00 for arrivals and all resources. Counts are simultaneous16-hour capacity; no separately modeled shifts/breaks. Unfinished work waits next opening; no automatic night overtime.

| Resource | Count | EUR/hour |
| --- | --- | --- |
| Adminisztrátor | 2 | 12 |
| Targoncás | 8 | 14 |
| Raktáros | 36 | 10 |

| Task | Resource | Normal mean/std minutes |
| --- | --- | --- |
| Kapuregisztráció | Adminisztrátor | 4/1 |
| Lerakodás | Targoncás | 40/10 |
| Áruátvételi ellenőrzés | Raktáros | 50/15 |
| Kárjegyzőkönyv és félretétel | Raktáros | 25/10 |
| Betárolás | Targoncás | 20/5 |
| Készletrögzítés | Adminisztrátor | 7/2 |

Damage8%/no92%. Baseline8forklifts; A10 with durations unchanged; B reset8, Betárolás Fixed0Minutes, others unchanged. B hands off to night, doesn't remove work; inventory registration becomes preliminary receipt.

Capacity: baseline135×60=8100/7680forklift-minutes (~105%); A8100/9600 (~84%); B day5400/7680 (~70%). B still needs2700night minutes=45worker-hours; four-hour window needs at leastceil(45/4)=12simultaneous capacity before variability. Discuss night cost/capacity and A extra day resources; low warehouse-worker average utilization alone doesn't justify layoffs.

For each run:135completed; mean working/calendar turnaround, forklift utilization, cost, last completion and start/timezone. If only rounded duration visible, label derived last completion approximate at that precision. Compare all three in management recommendation.

## Save and recover

Preserve baseline BPMN, seven scenario BPMNs, measured CSV/tables and comparisons. Prefer native Save scenario/Download CSV. If export fails, save verified parameters and observed tables locally with provenance; a transcribed CSV isn't a native export. Inspect existing outer QBP/schema resources before reuse; retain simulation extensions and verify import acceptance.

Blocked heat-map/security settings need policy-compliant user handoff; analyze observed waits and note unavailable view, never fabricate. For failed runs correct the actual cause; preserve prior successful evidence. No runtime/test framework needed for static lessons.
