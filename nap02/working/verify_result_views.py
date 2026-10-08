"""Verify static saved result contents/assets; no browser navigation or rendering."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'nap02/deliverables'
NOTES = ROOT / 'nap02/notes'
notes = ['01_kavezo_lepesek.md', '02_webshop_lepesek.md', '03_meridian_lepesek.md',
         '04_kave_szimulacio.md', '05_raktar_elemzes.md', '06_hibavadaszat.md']
titles = ['Kávézó', 'Webshop', 'Meridian', 'Kávézó-szimuláció', 'Atlas raktár', 'Hibavadászat']

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.links = []
        self.images = []
        self.base = None
        self.hidden = 0
        self.scripts = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ('head', 'script', 'style'):
            self.hidden += 1
        if tag == 'script':
            self.scripts += 1
        if tag == 'base':
            self.base = d.get('href')
        if tag == 'a':
            self.links.append(d['href'])
        if tag == 'img':
            self.images.append(d['src'])

    def handle_endtag(self, tag):
        if tag in ('head', 'script', 'style'):
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)

def words(text):
    return re.findall(r'\w+', text.casefold())

def markdown_words(text):
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'(?m)^\s*\d+\.\s+', '', text)
    return words(text)

report = []
all_texts = {}
for i, (note, title) in enumerate(zip(notes, titles), 1):
    path = OUT / f'result_{i:02d}.html'
    source = path.read_text(encoding='utf-8')
    assert '\ufffd' not in source and '<meta charset="utf-8">' in source
    page = Page(source)
    assert page.scripts == 0 and page.base == '../notes/'
    visible = ' '.join(page.text)
    assert title in visible
    expected = markdown_words((NOTES / note).read_text(encoding='utf-8'))
    actual = words(visible)
    assert any(actual[j:j+len(expected)] == expected for j in range(len(actual))), f'Note content mismatch: page{i}'
    checked_assets = []
    for url in page.links + page.images:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = (path.parent / page.base / unquote(parts.path)).resolve()
        assert target.is_file(), f'Missing local reference on page{i}'
        if url in page.images:
            with Image.open(target) as img:
                dimensions = img.size
                img.verify()
            assert dimensions[0] > 300 and dimensions[1] > 100
        if target.suffix == '.bpmn':
            ET.parse(target)
        checked_assets.append(target.relative_to(ROOT).as_posix())
    assert page.images
    report.append({'page': path.relative_to(ROOT).as_posix(), 'title': title,
                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'source_note': note, 'all_note_words_present_in_exact_order': True,
                   'note_word_count': len(expected), 'checked_local_assets': checked_assets,
                   'image_count': len(page.images), 'utf8_and_static_document': True})
    all_texts[i] = visible

measurements = json.loads((OUT / 'szimulacios_osszehasonlitas.json').read_text(encoding='utf-8'))
assert len(measurements) == 7
for row in measurements:
    text = all_texts[4 if row['forgatokonyv'].startswith('kave_') else 5]
    for key in ['forgatokonyv', 'atlag_munkaidoben', 'atlag_naptari', 'futas_hossza_kerekitve']:
        assert str(row[key]) in text, f'Saved measurement not shown:{key}'
    for value in row['eroforras_kihasznaltsag_szazalek'].values():
        assert str(value) in text
models = json.loads((OUT / 'modell_ellenorzes.json').read_text(encoding='utf-8'))
assert all(m['references'] == m['reachable_from_start'] == m['path_to_end'] == 'pass' for m in models)
result = {'passed': True, 'date': '2026-10-07', 'method': 'Offline HTML text/link/image/BPMN checks against preserved notes/results; no browser navigation or rendering.',
          'pages': report, 'seven_actual_measurement_summaries_match': True,
          'existing_model_structure_reports_pass': True,
          'user_browser_evidence': 'User reports opened all six in Brave; seems fine; left open as requested. User does not claim substantive content expertise.',
          'substantive_content_verification': 'Assistant independently compared complete note text and seven saved measurement summaries plus resolved/decoded local images and model references.',
          'direct_agent_browser_visual_inspection': False,
          'limitation': 'Rendered layout/current pixels not independently inspected by agent because local-page browser control is blocked. Static content/assets and user-reported opening are verified separately.'}
(OUT / 'result_views_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Passed offline content/asset checks for6pages,{sum(r["image_count"] for r in report)}images and7saved simulation summaries.')
