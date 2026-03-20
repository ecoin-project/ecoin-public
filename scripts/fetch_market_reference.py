import os
import csv
import requests
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, "data", "market_reference.csv")

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
COIN_ID = "bitcoin"
VS_CURRENCY = "usd"

GOLD_API_URL = "https://api.gold-api.com/price/XAU"


def ensure_csv_exists():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "asset", "value", "unit", "source_note", "fetched_at_utc"])


def read_existing_rows():
    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def fetch_btc_price():
    response = requests.get(
        COINGECKO_URL,
        params={
            "ids": COIN_ID,
            "vs_currencies": VS_CURRENCY,
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    if COIN_ID not in data or VS_CURRENCY not in data[COIN_ID]:
        raise ValueError("BTC price not found in CoinGecko response")

    return float(data[COIN_ID][VS_CURRENCY])


def fetch_gold_price():
    response = requests.get(GOLD_API_URL, timeout=20)
    response.raise_for_status()
    data = response.json()

    if "price" not in data:
        raise ValueError("GOLD price not found in gold-api.com response")

    return float(data["price"])


def append_row_if_new(date_str: str, asset: str, value: float, unit: str, source_note: str, fetched_at_utc: str):
    rows = read_existing_rows()
    for row in rows:
        if row.get("date") == date_str and row.get("asset") == asset:
            print(f"Row already exists for {date_str} / {asset}. Skip append.")
            return

    with open(DATA_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, asset, value, unit, source_note, fetched_at_utc])

    print(f"Appended {asset} value for {date_str}: {value}")


def main():
    ensure_csv_exists()

    now_utc = datetime.now(timezone.utc).replace(microsecond=0)
    today = now_utc.date().isoformat()
    fetched_at_utc = now_utc.isoformat().replace("+00:00", "Z")

    btc_price = fetch_btc_price()
    append_row_if_new(
        date_str=today,
        asset="BTC",
        value=btc_price,
        unit="usd",
        source_note="coingecko_demo_or_public",
        fetched_at_utc=fetched_at_utc,
    )

    gold_price = fetch_gold_price()
    append_row_if_new(
        date_str=today,
        asset="GOLD",
        value=gold_price,
        unit="usd_per_oz",
        source_note="gold_api_free",
        fetched_at_utc=fetched_at_utc,
    )


if __name__ == "__main__":
    main()
