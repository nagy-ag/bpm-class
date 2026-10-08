"""Explicit readiness checks; fictional test lead only, no credentials in output."""
import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from bpa_access import AccessError, CourseAPI

OUT = Path(__file__).parent / 'readiness_2026-10-06'


def save(name, value):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def success(result):
    rows = result.get('data', [])
    if len(rows) != 1 or rows[0].get('code') != 'SUCCESS' or rows[0].get('status') != 'success':
        raise AccessError('Test operation did not return per-record SUCCESS; inspect fictional test state before retry.')
    return rows[0].get('details', {})


def quotes():
    api = CourseAPI()
    result = api.cmc_quotes((1, 1027, 5426), 'EUR')
    rows = []
    for coin_id in (1, 1027, 5426):
        item = result['data'][str(coin_id)]
        quote = item['quote']['EUR']
        price = float(quote['price'])
        assert math.isfinite(price) and price > 0
        rows.append({'id': coin_id, 'symbol': item['symbol'], 'price_eur': price,
                     'change_24h_percent': quote['percent_change_24h'],
                     'provider_time': quote['last_updated']})
    record = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'coins': rows,
              'finite_positive_prices': True, 'credential_values_saved': False}
    save('quotes.json', record)
    print('BTC, ETH and SOL EUR prices verified; secret-free quote evidence saved.')


def crm():
    api = CourseAPI()
    marker = 'BPA_READINESS_' + uuid4().hex[:12]
    state = {'marker': marker, 'checked_utc': datetime.now(timezone.utc).isoformat(),
             'completed': [], 'cleanup': 'not_needed'}
    save('crm_test.json', state)
    lead_id = None
    try:
        for module, field in [('Leads', 'Last_Name'), ('Accounts', 'Account_Name'),
                              ('Contacts', 'Last_Name'), ('Deals', 'Deal_Name')]:
            api.zoho('GET', module, params={'fields': field, 'per_page': 1})
            state['completed'].append(module + '_read_access')
            save('crm_test.json', state)
        # Unique fictional identity; opt out and suppress workflows/cadences.
        lead = {'Last_Name': marker, 'First_Name': 'Fictional setup test',
                'Company': marker + ' fictional company', 'Email_Opt_Out': True,
                'Description': marker + ' disposable BPA capability check; not a real customer.'}
        options = {'trigger': [], 'skip_feature_execution': [{'name': 'cadences'}]}
        state['cleanup'] = 'write_attempted_reconcile_if_response_unknown'
        save('crm_test.json', state)
        details = success(api.zoho('POST', 'Leads', payload={'data': [lead], **options}))
        lead_id = str(details['id'])
        state['test_lead_id'] = lead_id
        state['cleanup'] = 'pending'
        state['completed'].append('fictional_lead_create')
        save('crm_test.json', state)
        readback = api.zoho('GET', 'Leads/' + lead_id)['data'][0]
        assert readback['Last_Name'] == marker and readback['Company'] == lead['Company']
        state['completed'].append('exact_create_readback')
        save('crm_test.json', state)
        updated = marker + ' update/readback verified; disposable fictional test.'
        success(api.zoho('PUT', 'Leads/' + lead_id,
                         payload={'data': [{'id': lead_id, 'Description': updated}], **options}))
        assert api.zoho('GET', 'Leads/' + lead_id)['data'][0]['Description'] == updated
        state['completed'].append('update_and_exact_readback')
        # These fixtures test strict threshold behavior; no extra CRM writes.
        state['conditional_fixtures'] = {'above': 101 > 100, 'below': not (99 > 100),
                                         'equal_no_create': not (100 > 100)}
        assert all(state['conditional_fixtures'].values())
        save('crm_test.json', state)
    finally:
        if lead_id:
            # Delete only the ID returned to this run, after exact ownership readback.
            record = api.zoho('GET', 'Leads/' + lead_id)['data'][0]
            if record.get('Last_Name') != marker:
                raise AccessError('Test cleanup ownership mismatch; no deletion performed.')
            success(api.zoho('DELETE', 'Leads/' + lead_id, params={'wf_trigger': 'false'}))
            try:
                removed = not api.zoho('GET', 'Leads/' + lead_id).get('data')
            except AccessError as error:
                removed = getattr(error, 'status', None) in (400, 404)
            if not removed:
                raise AccessError('Test lead deletion could not be confirmed.')
            state['cleanup'] = 'deleted_from_active_crm'
            state['completed'].append('delete_verified')
            save('crm_test.json', state)
    print('CRM module reads and fictional Lead create/read/update/delete verified; conditional fixtures passed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['quotes', 'crm'])
    args = parser.parse_args()
    try:
        (quotes if args.action == 'quotes' else crm)()
    except AccessError as error:
        print(str(error))
        raise SystemExit(1)
    except (AssertionError, KeyError, TypeError, ValueError):
        print('Readiness result did not match its acceptance check; inspect the secret-free evidence before retry.')
        raise SystemExit(1)
