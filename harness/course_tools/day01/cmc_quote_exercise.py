"""Run nap01's BTC/ETH exercise without putting the key in a URL or artifact."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())
sys.path.insert(0, str(ROOT / 'harness/course_tools/day03'))
from bpa_access import AccessError, CourseAPI


def main():
    response = CourseAPI().cmc_quotes((1, 1027), "EUR")
    output = ROOT / '.bpa/work/nap01/working/cmc_exercise'
    output.mkdir(parents=True, exist_ok=True)
    (output / "response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
    observation = {
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "currency": "EUR",
        "authentication": "HTTP header; key loaded from ignored local store",
        "public_demo": "Browser demonstration is not tested by this API helper",
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
