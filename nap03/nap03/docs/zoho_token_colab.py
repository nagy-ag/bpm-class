# Azonos Colab-jegyzetfüzetben futtasd a token-, majd a lead-cellát.
# Self Client: ZohoCRM.modules.ALL scope; EU-s Zoho-fiók.
from getpass import getpass
import requests

CLIENT_ID = input('Client ID: ').strip()
CLIENT_SECRET = getpass('Client Secret: ').strip()
GRANT_CODE = getpass('Frissen generált, egyszer használható kód: ').strip()
if not all([CLIENT_ID, CLIENT_SECRET, GRANT_CODE]):
    raise ValueError('Mindhárom belépési adatot add meg.')

try:
    response = requests.post(
        'https://accounts.zoho.eu/oauth/v2/token',
        data={'grant_type': 'authorization_code', 'client_id': CLIENT_ID,
              'client_secret': CLIENT_SECRET, 'code': GRANT_CODE}, timeout=30)
except requests.RequestException:
    raise RuntimeError('A tokenkérés hálózati hibával leállt. Ellenőrizd a kapcsolatot.') from None
try:
    result = response.json()
except ValueError:
    raise RuntimeError(f'Nem JSON-válasz érkezett. HTTP: {response.status_code}') from None
if not response.ok or not result.get('access_token'):
    raise RuntimeError('Tokenkérés sikertelen: ' + str(result.get('error', response.status_code))
                       + '. A generált kód lejárt vagy már felhasznált kód is lehet.')
if result.get('api_domain') != 'https://www.zohoapis.eu':
    raise RuntimeError('Ez nem EU-s CRM-hozzáférés. Ellenőrizd a fiók adatközpontját.')
ACCESS_TOKEN = result['access_token']
REFRESH_TOKEN = result.get('refresh_token', '')
ZOHO_API_DOMAIN = result['api_domain']
print('Token kész. Érvényesség:', result.get('expires_in', 3600), 'másodperc.')
print('A token az ACCESS_TOKEN változóban van; futtasd ugyanitt a lead-cellát.')
