import csv
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, "outputs")
MASTER_SUMMARY_PATH = os.path.join(OUT_DIR, "master_summary.csv")
PLOT_PATH = os.path.join(OUT_DIR, "state_space_trajectory.png")
CSV_PATH = os.path.join(OUT_DIR, "state_space_trajectory.csv")

# The observation layer is intentionally multidimensional. These columns are
# stored as the canonical state vector before any visualization chooses a
# projection. Do not collapse this list into a fixed two-axis data model.
OBSERVATION_VECTOR_COLUMNS = [
    "mean_fear_intensity",
    "mean_superiority_intensity",
    "mean_delegated_agency",
    "mean_polarization_risk",
    "mean_exploration",
    "mean_expansion",
    "mean_fixation_proxy",
    "mean_preference_pressure_score",
    "mean_shortcut_risk_score",
    "mean_emotional_delegation_score",
    "mean_pressure_gradient_score",
    "mean_pressure_activation",
    "mean_closure_pressure",
    "mean_emotional_offloading",
    "mean_shortcut_normalization",
]

# Visualization projections are downstream choices. The legacy 2D trajectory is
# retained as one projection over the complete observation vector, not as the
# canonical data model.
LEGACY_2D_PROJECTION = {
    "x_axis": {
        "name": "adaptive_state",
        "columns": ["mean_exploration", "mean_expansion"],
        "label": "adaptive / exploratory state (mean exploration + expansion)",
    },
    "y_axis": {
        "name": "pressure_state",
        "columns": [
            "mean_fear_intensity",
            "mean_delegated_agency",
            "mean_fixation_proxy",
            "mean_preference_pressure_score",
            "mean_shortcut_risk_score",
            "mean_emotional_delegation_score",
            "mean_pressure_gradient_score",
        ],
        "label": "pressure / delegated state (mean current pressure indicators)",
    },
}

SUPPORTED_DOWNSTREAM_VISUALIZATIONS = [
    "2d_projection",
    "pca",
    "umap",
    "radar_chart",
    "trajectory_plot",
    "clustering",
]


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean_available(row, columns):
    values = [to_float(row.get(column)) for column in columns]
    values = [value for value in values if value is not None]
    if not values:
        return None
    return sum(values) / len(values)


def batch_date(batch_id):
    token = (batch_id or "").split("_", 1)[0]
    try:
        return datetime.strptime(token, "%Y%m%d")
    except ValueError:
        return None


def difference(row, left_column, right_column):
    left = to_float(row.get(left_column))
    right = to_float(row.get(right_column))
    if left is None or right is None:
        return None
    return left - right


def observation_vector(row):
    """Return the complete numeric observation vector for one weekly row."""
    vector = {}
    for column in OBSERVATION_VECTOR_COLUMNS:
        value = to_float(row.get(column))
        if value is not None:
            vector[column] = value
    return vector


def project_legacy_2d(vector):
    """Project a multidimensional observation vector into the legacy 2D view."""
    x_columns = LEGACY_2D_PROJECTION["x_axis"]["columns"]
    y_columns = LEGACY_2D_PROJECTION["y_axis"]["columns"]

    x_values = [vector[column] for column in x_columns if column in vector]
    y_values = [vector[column] for column in y_columns if column in vector]
    if not x_values or not y_values:
        return None

    return {
        LEGACY_2D_PROJECTION["x_axis"]["name"]: sum(x_values) / len(x_values),
        LEGACY_2D_PROJECTION["y_axis"]["name"]: sum(y_values) / len(y_values),
    }


