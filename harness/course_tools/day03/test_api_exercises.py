"""Offline failure-path tests; no live service calls or credentials."""
import io
import json
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from bpa_access import AccessError, CourseAPI
from api_exercises import SAMPLE, above_threshold, create_verified, run_chain
from colab_runtime import MemoryCourseAPI


class FakeAPI:
    def __init__(self, existing=None, write_error=None, mismatch=False):
        self.rows = list(existing or [])
        self.write_error = write_error
        self.mismatch = mismatch
        self.writes = 0
        self.last_status = None

    def zoho(self, method, resource, *, params=None, payload=None):
        if method == 'POST':
            self.writes += 1
            assert payload['trigger'] == []
            if self.write_error:
                raise self.write_error
            self.rows.append(dict(payload['data'][0], id='123456'))
            self.last_status = 201
            return {'data': [{'status': 'success', 'code': 'SUCCESS', 'details': {'id': '123456'}}]}
        self.last_status = 200
        rows = self.rows
        if resource.endswith('/search'):
            rows = [row for row in rows if row.get('Email') == params['email']]
        elif self.mismatch:
            rows = [dict(row, Company='Wrong fixture') for row in rows]
        return {'data': rows}

    def cmc_quotes(self, ids, convert):
        return {'status': {'error_code': 0, 'timestamp': 'fixture'},
                'data': {'1': {'quote': {'EUR': {'price': 100}}}}}


class ExercisesTests(unittest.TestCase):
    def test_create_success_exact_readback_then_reuse(self):
        api = FakeAPI()
        attempts = {}
        self.assertTrue(create_verified(api, SAMPLE, attempts)['created_this_run'])
        self.assertFalse(create_verified(api, SAMPLE, attempts)['created_this_run'])
        self.assertEqual(api.writes, 1)
        self.assertEqual(attempts[SAMPLE['Email']]['state'], 'verified')

    def test_uncertain_write_cannot_be_retried(self):
        api = FakeAPI(write_error=AccessError('Fixture uncertain network write.'))
        attempts = {}
        with self.assertRaises(AccessError):
            create_verified(api, SAMPLE, attempts)
        with self.assertRaisesRegex(AccessError, 'already attempted'):
            create_verified(api, SAMPLE, attempts)
        self.assertEqual(api.writes, 1)

    def test_conflicting_or_duplicate_identity_stops_before_write(self):
        for rows in ([dict(SAMPLE, id='1', Company='Wrong')], [dict(SAMPLE, id='1'), dict(SAMPLE, id='2')]):
            api = FakeAPI(existing=rows)
            with self.assertRaises(AccessError):
                create_verified(api, SAMPLE, {})
            self.assertEqual(api.writes, 0)

    def test_bad_readback_preserves_created_reservation(self):
        api = FakeAPI(mismatch=True)
        attempts = {}
        with self.assertRaises(AccessError):
            create_verified(api, SAMPLE, attempts)
        self.assertEqual(api.writes, 1)
        self.assertEqual(attempts[SAMPLE['Email']]['state'], 'created_pending_readback')

    def test_non_fictional_address_refused(self):
        api = FakeAPI()
        with self.assertRaises(AccessError):
            create_verified(api, dict(SAMPLE, Email='person@real.test'), {})
        self.assertEqual(api.writes, 0)

    def test_positive_negative_and_equality(self):
        for threshold, expected in ((99, True), (100, False), (101, False)):
            api = FakeAPI()
            report = run_chain(api, threshold, 'fixture', {})
            self.assertEqual(report['crm_write_attempted'], expected)
            self.assertEqual(api.writes, int(expected))
            if expected:
                self.assertTrue(report['crm']['fields']['Last_Name'].startswith('ÁRJELZÉS BTC'))
            else:
                self.assertEqual(report['matching_records_after'], 0)

    def test_invalid_prices_and_thresholds_rejected(self):
        for value in (None, True, 0, -1, float('nan'), float('inf'), 'bad'):
            with self.assertRaises(AccessError):
                above_threshold(value, 100)
            with self.assertRaises(AccessError):
                above_threshold(100, value)

    def test_memory_refresh_keeps_refresh_token_and_never_reads_env(self):
        api = MemoryCourseAPI({'ZOHO_CLIENT_ID': 'fixture-id', 'ZOHO_CLIENT_SECRET': 'fixture-secret',
                               'ZOHO_REFRESH_TOKEN': 'fixture-refresh'})
        response = Mock()
        response.read.return_value = json.dumps({'api_domain': 'https://www.zohoapis.eu',
            'access_token': 'fixture-access', 'expires_in': 3600}).encode()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        api.opener.open = Mock(return_value=response)
        with patch('bpa_access.read_env', side_effect=AssertionError('Must not read env')):
            self.assertEqual(api.authenticate(), 'fixture-access')
            self.assertEqual(api.authenticate(), 'fixture-access')
        self.assertEqual(api.opener.open.call_count, 1)
        request = api.opener.open.call_args.args[0]
        self.assertEqual(request.full_url, 'https://accounts.zoho.eu/oauth/v2/token')
        self.assertNotIn('fixture-secret', request.full_url)
        self.assertIn(b'grant_type=refresh_token', request.data)
        self.assertEqual(api.credentials()['ZOHO_REFRESH_TOKEN'], 'fixture-refresh')
        api.clear()
        self.assertEqual(api.credentials(), {})

    def test_token_error_suppresses_provider_body_and_no_retry(self):
        api = MemoryCourseAPI({'ZOHO_CLIENT_ID': 'fixture-id', 'ZOHO_CLIENT_SECRET': 'fixture-secret'})
        api.opener.open = Mock(side_effect=HTTPError('https://accounts.zoho.eu/oauth/v2/token',
             400, 'bad', {}, io.BytesIO(b'fixture-secret')))
        with self.assertRaises(AccessError) as error:
            api.authorize('fixture-grant')
        self.assertNotIn('fixture-secret', str(error.exception))
        self.assertEqual(api.opener.open.call_count, 1)

    def test_http_status_captured_on_shared_transport(self):
        api = CourseAPI()
        response = Mock(status=201)
        response.read.return_value = b'{"data":[]}'
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        api.opener.open = Mock(return_value=response)
        api._request('Zoho', 'POST', 'https://www.zohoapis.eu/crm/v8/Leads', {}, {})
        self.assertEqual(api.last_status, 201)


if __name__ == '__main__':
    unittest.main()
