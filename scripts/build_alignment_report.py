import os
import csv
import json
from math import sqrt

ROOT = os.path.dirname(os.path.dirname(__file__))
INPUT_PATH = os.path.join(ROOT, "outputs", "combined_normalized_trends.csv")
OUT_DIR = os.path.join(ROOT, "outputs")
REPORT_PATH = os.path.join(OUT_DIR, "alignment_report.json")

MARKET_COLUMNS = ["BTC", "GOLD", "USDJPY", "VIX", "SP500"]


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def read_combined_csv():
    if not os.path.exists(INPUT_PATH):
        print(f"combined_normalized_trends.csv not found: {INPUT_PATH}")
        return [], {}

    with open(INPUT_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return [], {}

    dates = [row["date"] for row in rows]
    columns = [c for c in rows[0].keys() if c != "date"]

    series = {}
    for col in columns:
        points = []
        for row in rows:
            value = to_float(row.get(col))
            if value is not None:
                points.append((row["date"], value))
        if points:
            series[col] = points

    return dates, series


def build_change_map(points, eps=1e-9):
    """
    Returns:
      {
        end_date: {
          "delta": float,
          "direction": -1 | 0 | 1
        }
      }
    """
    result = {}
    if len(points) < 2:
        return result

    sorted_points = sorted(points, key=lambda x: x[0])

    for i in range(1, len(sorted_points)):
        prev_date, prev_value = sorted_points[i - 1]
        curr_date, curr_value = sorted_points[i]
        delta = curr_value - prev_value

        if delta > eps:
            direction = 1
        elif delta < -eps:
            direction = -1
        else:
            direction = 0

        result[curr_date] = {
            "delta": delta,
            "direction": direction,
        }

    return result


def pearson(xs, ys):
    if len(xs) < 2 or len(xs) != len(ys):
        return None

    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = sqrt(sum((y - my) ** 2 for y in ys))

    if den_x == 0 or den_y == 0:
        return None

    return num / (den_x * den_y)


def overlap_level_series(left_points, right_points):
    left_map = {d: v for d, v in left_points}
    right_map = {d: v for d, v in right_points}

    common_dates = sorted(set(left_map.keys()) & set(right_map.keys()))
    xs = [left_map[d] for d in common_dates]
    ys = [right_map[d] for d in common_dates]

    return common_dates, xs, ys


def same_week_direction_match(left_changes, right_changes):
    common_dates = sorted(set(left_changes.keys()) & set(right_changes.keys()))
    if not common_dates:
        return {
            "n_pairs": 0,
            "match_ratio": None,
            "matches": 0,
            "mismatches": 0,
            "flat_pairs": 0,
        }

    matches = 0
    mismatches = 0
    flat_pairs = 0

    for d in common_dates:
        ldir = left_changes[d]["direction"]
        rdir = right_changes[d]["direction"]

        if ldir == 0 or rdir == 0:
            flat_pairs += 1

        if ldir == rdir:
            matches += 1
        else:
            mismatches += 1

    ratio = matches / len(common_dates) if common_dates else None

    return {
        "n_pairs": len(common_dates),
        "match_ratio": ratio,
        "matches": matches,
        "mismatches": mismatches,
        "flat_pairs": flat_pairs,
    }


def lag_1_direction_match(left_changes, right_changes):
    """
    Simple one-step lag:
    compares left change at current shared date with right change at previous shared date.
    """
    common_dates = sorted(set(left_changes.keys()) & set(right_changes.keys()))
    if len(common_dates) < 2:
        return {
            "n_pairs": 0,
            "match_ratio": None,
            "matches": 0,
            "mismatches": 0,
            "flat_pairs": 0,
        }

    matches = 0
    mismatches = 0
    flat_pairs = 0
    n_pairs = 0

    for i in range(1, len(common_dates)):
        current_date = common_dates[i]
        prev_date = common_dates[i - 1]

        ldir = left_changes[current_date]["direction"]
        rdir = right_changes[prev_date]["direction"]

        if ldir == 0 or rdir == 0:
            flat_pairs += 1

        if ldir == rdir:
            matches += 1
        else:
            mismatches += 1

        n_pairs += 1

    ratio = matches / n_pairs if n_pairs else None

    return {
        "n_pairs": n_pairs,
        "match_ratio": ratio,
        "matches": matches,
        "mismatches": mismatches,
        "flat_pairs": flat_pairs,
    }


def build_pair_report(left_name, right_name, left_points, right_points):
    level_dates, xs, ys = overlap_level_series(left_points, right_points)
    level_corr = pearson(xs, ys)

    left_changes = build_change_map(left_points)
    right_changes = build_change_map(right_points)

    same_week = same_week_direction_match(left_changes, right_changes)
    lag_1 = lag_1_direction_match(left_changes, right_changes)

    notes = []
    if same_week["match_ratio"] is None:
        notes.append("Not enough overlapping change points for same-week direction comparison.")
    if lag_1["match_ratio"] is None:
        notes.append("Not enough overlapping change points for lag-1 direction comparison.")
    if level_corr is None:
        notes.append("Not enough overlapping level points for level correlation.")

    return {
        "left": left_name,
        "right": right_name,
        "overlap_dates": level_dates,
        "n_overlap_level_points": len(level_dates),
        "level_correlation": level_corr,
        "same_week_direction_match": same_week,
        "lag_1_direction_match": lag_1,
        "notes": notes,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    _, series = read_combined_csv()
    if not series:
        print("No valid series found.")
        return

    discourse_columns = [c for c in series.keys() if c not in MARKET_COLUMNS]
    market_columns = [c for c in MARKET_COLUMNS if c in series]

    reports = []
    for dcol in discourse_columns:
        for mcol in market_columns:
            reports.append(
                build_pair_report(
                    left_name=dcol,
                    right_name=mcol,
                    left_points=series[dcol],
                    right_points=series[mcol],
                )
            )

    result = {
        "report_type": "provisional_alignment_report",
        "source_file": os.path.basename(INPUT_PATH),
        "market_columns": market_columns,
        "discourse_columns": discourse_columns,
        "pairs": reports,
        "notes": [
            "This report is exploratory and provisional.",
            "Direction match is not evidence of causation.",
            "Early-week counts can be too small for stable inference.",
        ],
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Wrote: {REPORT_PATH}")


if __name__ == "__main__":
    main()
