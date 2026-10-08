"""Shared course API access. Standard library only; never prints credentials.

Commands from the BPA root:
  python nap03/working/bpa_access.py status
  python nap03/working/bpa_access.py check
  python nap03/working/bpa_access.py zoho-auth
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / '.env.local'
TOKEN_HELPER = Path(__file__).with_name('zoho_tokens.ps1')
KEYS = ('CMC_PRO_API_KEY', 'ZOHO_CLIENT_ID', 'ZOHO_CLIENT_SECRET',
        'ZOHO_GRANT_CODE', 'ZOHO_ACCESS_TOKEN', 'ZOHO_REFRESH_TOKEN')


class AccessError(RuntimeError):
    """Only safe, predefined diagnostics may be included in this exception."""


class APIError(AccessError):
    def __init__(self, service: str, status: int, code: str = ''):
        self.status = status
        self.code = code
        # Never echo a provider message, URL, response body, or arbitrary code.
        safe_codes = {'INVALID_TOKEN', 'OAUTH_SCOPE_MISMATCH', 'INVALID_MODULE',
                      'NO_PERMISSION', 'AUTHENTICATION_FAILURE', 'INVALID_DATA',
                      'DUPLICATE_DATA', 'MANDATORY_NOT_FOUND'}
        suffix = f' ({code})' if code in safe_codes else ''
        super().__init__(f'{service} request failed: HTTP {status}{suffix}.')


def read_env(path: Path = ENV_FILE) -> dict[str, str]:
    if not path.is_file():
        raise AccessError('Root .env.local is missing.')
    values: dict[str, str] = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        match = re.fullmatch(r'\s*([A-Z][A-Z0-9_]*)\s*=(.*)', line)
        if not match:
            if line.strip() and not line.lstrip().startswith('#'):
                raise AccessError('Unsupported .env.local syntax; use KEY=value.')
            continue
        key, value = match.groups()
        if key in values:
            raise AccessError(f'Duplicate field in .env.local: {key}.')
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Prevent authorization headers being forwarded to another host.
        return None


class CourseAPI:
    def __init__(self, env_file: Path = ENV_FILE):
        self.env_file = Path(env_file)
        self.opener = build_opener(NoRedirect())
        self.last_status: int | None = None

    def credentials(self) -> dict[str, str]:
        return read_env(self.env_file)

    def authenticate(self, *, force: bool = False) -> str:
        values = self.credentials()
        token = values.get('ZOHO_ACCESS_TOKEN', '')
        try:
            expires_at = int(values.get('ZOHO_ACCESS_TOKEN_EXPIRES_AT', '0'))
        except ValueError:
            expires_at = 0
        if token and not force and (not expires_at or expires_at > time.time() + 120):
            return token
        for key in ('ZOHO_CLIENT_ID', 'ZOHO_CLIENT_SECRET'):
            if not values.get(key):
                raise AccessError(f'Fill {key} in .env.local.')
        if not values.get('ZOHO_REFRESH_TOKEN') and not values.get('ZOHO_GRANT_CODE'):
            raise AccessError('Zoho needs initial authorization: generate a fresh EU Self Client code, save it as ZOHO_GRANT_CODE, then rerun the access check.')
        try:
            result = subprocess.run(
                ['powershell.exe', '-NoProfile', '-NonInteractive', '-File',
                 str(TOKEN_HELPER), '-Action', 'Auto', '-EnvFile', str(self.env_file)],
                capture_output=True, timeout=45, check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise AccessError('Zoho token helper could not run or timed out. Check PowerShell and connectivity.') from None
        if result.returncode:
            # Child output is intentionally suppressed: no credentials or tracebacks.
            raise AccessError('Zoho authorization failed. Check EU Client ID/Secret and use a fresh unused grant code, or check whether the refresh token was revoked.')
        values = self.credentials()
        if not values.get('ZOHO_ACCESS_TOKEN'):
            raise AccessError('Zoho token helper did not save an access token.')
        return values['ZOHO_ACCESS_TOKEN']

    def _request(self, service: str, method: str, url: str,
                 headers: dict[str, str], payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode('utf-8')
        request = Request(url, data=data, headers=headers, method=method)
        self.last_status = None
        try:
            with self.opener.open(request, timeout=30) as response:
                self.last_status = response.status
                raw = response.read()
        except HTTPError as error:
            self.last_status = error.code
            code = ''
            try:
                code = json.loads(error.read()).get('code', '')
            except (ValueError, AttributeError):
                pass
            raise APIError(service, error.code, code) from None
        except (URLError, OSError, TimeoutError):
            note = ' Check the service before retrying a write.' if method != 'GET' else ''
            raise AccessError(f'{service} network request failed.{note}') from None
        if not raw:
            return {}
        try:
            result = json.loads(raw)
        except ValueError:
            raise AccessError(f'{service} returned a non-JSON response.') from None
        if not isinstance(result, dict):
            raise AccessError(f'{service} returned an unexpected response shape.')
        return result

    def cmc_quotes(self, ids: tuple[int, ...] = (1, 1027), convert: str = 'EUR') -> dict:
        if not ids or any(type(item) is not int or item < 1 for item in ids):
            raise AccessError('CoinMarketCap IDs must be positive integers.')
        if not re.fullmatch(r'[A-Z]{3}', convert):
            raise AccessError('Use a three-letter uppercase currency code.')
        key = self.credentials().get('CMC_PRO_API_KEY')
        if not key:
            raise AccessError('Fill CMC_PRO_API_KEY in .env.local.')
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?' + urlencode(
            {'id': ','.join(map(str, ids)), 'convert': convert})
        result = self._request('CoinMarketCap', 'GET', url,
                               {'X-CMC_PRO_API_KEY': key, 'Accept': 'application/json'})
        if result.get('status', {}).get('error_code') != 0:
            raise AccessError('CoinMarketCap rejected the query. Check the key, plan, and quota.')
        for coin_id in ids:
            try:
                float(result['data'][str(coin_id)]['quote'][convert]['price'])
            except (KeyError, TypeError, ValueError):
                raise AccessError('CoinMarketCap response is missing a requested price.') from None
        return result

    def zoho(self, method: str, resource: str, *, params: dict | None = None,
             payload: dict | None = None) -> dict:
        method = method.upper()
        if method not in {'GET', 'POST', 'PUT', 'DELETE'}:
            raise AccessError('Unsupported CRM request method.')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:/[A-Za-z0-9_]+)*', resource):
            raise AccessError('Use a CRM resource such as Leads or Leads/record_id.')
        token = self.authenticate()
        url = 'https://www.zohoapis.eu/crm/v8/' + resource
        if params:
            url += '?' + urlencode(params)
        headers = {'Authorization': 'Zoho-oauthtoken ' + token,
                   'Accept': 'application/json', 'Content-Type': 'application/json'}
        try:
            return self._request('Zoho', method, url, headers, payload)
        except APIError as error:
            if method == 'GET' and error.status == 401 and error.code == 'INVALID_TOKEN':
                headers['Authorization'] = 'Zoho-oauthtoken ' + self.authenticate(force=True)
                return self._request('Zoho', method, url, headers, payload)
            # Never automatically retry creates/updates after uncertain outcomes.
            raise


def check_access(api: CourseAPI) -> dict:
    report = {}
    try:
        api.cmc_quotes()
        report['coinmarketcap'] = {'status': 'verified', 'check': 'BTC and ETH quotes in EUR'}
    except AccessError as error:
        report['coinmarketcap'] = {'status': 'needs_attention', 'detail': str(error)}
    try:
        # Request just one field; never print or persist returned CRM records.
        api.zoho('GET', 'Leads', params={'fields': 'Last_Name', 'per_page': 1})
        report['zoho_crm'] = {'status': 'verified', 'check': 'EU CRM Leads read access'}
        if not api.credentials().get('ZOHO_REFRESH_TOKEN'):
            report['zoho_crm']['refresh'] = 'missing: unattended token renewal is not ready'
    except AccessError as error:
        report['zoho_crm'] = {'status': 'needs_attention', 'detail': str(error)}
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('status', 'check', 'zoho-auth'))
    args = parser.parse_args()
    api = CourseAPI()
    try:
        if args.command == 'status':
            values = api.credentials()
            print(json.dumps({key: 'filled' if values.get(key) else 'empty' for key in KEYS}, indent=2))
        elif args.command == 'zoho-auth':
            api.authenticate(force=True)
            print('Zoho token saved locally; credential values were not displayed.')
        else:
            report = check_access(api)
            print(json.dumps(report, indent=2))
            return 0 if all(item['status'] == 'verified' for item in report.values()) else 1
    except AccessError as error:
        print(str(error))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
