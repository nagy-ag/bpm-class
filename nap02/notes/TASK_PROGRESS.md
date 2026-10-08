# nap02 task progress

Follow [the mandatory workflow](../../TASK_PROGRESS.md) before every action. Claim a task, execute its ordered steps, verify each result and update immediately. Source requirements and implementation are in the installed day runbook.

Initialized 2026-10-06. Completed coursework is migrated from existing dated evidence, not rerun. Preserve other agents' claims, blockers and evidence.

| Task | Scope | Status | Next step |
| --- | --- | --- | --- |
| [D2-01 — Café XOR](#d2-01) | required | done | None |
| [D2-02 — Webshop payment race](#d2-02) | required | done | None |
| [D2-03 — Webshop return mini-exercise](#d2-03) | required | done | None |
| [D2-04 — Meridian claims model](#d2-04) | required | done | None |
| [D2-05 — Café baseline](#d2-05) | required | done | None |
| [D2-06 — Café peak](#d2-06) | required | done | None |
| [D2-07 — Peak plus barista](#d2-07) | required | done | None |
| [D2-08 — Peak plus cashier](#d2-08) | required | done | None |
| [D2-09 — Café comparison](#d2-09) | required | done | None |
| [D2-10 — Warehouse baseline](#d2-10) | required | done | None |
| [D2-11 — Warehouse A](#d2-11) | required | done | None |
| [D2-12 — Warehouse B](#d2-12) | required | done | None |
| [D2-13 — Warehouse comparison](#d2-13) | required | done | None |
| [D2-14 — Repair model1](#d2-14) | required | done | None |
| [D2-15 — Repair model2](#d2-15) | required | done | None |
| [D2-16 — Repair model3](#d2-16) | required | done | None |
| [D2-17 — Eight-point check and handoff](#d2-17) | required | done | None |
| [D2-VIEW-01 — Open existing results in Brave](#additional-requested-task) | user-requested extra | done | None |
| [D2-EXPORT-01 — Native BIMP export and heat-map verification](#d2-export-01) | user-requested verification | done | None |

<a id="d2-export-01"></a>
## D2-EXPORT-01 — Native BIMP export and heat-map verification

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

Scope: user explicitly requests every remaining feature test, excluding website re-login. Dependencies: preserved verified nap02 outputs. New runs are separate evidence; never replace earlier measurements.

Source: pages/04_szimulacio.html and pages/05_raktar.html, user-approved verification plan.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read current source and existing evidence; prepare separate fresh test workspace and observe BIMP. | done | Read current04lesson and simulation runbook; all43source hashes unchanged. Separate verification_2026-10-07/kave_native_export_test.bpmn copied with hash976d7e...; public Academic BIMP upload screen observed, earlier outputs untouched. |
| 2 | Import a saved scenario, run actual simulation and verify native model/result downloads against visible settings/results. | done | Native Save scenario, Save results BPMN and Download CSV all produced actual browser downloads. Fresh run100completed/91.1EUR/1.1days. Downloaded result BPMN reimported in separate BIMP tab without rerun: same100/91.1/31.6calendar-min/12.4work-min and task table; Back to edit restores Exponential6Minutes/100/one Pultos8/one Barista9. Files/screens preserved under verification_2026-10-07. |
| 3 | Open waiting/duration heat-map and verify rendered view against actual result tables. | done | Both user-supplied popup screenshots verified. Waiting times: takeaway red3.3m, cup orange2.9m, coffee yellow2m. Durations: coffee red5.2m, takeaway orange3.9m, cup orange3.5m, order yellow2.1m, payment green1.5m. Colors/order agree with fresh native results. Saved heatmap_waiting_user.png and heatmap_duration_user.png. |
| 4 | Preserve downloads/screenshots/results and record pass or exact blocker; reconcile summary. | done | Packaged actual native scenario/results/CSV, fresh results screen, BIMP reimport screen/text, both heat-map screenshots and visual review. Working and packaged verifier each pass65checks. Linked native_bimp_verification_20261007/README.md and root summary; older runs preserved. |

Handoff / exceptions: Website re-login excluded by user. File-URL restrictions remain; use only public BIMP UI and saved allowed uploads.

<a id="d2-01"></a>
## D2-01 — Café XOR

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [01_kavezo.html](../nap02/pages/01_kavezo.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson and reference; preserve supplied files. | done | [Model](../deliverables/kave_xor.bpmn), [notes](01_kavezo_lepesek.md) |
| 2 | Build named cup/takeaway XOR alternatives and merge before payment. Save working BPMN. | done | [Model](../deliverables/kave_xor.bpmn), [notes](01_kavezo_lepesek.md) |
| 3 | Reopen in bpmn.io; verify names, graph and event/gateway/pool semantics. | done | [Model](../deliverables/kave_xor.bpmn), [notes](01_kavezo_lepesek.md) |
| 4 | Link final model and verification. | done | [Model](../deliverables/kave_xor.bpmn), [notes](01_kavezo_lepesek.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-02"></a>
## D2-02 — Webshop payment race

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [02_webshop.html](../nap02/pages/02_webshop.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson and reference; preserve supplied files. | done | [Model](../deliverables/webshop_egyszeru.bpmn), [notes](02_webshop_lepesek.md) |
| 2 | Build message/payment-vs-PT48H race with both endings. Save working BPMN. | done | [Model](../deliverables/webshop_egyszeru.bpmn), [notes](02_webshop_lepesek.md) |
| 3 | Reopen in bpmn.io; verify names, graph and event/gateway/pool semantics. | done | [Model](../deliverables/webshop_egyszeru.bpmn), [notes](02_webshop_lepesek.md) |
| 4 | Link final model and verification. | done | [Model](../deliverables/webshop_egyszeru.bpmn), [notes](02_webshop_lepesek.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-03"></a>
## D2-03 — Webshop return mini-exercise

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [02_webshop.html](../nap02/pages/02_webshop.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson and reference; preserve supplied files. | done | [Model](../deliverables/webshop_visszakuldes.bpmn), [notes](02_webshop_lepesek.md) |
| 2 | After receipt confirmation, race return request against P14D. Save working BPMN. | done | [Model](../deliverables/webshop_visszakuldes.bpmn), [notes](02_webshop_lepesek.md) |
| 3 | Reopen in bpmn.io; verify names, graph and event/gateway/pool semantics. | done | [Model](../deliverables/webshop_visszakuldes.bpmn), [notes](02_webshop_lepesek.md) |
| 4 | Link final model and verification. | done | [Model](../deliverables/webshop_visszakuldes.bpmn), [notes](02_webshop_lepesek.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-04"></a>
## D2-04 — Meridian claims model

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [03_karfelvetel.html](../nap02/pages/03_karfelvetel.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read lesson and reference; preserve supplied files. | done | [Model](../deliverables/meridian_karfelvetel.bpmn), [notes](03_meridian_lepesek.md) |
| 2 | Build two insurer lanes, customer pool, four messages and supplement loop. Save working BPMN. | done | [Model](../deliverables/meridian_karfelvetel.bpmn), [notes](03_meridian_lepesek.md) |
| 3 | Reopen in bpmn.io; verify names, graph and event/gateway/pool semantics. | done | [Model](../deliverables/meridian_karfelvetel.bpmn), [notes](03_meridian_lepesek.md) |
| 4 | Link final model and verification. | done | [Model](../deliverables/meridian_karfelvetel.bpmn), [notes](03_meridian_lepesek.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-05"></a>
## D2-05 — Café baseline

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: D2-01 and prior café scenario where applicable.

Source: [04_szimulacio.html](../nap02/pages/04_szimulacio.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read current scenario requirements and prerequisite model. | done | [Scenario](../deliverables/kave_01_alap_szimulacio.bpmn), [results](../deliverables/kave_01_alap_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 2 | Configure100cases, minutes, timetable/costs/probabilities and mean6, cashier1/barista1. | done | [Scenario](../deliverables/kave_01_alap_szimulacio.bpmn), [results](../deliverables/kave_01_alap_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 3 | Run BIMP; verify100finished and measured cycle/wait/utilization/cost. | done | [Scenario](../deliverables/kave_01_alap_szimulacio.bpmn), [results](../deliverables/kave_01_alap_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 4 | Save scenario/results with accurate native-export or local-preservation provenance. | done | [Scenario](../deliverables/kave_01_alap_szimulacio.bpmn), [results](../deliverables/kave_01_alap_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-06"></a>
## D2-06 — Café peak

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: D2-01 and prior café scenario where applicable.

Source: [04_szimulacio.html](../nap02/pages/04_szimulacio.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read current scenario requirements and prerequisite model. | done | [Scenario](../deliverables/kave_02_csucs_szimulacio.bpmn), [results](../deliverables/kave_02_csucs_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 2 | Configure100cases, minutes, timetable/costs/probabilities and mean3, cashier1/barista1. | done | [Scenario](../deliverables/kave_02_csucs_szimulacio.bpmn), [results](../deliverables/kave_02_csucs_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 3 | Run BIMP; verify100finished and measured cycle/wait/utilization/cost. | done | [Scenario](../deliverables/kave_02_csucs_szimulacio.bpmn), [results](../deliverables/kave_02_csucs_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 4 | Save scenario/results with accurate native-export or local-preservation provenance. | done | [Scenario](../deliverables/kave_02_csucs_szimulacio.bpmn), [results](../deliverables/kave_02_csucs_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-07"></a>
## D2-07 — Peak plus barista

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: D2-01 and prior café scenario where applicable.

Source: [04_szimulacio.html](../nap02/pages/04_szimulacio.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read current scenario requirements and prerequisite model. | done | [Scenario](../deliverables/kave_03_ket_barista_szimulacio.bpmn), [results](../deliverables/kave_03_ket_barista_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 2 | Configure100cases, minutes, timetable/costs/probabilities and mean3, cashier1/barista2. | done | [Scenario](../deliverables/kave_03_ket_barista_szimulacio.bpmn), [results](../deliverables/kave_03_ket_barista_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 3 | Run BIMP; verify100finished and measured cycle/wait/utilization/cost. | done | [Scenario](../deliverables/kave_03_ket_barista_szimulacio.bpmn), [results](../deliverables/kave_03_ket_barista_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 4 | Save scenario/results with accurate native-export or local-preservation provenance. | done | [Scenario](../deliverables/kave_03_ket_barista_szimulacio.bpmn), [results](../deliverables/kave_03_ket_barista_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-08"></a>
## D2-08 — Peak plus cashier

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: D2-01 and prior café scenario where applicable.

Source: [04_szimulacio.html](../nap02/pages/04_szimulacio.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read current scenario requirements and prerequisite model. | done | [Scenario](../deliverables/kave_04_ket_pultos_szimulacio.bpmn), [results](../deliverables/kave_04_ket_pultos_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 2 | Configure100cases, minutes, timetable/costs/probabilities and mean3, cashier2/barista1; restore barista1. | done | [Scenario](../deliverables/kave_04_ket_pultos_szimulacio.bpmn), [results](../deliverables/kave_04_ket_pultos_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 3 | Run BIMP; verify100finished and measured cycle/wait/utilization/cost. | done | [Scenario](../deliverables/kave_04_ket_pultos_szimulacio.bpmn), [results](../deliverables/kave_04_ket_pultos_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |
| 4 | Save scenario/results with accurate native-export or local-preservation provenance. | done | [Scenario](../deliverables/kave_04_ket_pultos_szimulacio.bpmn), [results](../deliverables/kave_04_ket_pultos_eredmenyek.csv), [measurement](04_kave_szimulacio.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-09"></a>
## D2-09 — Café comparison

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: D2-05 through D2-08.

Source: [04_szimulacio.html](../nap02/pages/04_szimulacio.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read all four observed runs and consistent metric definitions. | done | [Analysis](04_kave_szimulacio.md), [comparison](../deliverables/szimulacios_osszehasonlitas.csv) |
| 2 | Compare offered loads with measured waits/cycles/utilization. | done | [Analysis](04_kave_szimulacio.md), [comparison](../deliverables/szimulacios_osszehasonlitas.csv) |
| 3 | Record heat-map limitation and observed table-based analysis. | done | [Analysis](04_kave_szimulacio.md), [comparison](../deliverables/szimulacios_osszehasonlitas.csv) |
| 4 | Save capacity recommendation with linked evidence. | done | [Analysis](04_kave_szimulacio.md), [comparison](../deliverables/szimulacios_osszehasonlitas.csv) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-10"></a>
## D2-10 — Warehouse baseline

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Prior applicable task; previous warehouse scenario where applicable.

Source: [05_raktar.html](../nap02/pages/05_raktar.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read source/model and simultaneous capacity assumptions. | done | [Scenario](../deliverables/raktar_01_alap_szimulacio.bpmn), [results](../deliverables/raktar_01_alap_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 2 | Configure135cases, mean7, Monday06:00, daily06–22, minutes/costs/branches and 8forklifts and original Normal durations. | done | [Scenario](../deliverables/raktar_01_alap_szimulacio.bpmn), [results](../deliverables/raktar_01_alap_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 3 | Run BIMP; verify135finished and measured cycle/utilization/cost/finish-time precision. | done | [Scenario](../deliverables/raktar_01_alap_szimulacio.bpmn), [results](../deliverables/raktar_01_alap_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 4 | Save scenario and measured results with documented limitations. | done | [Scenario](../deliverables/raktar_01_alap_szimulacio.bpmn), [results](../deliverables/raktar_01_alap_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-11"></a>
## D2-11 — Warehouse A

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Prior applicable task; previous warehouse scenario where applicable.

Source: [05_raktar.html](../nap02/pages/05_raktar.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read source/model and simultaneous capacity assumptions. | done | [Scenario](../deliverables/raktar_02_A_tiz_targoncas_szimulacio.bpmn), [results](../deliverables/raktar_02_A_tiz_targoncas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 2 | Configure135cases, mean7, Monday06:00, daily06–22, minutes/costs/branches and 10forklifts with original durations. | done | [Scenario](../deliverables/raktar_02_A_tiz_targoncas_szimulacio.bpmn), [results](../deliverables/raktar_02_A_tiz_targoncas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 3 | Run BIMP; verify135finished and measured cycle/utilization/cost/finish-time precision. | done | [Scenario](../deliverables/raktar_02_A_tiz_targoncas_szimulacio.bpmn), [results](../deliverables/raktar_02_A_tiz_targoncas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 4 | Save scenario and measured results with documented limitations. | done | [Scenario](../deliverables/raktar_02_A_tiz_targoncas_szimulacio.bpmn), [results](../deliverables/raktar_02_A_tiz_targoncas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-12"></a>
## D2-12 — Warehouse B

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Prior applicable task; previous warehouse scenario where applicable.

Source: [05_raktar.html](../nap02/pages/05_raktar.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read source/model and simultaneous capacity assumptions. | done | [Scenario](../deliverables/raktar_03_B_kulon_betarolas_szimulacio.bpmn), [results](../deliverables/raktar_03_B_kulon_betarolas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 2 | Configure135cases, mean7, Monday06:00, daily06–22, minutes/costs/branches and reset8forklifts and putaway Fixed0minutes; retain separate night work. | done | [Scenario](../deliverables/raktar_03_B_kulon_betarolas_szimulacio.bpmn), [results](../deliverables/raktar_03_B_kulon_betarolas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 3 | Run BIMP; verify135finished and measured cycle/utilization/cost/finish-time precision. | done | [Scenario](../deliverables/raktar_03_B_kulon_betarolas_szimulacio.bpmn), [results](../deliverables/raktar_03_B_kulon_betarolas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |
| 4 | Save scenario and measured results with documented limitations. | done | [Scenario](../deliverables/raktar_03_B_kulon_betarolas_szimulacio.bpmn), [results](../deliverables/raktar_03_B_kulon_betarolas_eredmenyek.csv), [measurement](05_raktar_elemzes.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-13"></a>
## D2-13 — Warehouse comparison

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: D2-10 through D2-12.

Source: [05_raktar.html](../nap02/pages/05_raktar.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read comparable three-run evidence. | done | [Analysis](05_raktar_elemzes.md) |
| 2 | Calculate day capacity and retained night effort/cost. | done | [Analysis](05_raktar_elemzes.md) |
| 3 | Compare measured turnaround, utilization and approximate last completion. | done | [Analysis](05_raktar_elemzes.md) |
| 4 | Save justified recommendation without inferring layoffs from average utilization. | done | [Analysis](05_raktar_elemzes.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-14"></a>
## D2-14 — Repair model1

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [06_hibavadaszat.html](../nap02/pages/06_hibavadaszat.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read broken source model and identify actual errors. | done | [Repair](../deliverables/hibas_1_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 2 | Replace XOR merge with synchronizing AND. Save repaired working copy. | done | [Repair](../deliverables/hibas_1_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 3 | Reopen and verify gateway semantics, labels and reachable completion. | done | [Repair](../deliverables/hibas_1_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 4 | Save final repair and diagnosis. | done | [Repair](../deliverables/hibas_1_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-15"></a>
## D2-15 — Repair model2

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [06_hibavadaszat.html](../nap02/pages/06_hibavadaszat.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read broken source model and identify actual errors. | done | [Repair](../deliverables/hibas_2_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 2 | Name task/question/branches and connect appraisal coherently. Save repaired working copy. | done | [Repair](../deliverables/hibas_2_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 3 | Reopen and verify gateway semantics, labels and reachable completion. | done | [Repair](../deliverables/hibas_2_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 4 | Save final repair and diagnosis. | done | [Repair](../deliverables/hibas_2_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-16"></a>
## D2-16 — Repair model3

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: Previous applicable task.

Source: [06_hibavadaszat.html](../nap02/pages/06_hibavadaszat.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read broken source model and identify actual errors. | done | [Repair](../deliverables/hibas_3_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 2 | Add controlled loop exit reaching a named end. Save repaired working copy. | done | [Repair](../deliverables/hibas_3_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 3 | Reopen and verify gateway semantics, labels and reachable completion. | done | [Repair](../deliverables/hibas_3_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |
| 4 | Save final repair and diagnosis. | done | [Repair](../deliverables/hibas_3_javitva.bpmn), [diagnosis](06_hibavadaszat.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="d2-17"></a>
## D2-17 — Eight-point check and handoff

Status: `done` · Owner: `unassigned` · Updated: 2026-10-06 · Next step: None

Scope: required. Dependencies: All required nap02 tasks.

Source: [06_hibavadaszat.html](../nap02/pages/06_hibavadaszat.html).

Prior verification: 2026-10-05. Native simulation exports/heat-map limitations remain in measurement notes; no new platform run is claimed.

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Read all applicable completed models and repairs. | done | [Checklist](06_hibavadaszat.md), [validation](../deliverables/modell_ellenorzes.json), [index](../deliverables/README.md) |
| 2 | Apply eight checks plus reachability and DI consistency. | done | [Checklist](06_hibavadaszat.md), [validation](../deliverables/modell_ellenorzes.json), [index](../deliverables/README.md) |
| 3 | Confirm seven measured scenarios and known limitations are linked. | done | [Checklist](06_hibavadaszat.md), [validation](../deliverables/modell_ellenorzes.json), [index](../deliverables/README.md) |
| 4 | Save index and reconcile course summary. | done | [Checklist](06_hibavadaszat.md), [validation](../deliverables/modell_ellenorzes.json), [index](../deliverables/README.md) |

Handoff / exceptions: None beyond linked evidence. Record scope/source changes, blockers and retry-safe resume instructions here.

<a id="additional-requested-task"></a>
## Additional requested task

### D2-VIEW-01 — Open existing results in Brave

Source: user request, 2026-10-06. Dependencies: saved six-block deliverables and previews verified in the deliverable index.

Status: `done` · Owner: `unassigned` · Updated: 2026-10-07 · Next step: None

| Step | Action / acceptance | Status | Evidence / blocker |
| --- | --- | --- | --- |
| 1 | Prepare browser-readable views of the existing six blocks, preserving original models and measurements. | done | [View 1](../deliverables/result_01.html), [2](../deliverables/result_02.html), [3](../deliverables/result_03.html), [4](../deliverables/result_04.html), [5](../deliverables/result_05.html), [6](../deliverables/result_06.html); static HTML renders existing notes and saved screenshots. |
| 2 | Open six result views in Brave and verify the displayed results. | done | User confirms all6Brave pages opened/seem fine. Independent offline verifier passed exact complete note text,8decoded images/all local links/BPMN XML and7actual saved simulation summaries. result_views_verification.json preserves provenance; direct agent local-page visual/layout inspection remains unavailable and is not claimed. |
| 3 | Leave user-opened result views available and record verification provenance/limits. | done | User reports all6views opened; agent closed none. Final report/index/root summary record independently verified content/assets/results and no direct agent browser visual/layout inspection. Later permitted public-site browser work explicitly superseded old session-wide stop; local-page restriction preserved. No further user action required. |
