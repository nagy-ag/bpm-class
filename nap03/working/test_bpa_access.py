"""Offline checks for credential handling and request retry safety."""
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from bpa_access import APIError, AccessError, CourseAPI, NoRedirect, read_env


class AccessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = Path(self.temp.name) / '.env.local'
        self.env.write_text('CMC_PRO_API_KEY=fake-cmc\nZOHO_CLIENT_ID=fake-client\n'
                            'ZOHO_CLIENT_SECRET="fake-secret"\nZOHO_ACCESS_TOKEN=fake-access\n'
                            'ZOHO_REFRESH_TOKEN=fake-refresh\n', encoding='utf-8')
        self.api = CourseAPI(self.env)

    def test_env_values_are_literal_and_duplicates_are_rejected(self):
        self.assertEqual(read_env(self.env)['ZOHO_CLIENT_SECRET'], 'fake-secret')
        with self.env.open('a', encoding='utf-8') as output:
            output.write('ZOHO_CLIENT_ID=duplicate\n')
        with self.assertRaises(AccessError):
            read_env(self.env)

    def test_expired_token_refreshes_without_secrets_in_arguments(self):
        with self.env.open('a', encoding='utf-8') as output:
            output.write('ZOHO_ACCESS_TOKEN_EXPIRES_AT=1\n')
        def refresh(command, **kwargs):
            self.assertNotIn('fake-secret', command)
            self.assertNotIn('fake-refresh', command)
            self.env.write_text(self.env.read_text().replace('fake-access', 'fresh-access'))
            return subprocess.CompletedProcess(command, 0)
        with patch('bpa_access.subprocess.run', side_effect=refresh) as runner:
            self.assertEqual(self.api.authenticate(), 'fresh-access')
            runner.assert_called_once()

    def test_rejected_read_refreshes_once(self):
        self.api.authenticate = Mock(side_effect=['expired-access', 'fresh-access'])
        self.api._request = Mock(side_effect=[APIError('Zoho', 401, 'INVALID_TOKEN'), {'data': []}])
        self.assertEqual(self.api.zoho('GET', 'Leads'), {'data': []})
        self.assertEqual(self.api._request.call_count, 2)
        self.api.authenticate.assert_called_with(force=True)

    def test_write_is_never_automatically_retried(self):
        self.api.authenticate = Mock(return_value='expired-access')
        self.api._request = Mock(side_effect=APIError('Zoho', 401, 'INVALID_TOKEN'))
        with self.assertRaises(APIError):
            self.api.zoho('POST', 'Leads', payload={'data': []})
        self.assertEqual(self.api._request.call_count, 1)

    def test_cmc_key_stays_out_of_url(self):
        self.api._request = Mock(return_value={'status': {'error_code': 0}, 'data': {
            '1': {'quote': {'EUR': {'price': 1}}}}})
        self.api.cmc_quotes((1,))
        args = self.api._request.call_args.args
        self.assertNotIn('fake-cmc', args[2])
        self.assertEqual(args[3]['X-CMC_PRO_API_KEY'], 'fake-cmc')

    def test_http_error_does_not_echo_response_secrets(self):
        raw = json.dumps({'code': 'fake-secret', 'message': 'fake-secret'}).encode()
        self.api.opener.open = Mock(side_effect=HTTPError('https://example.invalid', 400, 'fake-secret', {}, io.BytesIO(raw)))
        with self.assertRaises(APIError) as caught:
            self.api._request('Zoho', 'GET', 'https://www.zohoapis.eu', {})
        self.assertNotIn('fake-secret', str(caught.exception))

    def test_redirects_and_non_crm_resources_are_rejected(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.invalid'))
        with self.assertRaises(AccessError):
            self.api.zoho('GET', '../oauth/v2/token')


if __name__ == '__main__':
    unittest.main()
