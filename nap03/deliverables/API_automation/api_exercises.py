"""Course exercise logic shared by local checks and the actual Colab notebook.

Only fictional .example identities are accepted. Never retries a write. A failed
write reserves its identity in memory until a person reconciles the CRM result.
"""
from datetime import datetime, timezone
import math
import re

from bpa_access import AccessError

SAMPLE = {
    'Last_Name': 'Teszt', 'First_Name': 'API', 'Company': 'Atlas Market',
    'Email': 'api.teszt@example.com', 'Lead_Source': 'API',
    'Description': 'Oktatási rekord, a harmadik napon Colabból hoztam létre.',
}
MINI = {
    'Last_Name': 'Kovács', 'First_Name': 'BPA', 'Company': 'Duna Minta Kft',
    'Email': 'bpa.kovacs@dunaminta.example', 'Lead_Source': 'API',
    'Description': 'Fiktív üzleti példa: érdeklődés egy automatizált készletjelentés iránt.',
}


def now():
    return datetime.now(timezone.utc).isoformat()


def validate_lead(lead):
    required = {'Last_Name', 'Company', 'Email', 'Lead_Source', 'Description'}
    if not required <= lead.keys() or any(not lead[key] for key in required):
        raise AccessError('Missing required fictional course lead fields.')
    if not re.fullmatch(r'[a-z0-9.]+@(?:[a-z0-9]+\.example|example\.com)', lead['Email']):
        raise AccessError('Use a reserved fictional example email identity.')
    if lead['Lead_Source'] != 'API':
        raise AccessError('These API exercises require API as Lead Source.')


def find_exact(api, email):
    # Search may return punctuation variants: independently compare the identity.
    result = api.zoho('GET', 'Leads/search', params={
        'email': email, 'fields': 'id,First_Name,Last_Name,Company,Email,Lead_Source,Description',
        'per_page': 200,
    })
    if result.get('info', {}).get('more_records'):
        raise AccessError('Identity search was truncated; reconcile before writing.')
    return [row for row in result.get('data', []) if row.get('Email', '').lower() == email.lower()]


def check_fields(row, lead):
    if any(row.get(key) != value for key, value in lead.items()):
        raise AccessError('Existing/readback course lead fields differ; inspect CRM before retrying.')


def create_verified(api, lead, attempts):
    validate_lead(lead)
    identity = lead['Email']
    existing = find_exact(api, identity)
    if len(existing) > 1:
        raise AccessError('Multiple records share the fictional identity; reconcile before writing.')
    if existing:
        check_fields(existing[0], lead)
        return {'outcome': 'existing_exact_record', 'created_this_run': False,
                'record_id': existing[0]['id'], 'fields': dict(lead), 'checked_at': now()}
    if identity in attempts:
        raise AccessError('A write was already attempted for this identity; reconcile CRM before retrying.')
    attempts[identity] = {'state': 'attempted_requires_reconciliation', 'at': now()}
    result = api.zoho('POST', 'Leads', payload={'data': [lead], 'trigger': []})
    http_status = api.last_status
    rows = result.get('data', [])
    if http_status != 201 or len(rows) != 1:
        raise AccessError('Expected HTTP201 and one CRM result; reconcile before retrying.')
    item = rows[0]
    record_id = item.get('details', {}).get('id', '')
    if item.get('status') != 'success' or item.get('code') != 'SUCCESS' or not re.fullmatch(r'\d+', record_id):
        raise AccessError('CRM did not confirm one successful record ID; reconcile before retrying.')
    attempts[identity].update(state='created_pending_readback', record_id=record_id)
    readback = api.zoho('GET', 'Leads/' + record_id).get('data', [])
    if len(readback) != 1 or readback[0].get('id') != record_id:
        raise AccessError('Exact CRM readback missing; do not resubmit.')
    check_fields(readback[0], lead)
    attempts[identity]['state'] = 'verified'
    return {'outcome': 'created_and_verified', 'created_this_run': True,
            'http_status': http_status, 'record_id': record_id, 'fields': dict(lead), 'checked_at': now()}


def finite_positive(value):
    if isinstance(value, bool):
        raise AccessError('Price/threshold must be a finite positive number.')
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise AccessError('Price/threshold must be a finite positive number.') from None
    if not math.isfinite(number) or number <= 0:
        raise AccessError('Price/threshold must be a finite positive number.')
    return number


def above_threshold(price, threshold):
    return finite_positive(price) > finite_positive(threshold)


def fetch_btc(api):
    result = api.cmc_quotes((1,), 'EUR')
    return {'price_eur': finite_positive(result['data']['1']['quote']['EUR']['price']),
            'provider_timestamp': result.get('status', {}).get('timestamp'), 'fetched_at': now()}


def run_chain(api, threshold, run_label, attempts):
    if not re.fullmatch(r'[a-z0-9]{1,32}', run_label):
        raise AccessError('Use a stable lowercase alphanumeric exercise run label.')
    threshold = finite_positive(threshold)
    quote = fetch_btc(api)  # fresh request for each manual execution
    identity = f'bpa.btc.{run_label}@example.com'
    before = find_exact(api, identity)
    if before:
        raise AccessError('This chain run identity already exists; review it instead of creating again.')
    report = dict(quote, threshold_eur=threshold, condition='price > threshold', run_label=run_label)
    if above_threshold(quote['price_eur'], threshold):
        price = quote['price_eur']
        lead = {'Last_Name': f'ÁRJELZÉS BTC {price:,.0f} EUR',
                'Company': 'Árfigyelő automatizmus', 'Email': identity, 'Lead_Source': 'API',
                'Description': f'Oktatási jelzés: BTC {price:.2f} EUR > {threshold:.2f} EUR.'}
        report.update(branch='positive', crm_write_attempted=True,
                      crm=create_verified(api, lead, attempts))
    else:
        after = find_exact(api, identity)
        if after:
            raise AccessError('Unexpected record appeared during negative check; reconcile CRM.')
        report.update(branch='negative', crm_write_attempted=False,
                      matching_records_before=0, matching_records_after=0)
    return report
