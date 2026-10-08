"""Inspect actual browser-downloaded BIMP files; never simulates or controls UI."""
from pathlib import Path
import csv
import hashlib
import json
import math
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
QBP = {'q': 'http://www.qbp-simulator.com/Schema201212',
       'a': 'http://www.qbp-simulator.com/ApiSchema201212'}
checks = []


def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})
    if not condition:
        raise ValueError(name)


scenario = ET.parse(HERE / 'native_scenario.bpmn')
result = ET.parse(HERE / 'native_results.bpmn')
sim = scenario.find('.//q:processSimulationInfo', QBP)
check('Native scenario has simulation parameters', sim is not None)
check('100 instances and EUR preserved', sim.get('processInstances') == '100' and sim.get('currency') == 'EUR')
resources = {e.get('id'): (e.get('totalAmount'), e.get('costPerHour'))
             for e in sim.findall('q:resources/q:resource', QBP)}
check('Original resource capacity and rates', resources == {'Pultos': ('1', '8'), 'Barista': ('1', '9')})
res = result.find('.//a:Results[a:process]', QBP)
check('Save results contains actual simulation output', res is not None)
process = res.find('a:process', QBP)
metric = lambda name: float(process.findtext('a:' + name, namespaces=QBP))
check('Completed count matches actual visible100', metric('processInstances') == 100)
check('Total cost rounds to actual visible91.1EUR', round(metric('totalCost'), 1) == 91.1)
check('Calendar mean matches visible31.6minutes', round(metric('averageCycleTime') / 60, 1) == 31.6)
check('Working mean matches visible12.4minutes', round(metric('averageDuration') / 60, 1) == 12.4)
rows = list(csv.reader((HERE / 'native_results.csv').open(encoding='utf-8-sig', newline='')))
for element in res.findall('a:elements/a:element', QBP):
    element_id = element.get('id')
    matching = [row for row in rows if len(row) > 25 and row[1] == element_id]
    check(element_id + ' has exactly one native CSV row', len(matching) == 1)
    row = matching[0]
    check(element_id + ' name unchanged', row[0] == element.get('name'))
    check(element_id + ' count agrees', int(row[-1]) == int(element.findtext('a:count', namespaces=QBP)))
    for index, field in [(2, 'duration'), (6, 'waitingTime'), (14, 'cost')]:
        actual = float(element.findtext('a:' + field + '/a:average', namespaces=QBP))
        check(element_id + ' CSV/XML average ' + field, math.isclose(float(row[index]), actual, rel_tol=1e-9, abs_tol=1e-9))
check('All five task IDs retained alongside gateway/event statistics',
      {e.get('id') for e in res.findall('a:elements/a:element', QBP)
       if e.get('id', '').startswith('Process_1.t')} == {f'Process_1.t{i}' for i in range(1, 6)})
review_path = HERE / 'heatmap_review.json'
review = json.loads(review_path.read_text(encoding='utf-8')) if review_path.exists() else {}
heatmap_verified = review.get('status') == 'passed'
if heatmap_verified:
    for metric in ('waiting_times', 'durations'):
        check(metric + ' reviewed rendered evidence exists', (HERE / review[metric]['screenshot']).is_file())
report = {'status': 'passed' if heatmap_verified else 'native_exports_passed_heatmap_pending', 'checks': checks,
          'heatmap_visual_review': review if heatmap_verified else None,
          'native_results_reimported_in_bimp': True,
          'new_run_not_replacement_for_20261005_measurements': True,
          'files': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                    for name in ['native_scenario.bpmn', 'native_results.bpmn', 'native_results.csv']}}
(HERE / 'native_exports_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Passed {len(checks)} checks; heat-map visual review {"passed" if heatmap_verified else "pending"}.')
