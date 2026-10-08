"""Memory-only adaptation of supplied token/refresh cells; no workspace secrets.

API operations inherit the shared CourseAPI, including redirect rejection,
header-based CMC authentication and no automatic retry of CRM writes.
"""
from getpass import getpass
import json
import time
from urllib.parse import urlencode
from urllib.request import Request
from urllib.error import HTTPError, URLError

from bpa_access import AccessError, CourseAPI


class MemoryCourseAPI(CourseAPI):
    def __init__(self, values):
        super().__init__()
        self._values = dict(values)
        self._expires_at = 0

    def credentials(self):
        return self._values

    def authorize(self, grant_code=''):
        values = self._values
        fields = {'client_id': values.get('ZOHO_CLIENT_ID', ''),
                  'client_secret': values.get('ZOHO_CLIENT_SECRET', '')}
        if not all(fields.values()):
            raise AccessError('Private runtime Client ID and Client Secret are required.')
        if grant_code:
            fields.update(grant_type='authorization_code', code=grant_code)
        elif values.get('ZOHO_REFRESH_TOKEN'):
            fields.update(grant_type='refresh_token', refresh_token=values['ZOHO_REFRESH_TOKEN'])
        else:
            raise AccessError('Private runtime authorization is missing.')
        request = Request('https://accounts.zoho.eu/oauth/v2/token',
                          data=urlencode(fields).encode('utf-8'), method='POST',
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
        try:
            with self.opener.open(request, timeout=30) as response:
                result = json.loads(response.read())
        except (HTTPError, URLError, OSError, ValueError):
            raise AccessError('EU token request failed; check authorization privately. No automatic code retry.') from None
        if not isinstance(result, dict) or result.get('api_domain') != 'https://www.zohoapis.eu' or not result.get('access_token'):
            raise AccessError('EU token response was not valid; check authorization privately.')
        try:
            duration = int(result.get('expires_in', 3600))
        except (ValueError, TypeError):
            raise AccessError('Token response has an invalid duration.') from None
        if duration <= 120:
            raise AccessError('Token response has an unusable duration.')
        values['ZOHO_ACCESS_TOKEN'] = result['access_token']
        if result.get('refresh_token'):
            values['ZOHO_REFRESH_TOKEN'] = result['refresh_token']
        self._expires_at = time.time() + duration

    def authenticate(self, *, force=False):
        if force or not self._values.get('ZOHO_ACCESS_TOKEN') or time.time() >= self._expires_at - 120:
            self.authorize()
        return self._values['ZOHO_ACCESS_TOKEN']

    def clear(self):
        self._values.clear()
        self._expires_at = 0


def private_runtime():
    # Human fills masked prompts. Agent never transfers .env.local into Colab.
    values = {'ZOHO_CLIENT_ID': getpass('Zoho EU Client ID: ').strip(),
              'ZOHO_CLIENT_SECRET': getpass('Zoho EU Client Secret: ').strip()}
    mode = input('Existing refresh token (r) or fresh unused grant code (g)? ').strip().lower()
    grant = ''
    if mode == 'r':
        values['ZOHO_REFRESH_TOKEN'] = getpass('Existing Zoho refresh token: ').strip()
    elif mode == 'g':
        grant = getpass('Fresh unused Zoho EU grant code: ').strip()
        if not grant:
            raise AccessError('Grant code cannot be empty.')
    else:
        raise AccessError('Choose r or g; no request was sent.')
    api = MemoryCourseAPI(values)
    values.clear()
    try:
        api.authorize(grant)
    finally:
        grant = ''
    api.credentials()['CMC_PRO_API_KEY'] = getpass('CoinMarketCap API key: ').strip()
    if not api.credentials()['CMC_PRO_API_KEY']:
        api.clear()
        raise AccessError('CMC key cannot be empty.')
    return api
