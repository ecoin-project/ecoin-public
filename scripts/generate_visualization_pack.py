"""Generate ECOIN Visualization Pack v0.3 artifacts.

This script is intentionally downstream of observation and scoring. It reads the
existing CSV outputs, stores complete weekly observation vectors first, and then
renders visualization-specific projections from those stored vectors.
"""

import argparse
import csv
import json
import os
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_INPUT = os.path.join(ROOT, "outputs", "master_summary.csv")
DEFAULT_OUT_DIR = os.path.join(ROOT, "outputs")

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

TREND_COLUMNS = [
    ("mean_fear_intensity", "fear"),
    ("mean_delegated_agency", "delegated agency"),
    ("mean_exploration", "exploration"),
    ("mean_fixation_proxy", "fixation proxy"),
    ("mean_pressure_gradient_score", "pressure gradient"),
]

ADAPTIVE_COLUMNS = ["mean_exploration", "mean_expansion"]
PRESSURE_COLUMNS = [
    "mean_fear_intensity",
    "mean_delegated_agency",
    "mean_fixation_proxy",
    "mean_preference_pressure_score",
    "mean_shortcut_risk_score",
    "mean_emotional_delegation_score",
    "mean_pressure_gradient_score",
]


def to_float(value: object) -> Optional[float]:
    try:
        if value == "" or value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def batch_date(batch_id: str) -> Optional[datetime]:
    token = (batch_id or "").split("_", 1)[0]
    try:
        return datetime.strptime(token, "%Y%m%d")
    except ValueError:
        return None


def mean_values(vector: Dict[str, float], columns: Iterable[str]) -> Optional[float]:
    values = [vector[column] for column in columns if column in vector]
    if not values:
        return None
    return sum(values) / len(values)


