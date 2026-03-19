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

    plt.figure(figsize=(11, 6))
    plt.plot(x, fear, marker="o", linewidth=2, label="fear")
    plt.plot(x, delegated, marker="o", linewidth=2, label="delegated")
    plt.plot(x, exploration, marker="o", linewidth=2, label="exploration")
    plt.plot(x, fixation, marker="o", linewidth=2, label="fixation")

    plt.xticks(x, batch_ids, rotation=30, ha="right")
    plt.ylim(0, 100)
    plt.xlabel("batch_id")
    plt.ylabel("score")
    plt.title("Weekly observation trends")
    plt.legend(loc="best")
    plt.tight_layout()

    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    print(f"Wrote: {PLOT_PATH}")


if __name__ == "__main__":
    main()
