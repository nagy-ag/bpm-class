# Ár lekérése -> szabály -> jelzőrekord a CRM-ben. Nem hoz létre CRM Taskot.
from getpass import getpass
import requests
import math

CMC_KULCS = getpass('CoinMarketCap API-kulcs: ').strip()
ACCESS_TOKEN = globals().get('ACCESS_TOKEN') or getpass('Zoho access token: ').strip()
KUSZOB_EUR = 50000  # Tizedes számnál pontot használj; a két ágat külön teszteld.
try:
    response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
        params={'id': '1', 'convert': 'EUR', 'CMC_PRO_API_KEY': CMC_KULCS}, timeout=30)
except requests.RequestException:
    raise RuntimeError('Az árlekérés hálózati hibával leállt.') from None
try:
    result = response.json()
except ValueError:
    raise RuntimeError(f'Az árlekérés nem JSON-választ adott. HTTP: {response.status_code}') from None
if not response.ok or result.get('status', {}).get('error_code') != 0:
    raise RuntimeError('CMC-hiba: ' + str(result.get('status', {}).get('error_message') or response.status_code))
try:
    ar = float(result['data']['1']['quote']['EUR']['price'])
except (KeyError, TypeError, ValueError):
    raise RuntimeError('Hiányzik vagy hibás a BTC euróban megadott ára.') from None
if not math.isfinite(ar) or ar <= 0:
    raise RuntimeError('A BTC ára nem használható pozitív, véges számként.')
print(f'BTC ár: {ar:,.2f} EUR; küszöb: {KUSZOB_EUR:,.2f} EUR')
if ar > KUSZOB_EUR:
    lead = {'Last_Name': f'ÁRJELZÉS BTC {ar:,.0f} EUR', 'Company': 'Árfigyelő automatizmus',
            'Lead_Source': 'API', 'Description': f'Oktatási jelzés: BTC {ar:.2f} EUR > {KUSZOB_EUR:.2f} EUR.'}
    try:
        response = requests.post('https://www.zohoapis.eu/crm/v8/Leads',
            headers={'Authorization': f'Zoho-oauthtoken {ACCESS_TOKEN}'},
            json={'data': [lead], 'trigger': []}, timeout=30)
    except requests.RequestException:
        raise RuntimeError('A CRM-kérés hálózati hibával leállt. Újrafuttatás előtt ellenőrizd a Leads listát.') from None
    try:
        result = response.json()
    except ValueError:
        raise RuntimeError(f'A CRM nem JSON-választ adott. HTTP: {response.status_code}') from None
    item = (result.get('data') or [result])[0]
    if not response.ok or item.get('code') != 'SUCCESS' or item.get('status') != 'success':
        raise RuntimeError('CRM-hiba: ' + str(item.get('code', 'ismeretlen')) + ': ' + str(item.get('message', '')))
    record_id = item.get('details', {}).get('id')
    if not record_id:
        raise RuntimeError('A CRM-válasz nem tartalmazza a jelzőrekord azonosítóját. Ellenőrizd a Leads listát újrafuttatás előtt.')
    print('Jelzőrekord létrejött. Azonosító:', record_id)
else:
    print('A küszöböt nem haladta meg: nem hoztunk létre CRM-rekordot.')