def read_state_points():
    if not os.path.exists(MASTER_SUMMARY_PATH):
        print(f"master_summary.csv not found: {MASTER_SUMMARY_PATH}")
        return []

    points = []
    with open(MASTER_SUMMARY_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            vector = observation_vector(row)
            projection = project_legacy_2d(vector)
            if projection is None:
                continue

            batch_id = row.get("batch_id", "")
            points.append(
                {
                    "batch_id": batch_id,
                    "date": batch_date(batch_id),
                    "source_order": index,
                    "observation_vector": vector,
                    "observation_dimensions": list(vector.keys()),
                    "projection_name": "legacy_adaptive_pressure_2d",
                    **projection,
                    "fixation_exploration_balance": difference(
                        row, "mean_fixation_proxy", "mean_exploration"
                    ),
                    "delegation_exploration_balance": difference(
                        row, "mean_delegated_agency", "mean_exploration"
                    ),
                    "dominant_mode": row.get("dominant_mode", ""),
                    "dominant_pressure_mode": row.get("dominant_pressure_mode", ""),
                }
            )

    return sorted(points, key=lambda p: (p["date"] is None, p["date"] or datetime.max, p["source_order"]))


def write_csv(points):
    fieldnames = [
        "batch_id",
        "date",
        "observation_vector_json",
        "observation_dimensions",
        "supported_downstream_visualizations",
        "projection_name",
        "adaptive_state",
        "pressure_state",
        "fixation_exploration_balance",
        "delegation_exploration_balance",
        "dominant_mode",
        "dominant_pressure_mode",
    ]
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for point in points:
            writer.writerow(
                {
                    "batch_id": point["batch_id"],
                    "date": "" if point["date"] is None else point["date"].date().isoformat(),
                    "observation_vector_json": json.dumps(point["observation_vector"], sort_keys=True),
                    "observation_dimensions": ";".join(point["observation_dimensions"]),
                    "supported_downstream_visualizations": ";".join(SUPPORTED_DOWNSTREAM_VISUALIZATIONS),
                    "projection_name": point["projection_name"],
                    "adaptive_state": round(point["adaptive_state"], 4),
                    "pressure_state": round(point["pressure_state"], 4),
                    "fixation_exploration_balance": ""
                    if point["fixation_exploration_balance"] is None
                    else round(point["fixation_exploration_balance"], 4),
                    "delegation_exploration_balance": ""
                    if point["delegation_exploration_balance"] is None
                    else round(point["delegation_exploration_balance"], 4),
                    "dominant_mode": point["dominant_mode"],
                    "dominant_pressure_mode": point["dominant_pressure_mode"],
                }
            )
    print(f"Wrote csv: {CSV_PATH}")


def plot(points):
    x_name = LEGACY_2D_PROJECTION["x_axis"]["name"]
    y_name = LEGACY_2D_PROJECTION["y_axis"]["name"]
    x = [point[x_name] for point in points]
    y = [point[y_name] for point in points]
    labels = [point["batch_id"].split("_", 1)[0] for point in points]

    plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.plot(x, y, color="#1f77b4", linewidth=2, marker="o", markersize=6)

    for idx, point in enumerate(points[:-1]):
        ax.annotate(
            "",
            xy=(x[idx + 1], y[idx + 1]),
            xytext=(x[idx], y[idx]),
            arrowprops={"arrowstyle": "->", "color": "#1f77b4", "lw": 1.5, "shrinkA": 6, "shrinkB": 6},
        )

    for idx, label in enumerate(labels):
        ax.annotate(label, (x[idx], y[idx]), textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax.scatter([x[0]], [y[0]], s=90, color="#2ca02c", zorder=3, label="start")
    ax.scatter([x[-1]], [y[-1]], s=90, color="#d62728", zorder=3, label="latest")

    ax.set_title("ECOIN weekly state-space trajectory (legacy 2D projection)")
    ax.set_xlabel(LEGACY_2D_PROJECTION["x_axis"]["label"])
    ax.set_ylabel(LEGACY_2D_PROJECTION["y_axis"]["label"])
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best")
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()
    print(f"Wrote plot: {PLOT_PATH}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    points = read_state_points()
    if len(points) < 2:
        print("Need at least two valid weekly observations for a trajectory plot.")
        return

    write_csv(points)
    plot(points)


if __name__ == "__main__":
    main()
