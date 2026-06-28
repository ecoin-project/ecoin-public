"""Generate ECOIN data artifacts from existing weekly summary/trend data.

This script is intentionally downstream of observation and scoring. It reads the
existing CSV outputs, writes complete weekly observation vectors first, and then
writes derived state-space trajectory coordinates from those stored vectors.
No prompt, scoring-schema, workflow, or chart-image artifacts are changed here.
"""

import argparse
import csv
import json
import os
from datetime import datetime
from typing import Dict, Iterable, List, Optional

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
SUPPORTED_DOWNSTREAM_VISUALIZATIONS = [
    "2d_projection",
    "pca",
    "umap",
    "radar_chart",
    "trajectory_plot",
    "clustering",
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


def difference(vector: Dict[str, float], left_column: str, right_column: str) -> Optional[float]:
    if left_column not in vector or right_column not in vector:
        return None
    return vector[left_column] - vector[right_column]


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
                "fixation_exploration_balance": difference(vector, "mean_fixation_proxy", "mean_exploration"),
                "delegation_exploration_balance": difference(vector, "mean_delegated_agency", "mean_exploration"),
                "dominant_mode": row.get("dominant_mode", ""),
                "dominant_pressure_mode": row.get("dominant_pressure_mode", ""),
                "top_anxiety_label_1": row.get("top_anxiety_label_1", ""),
                "top_solution_mode_1": row.get("top_solution_mode_1", ""),
            }
        )
    return sorted(vector_rows, key=lambda r: (r["date"] == "", r["date"], r["source_order"]))


def rounded(value: object) -> object:
    return "" if value is None else round(float(value), 4)


def write_observation_vectors(vector_rows: List[Dict[str, object]], path: str) -> None:
    fieldnames = ["batch_id", "date", *OBSERVATION_VECTOR_COLUMNS, "observation_vector_json", "observation_dimensions", "dominant_mode", "dominant_pressure_mode"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in vector_rows:
            vector = row["observation_vector"]
            writer.writerow({
                "batch_id": row["batch_id"],
                "date": row["date"],
                **{column: rounded(vector.get(column)) for column in OBSERVATION_VECTOR_COLUMNS},
                "observation_vector_json": json.dumps(vector, sort_keys=True),
                "observation_dimensions": ";".join(row["observation_dimensions"]),
                "dominant_mode": row["dominant_mode"],
                "dominant_pressure_mode": row["dominant_pressure_mode"],
            })


def write_state_space_trajectory(vector_rows: List[Dict[str, object]], path: str) -> None:
    fieldnames = ["batch_id", "date", "observation_vector_json", "observation_dimensions", "supported_downstream_visualizations", "projection_name", "adaptive_state", "pressure_state", "fixation_exploration_balance", "delegation_exploration_balance", "dominant_mode", "dominant_pressure_mode"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in vector_rows:
            if row["adaptive_state"] is None or row["pressure_state"] is None:
                continue
            writer.writerow({
                "batch_id": row["batch_id"],
                "date": row["date"],
                "observation_vector_json": json.dumps(row["observation_vector"], sort_keys=True),
                "observation_dimensions": ";".join(row["observation_dimensions"]),
                "supported_downstream_visualizations": ";".join(SUPPORTED_DOWNSTREAM_VISUALIZATIONS),
                "projection_name": "legacy_adaptive_pressure_2d",
                "adaptive_state": rounded(row["adaptive_state"]),
                "pressure_state": rounded(row["pressure_state"]),
                "fixation_exploration_balance": rounded(row["fixation_exploration_balance"]),
                "delegation_exploration_balance": rounded(row["delegation_exploration_balance"]),
                "dominant_mode": row["dominant_mode"],
                "dominant_pressure_mode": row["dominant_pressure_mode"],
            })


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
        "## Data artifact note",
        "",
        "This dashboard is generated after the complete multidimensional observation vector CSV is written. The adaptive and pressure coordinates are downstream state-space projections only; this does not change the observation schema, scoring logic, fixed prompts, or scheduled OpenAI workflow.",
        "",
    ])
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ECOIN data artifacts from existing weekly summary/trend data.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Existing master summary CSV to read.")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="Directory for generated data artifacts.")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    rows = read_master_summary(args.input)
    vector_rows = build_vector_rows(rows)
    if not vector_rows:
        raise ValueError("No valid observation vectors found in input CSV.")

    vector_path = os.path.join(args.out_dir, "observation_vectors_v0_3.csv")
    trajectory_path = os.path.join(args.out_dir, "state_space_trajectory_v0_3.csv")
    dashboard_path = os.path.join(args.out_dir, "latest_weekly_dashboard_summary.md")

    write_observation_vectors(vector_rows, vector_path)
    write_state_space_trajectory(vector_rows, trajectory_path)
    write_dashboard(vector_rows, dashboard_path)

    print(f"Wrote observation vectors: {vector_path}")
    print(f"Wrote state-space trajectory CSV: {trajectory_path}")
    print(f"Wrote latest dashboard summary: {dashboard_path}")


if __name__ == "__main__":
    main()