def read_master_summary(path: str) -> List[Dict[str, str]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input CSV not found: {path}")
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def observation_vector(row: Dict[str, str]) -> Dict[str, float]:
    vector = {}
    for column in OBSERVATION_VECTOR_COLUMNS:
        value = to_float(row.get(column))
        if value is not None:
            vector[column] = value
    return vector


def build_vector_rows(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    vector_rows = []
    for source_order, row in enumerate(rows):
        batch_id = row.get("batch_id", "")
        vector = observation_vector(row)
        if not vector:
            continue
        dt = batch_date(batch_id)
        adaptive_state = mean_values(vector, ADAPTIVE_COLUMNS)
        pressure_state = mean_values(vector, PRESSURE_COLUMNS)
        vector_rows.append(
            {
                "batch_id": batch_id,
                "date": "" if dt is None else dt.date().isoformat(),
                "source_order": source_order,
                "observation_vector": vector,
                "observation_dimensions": list(vector.keys()),
                "adaptive_state": adaptive_state,
                "pressure_state": pressure_state,
                "dominant_mode": row.get("dominant_mode", ""),
                "dominant_pressure_mode": row.get("dominant_pressure_mode", ""),
                "top_anxiety_label_1": row.get("top_anxiety_label_1", ""),
                "top_solution_mode_1": row.get("top_solution_mode_1", ""),
            }
        )
    return sorted(vector_rows, key=lambda r: (r["date"] == "", r["date"], r["source_order"]))


def write_observation_vectors(vector_rows: List[Dict[str, object]], path: str) -> None:
    fieldnames = [
        "batch_id",
        "date",
        "observation_vector_json",
        "observation_dimensions",
        "adaptive_state",
        "pressure_state",
        "dominant_mode",
        "dominant_pressure_mode",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in vector_rows:
            writer.writerow(
                {
                    "batch_id": row["batch_id"],
                    "date": row["date"],
                    "observation_vector_json": json.dumps(row["observation_vector"], sort_keys=True),
                    "observation_dimensions": ";".join(row["observation_dimensions"]),
                    "adaptive_state": "" if row["adaptive_state"] is None else round(row["adaptive_state"], 4),
                    "pressure_state": "" if row["pressure_state"] is None else round(row["pressure_state"], 4),
                    "dominant_mode": row["dominant_mode"],
                    "dominant_pressure_mode": row["dominant_pressure_mode"],
                }
            )


def plot_indicator_trends(vector_rows: List[Dict[str, object]], path: str) -> None:
    x = list(range(len(vector_rows)))
    labels = [str(row["date"] or row["batch_id"]) for row in vector_rows]
    plt.figure(figsize=(12, 6))
    for column, label in TREND_COLUMNS:
        values = [row["observation_vector"].get(column) for row in vector_rows]
        plt.plot(x, values, marker="o", linewidth=2, label=label)
    plt.xticks(x, labels, rotation=35, ha="right")
    plt.ylim(0, 100)
    plt.xlabel("week")
    plt.ylabel("score")
    plt.title("ECOIN weekly indicator trends")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def plot_state_space(vector_rows: List[Dict[str, object]], path: str) -> None:
    points = [row for row in vector_rows if row["adaptive_state"] is not None and row["pressure_state"] is not None]
    if len(points) < 2:
        raise ValueError("Need at least two projected observations for state-space trajectory.")
    x = [row["adaptive_state"] for row in points]
    y = [row["pressure_state"] for row in points]
    labels = [str(row["date"] or row["batch_id"]) for row in points]
    plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.plot(x, y, color="#1f77b4", linewidth=2, marker="o")
    for idx in range(len(points) - 1):
        ax.annotate("", xy=(x[idx + 1], y[idx + 1]), xytext=(x[idx], y[idx]), arrowprops={"arrowstyle": "->", "color": "#1f77b4", "lw": 1.4})
    for idx, label in enumerate(labels):
        ax.annotate(label, (x[idx], y[idx]), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.scatter([x[0]], [y[0]], s=90, color="#2ca02c", zorder=3, label="start")
    ax.scatter([x[-1]], [y[-1]], s=90, color="#d62728", zorder=3, label="latest")
    ax.set_title("ECOIN state-space trajectory (v0.3 projection)")
    ax.set_xlabel("adaptive / exploratory state")
    ax.set_ylabel("pressure / delegated state")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def write_dashboard(vector_rows: List[Dict[str, object]], path: str) -> None:
    latest = vector_rows[-1]
    previous = vector_rows[-2] if len(vector_rows) > 1 else None
    vector = latest["observation_vector"]
    lines = [
        "# ECOIN latest weekly dashboard summary",
        "",
        f"- Batch: `{latest['batch_id']}`",
        f"- Date: `{latest['date']}`",
        f"- Observation dimensions stored: {len(latest['observation_dimensions'])}",
        f"- Dominant mode: {latest['dominant_mode'] or 'n/a'}",
        f"- Dominant pressure mode: {latest['dominant_pressure_mode'] or 'n/a'}",
        f"- Top anxiety label: {latest['top_anxiety_label_1'] or 'n/a'}",
        f"- Top solution mode: {latest['top_solution_mode_1'] or 'n/a'}",
        "",
        "## Indicator snapshot",
        "",
        "| indicator | latest | change vs previous |",
        "| --- | ---: | ---: |",
    ]
    for column, label in TREND_COLUMNS:
        latest_value = vector.get(column)
        previous_value = None if previous is None else previous["observation_vector"].get(column)
        delta = None if latest_value is None or previous_value is None else latest_value - previous_value
        lines.append(f"| {label} | {latest_value:.2f} | {'n/a' if delta is None else f'{delta:+.2f}'} |")
    lines.extend([
        "",
        "## Projection note",
        "",
        "The dashboard is generated after the complete multidimensional observation vector is written. The adaptive and pressure coordinates are visualization projections only, not changes to the observation schema or scoring logic.",
        "",
    ])
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ECOIN Visualization Pack v0.3 artifacts.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Existing master summary CSV to read.")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="Directory for generated visualization artifacts.")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    rows = read_master_summary(args.input)
    vector_rows = build_vector_rows(rows)
    if not vector_rows:
        raise ValueError("No valid observation vectors found in input CSV.")

    vector_path = os.path.join(args.out_dir, "observation_vectors_v0_3.csv")
    trend_path = os.path.join(args.out_dir, "weekly_indicator_trends_v0_3.png")
    trajectory_path = os.path.join(args.out_dir, "state_space_trajectory_v0_3.png")
    dashboard_path = os.path.join(args.out_dir, "latest_weekly_dashboard_summary.md")

    write_observation_vectors(vector_rows, vector_path)
    plot_indicator_trends(vector_rows, trend_path)
    plot_state_space(vector_rows, trajectory_path)
    write_dashboard(vector_rows, dashboard_path)

    print(f"Wrote observation vectors: {vector_path}")
    print(f"Wrote weekly indicator trend chart: {trend_path}")
    print(f"Wrote state-space trajectory chart: {trajectory_path}")
    print(f"Wrote latest dashboard summary: {dashboard_path}")


if __name__ == "__main__":
    main()
