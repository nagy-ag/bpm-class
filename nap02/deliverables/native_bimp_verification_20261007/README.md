# Native BIMP verification — 2026-10-07

Passed: actual Save scenario, Save results BPMN and CSV downloads; saved result reimport in BIMP; Waiting times and Durations heat-map views. This is a separate fresh café baseline run, preserving all original seven comparison runs.

The actual run completed 100 cases, cost 91.1 EUR, and showed mean calendar time 31.6 minutes and mean working time 12.4 minutes. The downloaded result BPMN restored the same results without rerunning. Back to edit restored the scenario's 6-minute exponential arrivals, 100 cases, one Pultos at 8 EUR/hour and one Barista at 9 EUR/hour.

- [Scenario](native_scenario.bpmn), [results BPMN](native_results.bpmn), [results CSV](native_results.csv)
- [Actual result screen](bimp_results.png), [reimport proof](native_results_roundtrip.png), [reimport text](native_results_roundtrip.txt)
- [Waiting times](heatmap_waiting_user.png): takeaway filling has the highest average wait (3.3 minutes).
- [Durations](heatmap_duration_user.png): coffee preparation has the highest average duration (5.2 minutes).
- [Visual review](heatmap_review.json), [65-check verification](native_exports_verification.json), [file verifier](verify_native_exports.py)

The heat-map popup was outside the exposed browser-tab inventory. The user supplied both actual screenshots; their selected metrics and activity colors were checked against the native result table. The legend overlaps the right side of the diagram.

Earlier 2026-10-05 native-download and heat-map limitations are historical; this verification resolves those features for the new run. The separate six local result-view checks remain pending.
