import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(__file__))

MARKET_PATH = os.path.join(ROOT, "data", "market_reference.csv")
DISCOURSE_PATH = os.path.join(ROOT, "measurements", "discourse_sidecar.csv")

OUT_DIR = os.path.join(ROOT, "outputs")
PLOT_PATH = os.path.join(OUT_DIR, "combined_normalized_trends.png")
MERGED_CSV_PATH = os.path.join(OUT_DIR, "combined_normalized_trends.csv")


def to_float(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_iso_date(value: str):
    if not value:
        return None

    value = value.strip()
    if not value:
        return None

    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        return None


def read_market_series():
    if not os.path.exists(MARKET_PATH):
        print(f"market_reference.csv not found: {MARKET_PATH}")
        return {}

    series = {}

    with open(MARKET_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = to_iso_date(row.get("date", ""))
            asset = row.get("asset", "").strip()
            value = to_float(row.get("value"))

            if not date or not asset or value is None:
                continue

            series.setdefault(asset, []).append((date, value))

    return series


def read_discourse_series():
    if not os.path.exists(DISCOURSE_PATH):
        print(f"discourse_sidecar.csv not found: {DISCOURSE_PATH}")
        return {}

    # ここで重ねたい discourse 側の列を選ぶ
    discourse_columns = [
        "fear_intensity",
        "delegated_agency_intensity",
        "exploration_score",
        "fixation_score",
    ]

    series = {col: [] for col in discourse_columns}

    with open(DISCOURSE_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = to_iso_date(row.get("week_id", ""))

            if not date:
                continue

            for col in discourse_columns:
                value = to_float(row.get(col))
                if value is None:
                    continue
                series[col].append((date, value))

    # 空の系列は落とす
    series = {k: v for k, v in series.items() if v}
    return series


def normalize_series(points):
    points = sorted(points, key=lambda x: x[0])

    if not points:
        return []

    first_value = points[0][1]
    if first_value in (None, 0):
        return []

    normalized = []
    for date, value in points:
        normalized_value = (value / first_value) * 100
        normalized.append((date, normalized_value))

    return normalized


def write_merged_csv(normalized_series):
    all_dates = sorted(
        {
            date
            for points in normalized_series.values()
            for date, _ in points
        }
    )

    series_lookup = {}
    for name, points in normalized_series.items():
        series_lookup[name] = {date: value for date, value in points}

    fieldnames = ["date"] + list(normalized_series.keys())

    with open(MERGED_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)

        for date in all_dates:
            row = [date]
            for name in normalized_series.keys():
                value = series_lookup[name].get(date)
                row.append("" if value is None else round(value, 4))
            writer.writerow(row)

    print(f"Wrote merged csv: {MERGED_CSV_PATH}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    market_series = read_market_series()
    discourse_series = read_discourse_series()

    if not market_series and not discourse_series:
        print("No valid market or discourse data found.")
        return

    # ここで重ねたい market 側の系列を選ぶ
    selected_market_assets = ["BTC", "GOLD", "USDJPY", "VIX", "SP500"]

    combined = {}

    for asset in selected_market_assets:
        if asset in market_series:
            normalized = normalize_series(market_series[asset])
            if normalized:
                combined[asset] = normalized

    for name, points in discourse_series.items():
        normalized = normalize_series(points)
        if normalized:
            combined[name] = normalized

    if not combined:
        print("No valid normalized series found.")
        return

    plt.figure(figsize=(12, 7))

    for name, points in combined.items():
        dates = [p[0] for p in points]
        values = [p[1] for p in points]
        plt.plot(dates, values, marker="o", label=name)

    plt.title("Combined normalized trends (market + discourse)")
    plt.xlabel("date")
    plt.ylabel("index (first point = 100)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    write_merged_csv(combined)

    print(f"Wrote plot: {PLOT_PATH}")


if __name__ == "__main__":
    main()
