"""Build a credential-free notebook from reviewed shared sources; no execution."""
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
cells = []


def markdown(text):
    cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(True)})


def code(text):
    cells.append({'cell_type': 'code', 'metadata': {}, 'source': text.splitlines(True),
                  'execution_count': None, 'outputs': []})


markdown('''# BPA Nap3 – Zoho és CMC
Előkészített, még nem futtatott Colab-jegyzetfüzet. A helyi tesztek nem Colab-bizonyítékok.
Csak fiktív tanfolyami rekordokat hoz létre. Nem küld üzenetet és nincs időzítő.
Futtasd a cellákat sorrendben; **ne használd a Run all parancsot** a beviteli cellák miatt.
Az API Teszt, a mini-feladat és a két árfolyamág külön futás.
Titkot kizárólag a saját maszkolt bemeneti meződbe írj. `.env.local` feltöltése tilos.
A Colab-runtime újraindítása törli a memóriabeli hozzáférést. Mentés/megosztás előtt töröld a kimeneteket.
''')
code('print("Szia, BPA!")\n')
markdown('A következő cella a megvizsgált közös kliens és az automatizmusok pontos forrását tölti be. Nem olvas helyi környezeti fájlt, nem küld hálózati kérést.\n')
sources = {name: (here / (name + '.py')).read_text(encoding='utf-8')
           for name in ('bpa_access', 'api_exercises', 'colab_runtime')}
code('import sys, types\n'
     + 'MODULE_SOURCES = ' + repr(sources) + '\n'
     + 'for name, source in MODULE_SOURCES.items():\n'
     + '    module = types.ModuleType(name)\n'
     + '    module.__file__ = "/content/BPA/nap03/working/" + name + ".py"\n'
     + '    sys.modules[name] = module\n'
     + '    exec(compile(source, module.__file__, "exec"), module.__dict__)\n'
     + 'from api_exercises import SAMPLE, MINI, create_verified, fetch_btc, run_chain, above_threshold\n'
     + 'from colab_runtime import private_runtime\n'
     + 'attempts = {}\nresults = {}\nprint("Közös kliens betöltve; még nem történt API-kérés.")\n')
markdown('## Privát hozzáférés – a felhasználó tölti ki\nA már működő EU-kliens újrahasználható. `r`: a meglévő refresh token; `g`: friss, egyszer használható grant code. A mezők értéke nem kerül kódba vagy kimenetbe. Az ügynök nem olvassa a bevitelt.\n')
code('api = private_runtime()\nprint("EU token kész a runtime memóriájában; titkos érték nincs kiírva.")\n')
markdown('## API Teszt / Atlas Market\nEgyszer futtasd. Meglévő pontos rekordnál csak ellenőrzés történik; az nem új létrehozás. Hálózati hiba után először ellenőrizd a CRM-et, ne indítsd újra a POST-ot.\n')
code('results["sample"] = create_verified(api, SAMPLE, attempts)\nprint(results["sample"])\n')
markdown('## Mini-feladat – külön fiktív érdeklődő\n')
code('results["mini"] = create_verified(api, MINI, attempts)\nprint(results["mini"])\n')
markdown('## Aktuális ár és kézzel választott küszöb\nAz ág minden futása új árat kér. Válassz egy pozitív, az aktuális ár alatti küszöböt az első ághoz; a másodikhoz az aktuális ár felettit. Ha a piac közben megváltozik, a tényleges ág számít.\n')
code('quote = fetch_btc(api)\nprint(quote)\n')
code('positive_threshold = float(input("Pozitív ág küszöbe EUR (ponttal): "))\n'
     'results["positive"] = run_chain(api, positive_threshold, "positive1", attempts)\n'
     'print(results["positive"])\n')
code('negative_threshold = float(input("Negatív ág küszöbe EUR (ponttal): "))\n'
     'results["negative"] = run_chain(api, negative_threshold, "negative1", attempts)\n'
     'print(results["negative"])\n')
markdown('## Külön offline határeset\nEz nem élő árfolyam- vagy CRM-bizonyíték.\n')
code('assert above_threshold(100, 99) is True\nassert above_threshold(100, 100) is False\nassert above_threshold(100, 101) is False\nprint("Offline szigorú > határesetek rendben.")\n')
markdown('## Bizonyíték és lezárás\nA CRM-ben nyisd meg a visszakapott rekordokat, ellenőrizd a mezőket és az API Teszt Timeline / Lead Created bejegyzését. A negatív ág kimenetében `crm_write_attempted=False` és mindkét azonosságvizsgálat 0 legyen. Az alábbi export csak a fiktív tanfolyami mezőket és eredményeket tartalmazza. A notebook kimenetét megosztás előtt töröld.\n')
code('import json\nfrom google.colab import files\n'
     'with open("BPA_Nap3_API_evidence.json", "w", encoding="utf-8") as stream:\n'
     '    json.dump(results, stream, ensure_ascii=False, indent=2)\n'
     'files.download("BPA_Nap3_API_evidence.json")\n')
code('api.clear()\nprint("Runtime API-kulcsok és tokenek törölve. A session bezárható.")\n')
root = next(p for p in here.parents if (p / 'AGENTS.md').is_file())
out = root / '.bpa/work/nap03/working/API_automation/BPA_Nap3_Zoho.ipynb'
out.parent.mkdir(parents=True, exist_ok=True)
notebook = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
            'language_info': {'name': 'python'}, 'colab': {'name': out.name}}, 'nbformat': 4, 'nbformat_minor': 5}
for index, cell in enumerate(cells):
    cell['id'] = f'bpa-{index:02d}'
out.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(out.parent / 'api_preparation_manifest.json').write_text(json.dumps({
    'scope': 'Preparation only; actual Colab/CRM creation remains pending',
    'source_sha256': {name + '.py': hashlib.sha256(text.encode('utf-8')).hexdigest() for name, text in sources.items()},
    'notebook_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'cells': len(cells), 'stored_outputs': 0,
}, indent=2) + '\n', encoding='utf-8')
print('Credential-free notebook prepared; no cells executed and no API requests sent.')
