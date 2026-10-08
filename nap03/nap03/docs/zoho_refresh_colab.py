# Az előző tokenkérés cellájának változóit használja ugyanabban a Colabban.
import requests

if not globals().get('REFRESH_TOKEN') or not globals().get('CLIENT_ID') or not globals().get('CLIENT_SECRET'):
    raise RuntimeError('Előbb futtasd a tokenkérés celláját. A Colab újraindítása törli ezeket a változókat.')
try:
    response = requests.post('https://accounts.zoho.eu/oauth/v2/token',
        data={'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN,
              'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}, timeout=30)
except requests.RequestException:
    raise RuntimeError('Hálózati hiba a token frissítésekor.') from None
try:
    result = response.json()
except ValueError:
    raise RuntimeError('A tokenfrissítés nem JSON-választ adott.') from None
if not response.ok or not result.get('access_token'):
    raise RuntimeError('A tokenfrissítés sikertelen: ' + str(result.get('error', response.status_code)))
if result.get('api_domain') != 'https://www.zohoapis.eu':
    raise RuntimeError('A válasz adatközpontja nem EU-s.')
ACCESS_TOKEN = result['access_token']
print('ACCESS_TOKEN frissítve; a következő API-cellát újra futtathatod.')
