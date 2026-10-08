"""Verify actual Office robot outputs without creating or editing Office files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as E
from zipfile import ZipFile
from openpyxl import load_workbook

p = argparse.ArgumentParser()
p.add_argument('--records', type=int, choices=[12,6], required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
source = here.parent / 'nap04/docs'
folder = here / 'RiportRobot' / f'reports_{a.records}'
ns = {'c':'http://schemas.openxmlformats.org/drawingml/2006/chart',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
checks = []

def check(label, condition):
    checks.append({'check':label,'passed':bool(condition)})
    if not condition: raise ValueError(label)

def workbook_values(path):
    book = load_workbook(path, read_only=True, data_only=False)
    try: return list(book['us-500'].values)
    finally: book.close()

original = workbook_values(source/'Raw_data.xlsx')
actual = workbook_values(folder/'Riport_adatok.xlsx')
check('All original243data rows and headers unchanged', len(original)==244 and original==actual)
expected_categories = [str(row[0]) for row in original[1:a.records+1]]
expected_values = [float(row[1]) for row in original[1:a.records+1]]

def chart_values(xml):
    chart = E.fromstring(xml)
    series = chart.findall('.//c:barChart/c:ser',ns)
    check('Exactly one clustered-column series', len(series)==1 and chart.find('.//c:barDir',ns).get('val')=='col'
          and chart.find('.//c:grouping',ns).get('val')=='clustered')
    categories = [v.text for v in series[0].findall('c:cat/c:strRef/c:strCache/c:pt/c:v',ns)]
    values = [float(v.text) for v in series[0].findall('c:val/c:numRef/c:numCache/c:pt/c:v',ns)]
    check('Exact first-record categories, including repeated states', categories==expected_categories)
    check('Exact first-record quantities and bar count', values==expected_values and len(values)==a.records)
    return categories,values

with ZipFile(folder/'Riport_adatok.xlsx') as z:
    charts = [name for name in z.namelist() if name.startswith('xl/charts/chart') and name.endswith('.xml')]
    check('Exactly one new Excel chart',len(charts)==1)
    chart_values(z.read(charts[0]))
    formulas = [node.text for node in E.fromstring(z.read(charts[0])).findall('.//c:f',ns)]
    check('Excel source range is exact', formulas==["'us-500'!$B$1",f"'us-500'!$A$2:$A${a.records+1}",f"'us-500'!$B$2:$B${a.records+1}"])
with ZipFile(folder/'Riport_eredmeny.pptx') as z, ZipFile(source/'Dickinson_Sample_Slides.pptx') as original_deck:
    slides = [name for name in z.namelist() if name.startswith('ppt/slides/slide') and name.endswith('.xml')]
    check('All nine slides retained',len(slides)==9)
    for index in range(1,9):
        part=f'ppt/slides/slide{index}.xml'
        old=[''.join(t.text or '' for t in para.findall('.//a:t',ns)) for para in E.fromstring(original_deck.read(part)).findall('.//a:p',ns)]
        new=[''.join(t.text or '' for t in para.findall('.//a:t',ns)) for para in E.fromstring(z.read(part)).findall('.//a:p',ns)]
        check(f'Original slide{index}text preserved',old==new)
    slide=E.fromstring(z.read('ppt/slides/slide9.xml'))
    title=''.join(t.text or '' for t in slide.findall('.//p:sp/p:txBody//a:t',ns))
    check('Slide9exact title',title==f'Az első {a.records} rekord mennyisége')
    frames=slide.findall('.//p:graphicFrame',ns)
    check('One pasted chart in named target',len(frames)==1 and frames[0].find('.//p:cNvPr',ns).get('name')==f'BPA_{a.records}_rekord')
    rid=frames[0].find('.//c:chart',ns).get('{'+ns['r']+'}id')
    rels=E.fromstring(z.read('ppt/slides/_rels/slide9.xml.rels'))
    target=next(rel.get('Target') for rel in rels if rel.get('Id')==rid)
    import posixpath
    part=posixpath.normpath(posixpath.join('ppt/slides',target))
    chart_values(z.read(part))
run=(here/f'report_{a.records}_run.json').read_text(encoding='utf-8-sig')
result=json.loads(run[run.index('{\n'):])
check('Actual robot completed without execution errors',result['Result']=='Success' and result['Data']['hasErrors'] is False and result['Data']['errorMessage'] is None)
report={'status':'passed','records':a.records,'checks':checks,
        'values':expected_values,'categories':expected_categories,
        'output_sha256':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['Riport_adatok.xlsx','Riport_eredmeny.pptx']},
        'native_visual_evidence':[f'../report_{a.records}_excel_reopened.jpg',f'../report_{a.records}_ppt_reopened.jpg']}
(folder/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Passed{len(checks)}checks for actual{a.records}-record Office outputs.')
