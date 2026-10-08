"""Read-only native workbook check; report no credential values."""
import base64
import io
import json
from pathlib import Path
import re
import warnings
import zipfile
import xml.etree.ElementTree as ET
from bpa_access import read_env
import openpyxl

ROOT = Path(__file__).resolve().parents[2]

def verify(path):
    values = [v for v in read_env().values() if len(v) >= 8]
    needles = [v.encode(enc) for v in values for enc in ('utf-8', 'utf-16-le')]
    pieces = []
    queries = []
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            raw = archive.read(name)
            pieces.append(raw)
            if name.startswith('customXml/') and name.endswith('.xml'):
                element = ET.fromstring(raw)
                if element.tag.rsplit('}', 1)[-1] == 'DataMashup':
                    decoded = base64.b64decode(element.text)
                    pieces.append(decoded)
                    length = int.from_bytes(decoded[4:8], 'little')
                    with zipfile.ZipFile(io.BytesIO(decoded[8:8+length])) as mashup:
                        for item in mashup.namelist():
                            data = mashup.read(item)
                            pieces.append(data)
                            if item.endswith('.m'):
                                queries.append(data.decode('utf-8-sig'))
    if any(n in p for p in pieces for n in needles):
        raise SystemExit('Credential scan failed; workbook must not be delivered.')
    assert queries and all('.env.local' not in q and 'Web.Contents' not in q for q in queries)
    assert any('Json.Document(File.Contents(' in q for q in queries)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        wb = openpyxl.load_workbook(path, data_only=True)
    sheet = wb['Query1']
    rows = list(sheet.values)
    assert rows[0][:5] == ('CMC_ID', 'Név', 'Symbol', 'Ár (EUR)', '24h változás')
    data = [r for r in rows[1:] if r[0] is not None]
    assert {r[0] for r in data} in ({1,1027}, {1,1027,5426})
    assert all(isinstance(r[3], (int,float)) and isinstance(r[4], (int,float)) for r in data)
    expected = json.loads((ROOT/'nap03/working/cmc_power_query/quotes.json').read_text('utf-8'))
    for row in data:
        coin = expected['data'][str(row[0])]
        assert abs(row[3] - coin['quote']['EUR']['price']) < 1e-8
        assert row[5] == expected['status']['timestamp']
        assert row[6] == expected['fetched_utc']
    report = {'workbook': str(path), 'passed': True,
              'credential_scan': 'Passed: archive members and decoded/decompressed Power Query mashup',
              'query': 'Local public JSON import; no env source or web request',
              'rows': [dict(zip(rows[0], row)) for row in data]}
    out = path.with_suffix('.verification.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'rows':len(data),'evidence':str(out)}))

if __name__ == '__main__':
    import sys
    verify(Path(sys.argv[1]).resolve())
