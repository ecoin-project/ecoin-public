import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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


def to_dt(value: str):
    try:
        return datetime.fromisoformat(value)
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
        dt = to_dt(row.get("date", "").strip())
        value = to_float(row.get("value"))

        if not asset or not dt or value is None:
            continue

        assets.setdefault(asset, []).append((dt, value))

    if not assets:
        print("No valid rows found in market_reference.csv.")
        return

    plt.figure(figsize=(10, 6))
    ax = plt.gca()

    for asset, points in assets.items():
        points = sorted(points, key=lambda x: x[0])

        first_value = points[0][1]
        if first_value in (None, 0):
            continue

        dates = [p[0] for p in points]
        normalized = [(p[1] / first_value) * 100 for p in points]

        ax.plot(dates, normalized, marker="o", label=asset)

    ax.set_title("Market reference trends (normalized, first point = 100)")
    ax.set_xlabel("date")
    ax.set_ylabel("index (first point = 100)")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45, ha="right")

    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    print(f"Wrote: {PLOT_PATH}")


if __name__ == "__main__":
    main()
