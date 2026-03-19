import os
import csv
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, "outputs")
MASTER_SUMMARY_PATH = os.path.join(OUT_DIR, "master_summary.csv")
PLOT_PATH = os.path.join(OUT_DIR, "summary_trends.png")


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main():
    if not os.path.exists(MASTER_SUMMARY_PATH):
        print(f"master_summary.csv not found: {MASTER_SUMMARY_PATH}")
        return

    rows = []
    with open(MASTER_SUMMARY_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("master_summary.csv is empty.")
        return

    batch_ids = [row.get("batch_id", "") for row in rows]

    fear = [to_float(row.get("mean_fear_intensity")) for row in rows]
    delegated = [to_float(row.get("mean_delegated_agency")) for row in rows]
    exploration = [to_float(row.get("mean_exploration")) for row in rows]
    fixation = [to_float(row.get("mean_fixation_proxy")) for row in rows]

    x = list(range(len(batch_ids)))

    plt.figure(figsize=(10, 6))
    plt.plot(x, fear, marker="o", label="mean_fear_intensity")
    plt.plot(x, delegated, marker="o", label="mean_delegated_agency")
    plt.plot(x, exploration, marker="o", label="mean_exploration")
    plt.plot(x, fixation, marker="o", label="mean_fixation_proxy")

    plt.xticks(x, batch_ids, rotation=45, ha="right")
    plt.ylim(0, 100)
    plt.xlabel("batch_id")
    plt.ylabel("score")
    plt.title("ECOIN Weekly Observation Trends")
    plt.legend()
    plt.tight_layout()

    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    print(f"Wrote: {PLOT_PATH}")


if __name__ == "__main__":
    main()
