"""Run nap01's BTC/ETH exercise without putting the key in a URL or artifact."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "nap03" / "working"))
from bpa_access import AccessError, CourseAPI


def main():
    response = CourseAPI().cmc_quotes((1, 1027), "EUR")
    output = ROOT / "nap01" / "working" / "cmc_exercise"
    output.mkdir(exist_ok=True)
    (output / "response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
    observation = {
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "currency": "EUR",
        "authentication": "HTTP header; key loaded from ignored local store",
        "public_demo": "In-app browser attempt returned net::ERR_BLOCKED_BY_CLIENT",
        "quotes": [{"id": coin, "symbol": response["data"][str(coin)]["symbol"],
                    "price": response["data"][str(coin)]["quote"]["EUR"]["price"],
                    "json_path": f"data.{coin}.quote.EUR.price"} for coin in (1, 1027)],
    }
    (output / "observation.json").write_text(json.dumps(observation, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(observation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except AccessError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
