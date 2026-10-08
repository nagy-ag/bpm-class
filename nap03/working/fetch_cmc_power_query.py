"""Approved CMC adaptation: fetch public quotes, then refresh Excel's local query."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from bpa_access import CourseAPI, AccessError

OUT = Path(__file__).parent / 'cmc_power_query'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solana', action='store_true')
    parser.add_argument('--output-dir', type=Path, default=OUT,
                        help='Credential-free snapshot directory for a fresh work copy.')
    args = parser.parse_args()
    out = args.output_dir.resolve()
    ids = (1, 1027, 5426) if args.solana else (1, 1027)
    response = CourseAPI().cmc_quotes(ids, 'EUR')
    payload = {'fetched_utc': datetime.now(timezone.utc).isoformat(),
               'status': response['status'], 'data': response['data']}
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    raw = json.dumps(payload, ensure_ascii=False, indent=2)
    (out / ('fetch_' + stamp + '.json')).write_text(raw, encoding='utf-8')
    pending = out / 'quotes.tmp'
    pending.write_text(raw, encoding='utf-8')
    pending.replace(out / 'quotes.json')
    print(json.dumps({'ids': ids, 'fetched_utc': payload['fetched_utc'],
                      'provider_timestamp': payload['status']['timestamp'],
                      'output': str(out / 'quotes.json')}, indent=2))

if __name__ == '__main__':
    try:
        main()
    except AccessError as error:
        raise SystemExit(str(error)) from None
