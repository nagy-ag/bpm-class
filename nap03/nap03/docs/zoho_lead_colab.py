from getpass import getpass
import requests

# Ha a token-cellát már futtattad, annak változóját használjuk.
ACCESS_TOKEN = globals().get('ACCESS_TOKEN') or getpass('Zoho access token: ').strip()
lead = {'Last_Name': 'Teszt', 'First_Name': 'API', 'Company': 'Atlas Market',
        'Email': 'api.teszt@example.com', 'Lead_Source': 'API',
        'Description': 'Oktatási rekord, a harmadik napon Colabból hoztam létre.'}
try:
    response = requests.post('https://www.zohoapis.eu/crm/v8/Leads',
        headers={'Authorization': f'Zoho-oauthtoken {ACCESS_TOKEN}'},
        json={'data': [lead], 'trigger': []}, timeout=30)
except requests.RequestException:
    raise RuntimeError('A kérés hálózati hibával leállt. Újrafuttatás előtt nézd meg a CRM-et: a rekord már létrejöhetett.') from None
try:
    result = response.json()
except ValueError:
    raise RuntimeError(f'Nem JSON-válasz érkezett. HTTP: {response.status_code}') from None
rows = result.get('data', [])
item = rows[0] if rows else result
print('HTTP státusz:', response.status_code)
if not response.ok or item.get('status') != 'success' or item.get('code') != 'SUCCESS':
    raise RuntimeError('CRM-hiba: ' + str(item.get('code', result.get('code', 'ismeretlen')))
                       + ': ' + str(item.get('message', result.get('message', ''))))
record_id = item.get('details', {}).get('id')
if not record_id:
    raise RuntimeError('A válasz nem tartalmazza a létrejött rekord azonosítóját.')
print('Rekord létrejött. Azonosító:', record_id)
print('A CRM Leads listájában keresd: API Teszt / Atlas Market.')
