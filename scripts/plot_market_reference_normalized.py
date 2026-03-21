import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT, "data", "market_reference.csv")
OUT_DIR = os.path.join(ROOT, "outputs")
PLOT_PATH = os.path.join(OUT_DIR, "market_reference_normalized_trends.png")


def to_float(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_iso_date(value: str):
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except (TypeError, ValueError):
        return None


def main():
    if not os.path.exists(DATA_PATH):
        print(f"market_reference.csv not found: {DATA_PATH}")
        return

    rows = []
    with open(DATA_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("market_reference.csv is empty.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)

    assets = {}
    for row in rows:
        asset = row.get("asset", "").strip()
        raw_date = row.get("date", "").strip()
        date = to_iso_date(raw_date)
        value = to_float(row.get("value"))

        if not asset or not date or value is None:
            continue

        assets.setdefault(asset, []).append((date, value))

    if not assets:
        print("No valid rows found in market_reference.csv.")
        return

    plt.figure(figsize=(10, 6))

    for asset, points in assets.items():
        points = sorted(points, key=lambda x: datetime.fromisoformat(x[0]))

        first_value = points[0][1]
        if first_value in (None, 0):
            continue

        dates = [p[0] for p in points]
        normalized = [(p[1] / first_value) * 100 for p in points]

        plt.plot(dates, normalized, marker="o", label=asset)

    plt.title("Market reference trends (normalized, first point = 100)")
    plt.xlabel("date")
    plt.ylabel("index (first point = 100)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    print(f"Wrote: {PLOT_PATH}")


if __name__ == "__main__":
    main()
