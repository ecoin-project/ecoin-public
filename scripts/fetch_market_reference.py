import os
import csv
import io
import requests
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, "data", "market_reference.csv")

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
COIN_ID = "bitcoin"
VS_CURRENCY = "usd"

GOLD_API_URL = "https://api.gold-api.com/price/XAU"
FRANKFURTER_URL = "https://api.frankfurter.dev/v1/latest"
VIX_HISTORY_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_SERIES_OBS_URL = "https://api.stlouisfed.org/fred/series/observations"
SP500_SERIES_ID = "SP500"


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


def fetch_usdjpy():
    response = requests.get(
        FRANKFURTER_URL,
        params={
            "base": "USD",
            "symbols": "JPY",
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    rates = data.get("rates", {})
    if "JPY" not in rates:
        raise ValueError("JPY rate not found in Frankfurter response")

    return float(rates["JPY"])


def fetch_latest_vix_close():
    response = requests.get(VIX_HISTORY_URL, timeout=20)
    response.raise_for_status()

    text = response.text
    reader = csv.DictReader(io.StringIO(text))

    rows = list(reader)
    if not rows:
        raise ValueError("No rows found in VIX history CSV")

    last = rows[-1]
    raw_date = last["DATE"].strip()
    value = float(last["CLOSE"])
    date_str = datetime.strptime(raw_date, "%m/%d/%Y").date().isoformat()

    return date_str, value


def fetch_latest_sp500_close():
    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY is not set")

    response = requests.get(
        FRED_SERIES_OBS_URL,
        params={
            "series_id": SP500_SERIES_ID,
            "api_key": FRED_API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 10,
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()

    observations = data.get("observations", [])
    if not observations:
        raise ValueError("No observations found in FRED API response")

    for obs in observations:
        date_str = (obs.get("date") or "").strip()
        value_str = (obs.get("value") or "").strip()

        if not date_str or not value_str or value_str == ".":
            continue

        return date_str, float(value_str)

    raise ValueError("No valid SP500 observations found in FRED API response")


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

    errors = []
    success_count = 0

    try:
        btc_price = fetch_btc_price()
        append_row_if_new(
            date_str=today,
            asset="BTC",
            value=btc_price,
            unit="usd",
            source_note="coingecko_demo_or_public",
            fetched_at_utc=fetched_at_utc,
        )
        success_count += 1
    except Exception as e:
        errors.append(f"BTC fetch failed: {e}")

    try:
        gold_price = fetch_gold_price()
        append_row_if_new(
            date_str=today,
            asset="GOLD",
            value=gold_price,
            unit="usd_per_oz",
            source_note="gold_api_free",
            fetched_at_utc=fetched_at_utc,
        )
        success_count += 1
    except Exception as e:
        errors.append(f"GOLD fetch failed: {e}")

    try:
        usdjpy = fetch_usdjpy()
        append_row_if_new(
            date_str=today,
            asset="USDJPY",
            value=usdjpy,
            unit="jpy_per_usd",
            source_note="frankfurter_public",
            fetched_at_utc=fetched_at_utc,
        )
        success_count += 1
    except Exception as e:
        errors.append(f"USDJPY fetch failed: {e}")

    try:
        vix_date, vix_close = fetch_latest_vix_close()
        append_row_if_new(
            date_str=vix_date,
            asset="VIX",
            value=vix_close,
            unit="index_close",
            source_note="cboe_daily_close_csv",
            fetched_at_utc=fetched_at_utc,
        )
        success_count += 1
    except Exception as e:
        errors.append(f"VIX fetch failed: {e}")

    try:
        sp500_date, sp500_close = fetch_latest_sp500_close()
        append_row_if_new(
            date_str=sp500_date,
            asset="SP500",
            value=sp500_close,
            unit="index_close",
            source_note="fred_sp500_csv",
            fetched_at_utc=fetched_at_utc,
        )
        success_count += 1
    except Exception as e:
        errors.append(f"SP500 fetch failed: {e}")

    if errors:
        print("Market reference warnings:")
        for err in errors:
            print(err)

    if success_count == 0:
        raise RuntimeError("All market reference fetches failed.")


if __name__ == "__main__":
    main()
