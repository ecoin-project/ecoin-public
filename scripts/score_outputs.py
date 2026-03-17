import os
import json
import glob
from collections import Counter
from statistics import mean

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, "outputs")


def latest_raw_file():
    files = sorted(glob.glob(os.path.join(OUT_DIR, "raw_*.jsonl")))
    return files[-1] if files else None


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def safe_mean(values):
    return round(mean(values), 2) if values else None


def classify_error(err_text):
    err_text = err_text or ""
    if "insufficient_quota" in err_text:
        return "insufficient_quota"
    if "rate_limit" in err_text:
        return "rate_limit"
    if "429" in err_text:
        return "http_429_other"
    if "401" in err_text:
        return "auth_error"
    if "timeout" in err_text.lower():
        return "timeout"
    return "other"


def main():
    raw_path = latest_raw_file()
    if not raw_path:
        print("No raw file found.")
        return

    rows = load_jsonl(raw_path)
    if not rows:
        print("Raw file is empty.")
        return

    success_rows = [r for r in rows if "error" not in r]
    error_rows = [r for r in rows if "error" in r]

    error_counter = Counter()
    for r in error_rows:
        error_counter[classify_error(r.get("error", ""))] += 1

    all_items = []
    exploration_scores = []
    expansion_scores = []
    parse_error_count = 0

    for r in success_rows:
        output_text = r.get("output_text")
        if not output_text:
            parse_error_count += 1
            continue

        try:
            obj = json.loads(output_text)
        except Exception:
            parse_error_count += 1
            continue

        items = obj.get("items", [])
        all_items.extend(items)

        mode_scores = obj.get("mode_scores", {})
        if isinstance(mode_scores.get("exploration"), (int, float)):
            exploration_scores.append(mode_scores["exploration"])
        if isinstance(mode_scores.get("expansion"), (int, float)):
            expansion_scores.append(mode_scores["expansion"])

    if parse_error_count:
        error_counter["parse_error"] += parse_error_count

    anxiety_counter = Counter()
    solution_counter = Counter()
    agency_counter = Counter()

    delegated_vals = []
    fear_vals = []
    superiority_vals = []
    polarization_vals = []

    for item in all_items:
        label = item.get("anxiety_label")
        if label:
            anxiety_counter[label] += 1

        for s in item.get("solutions_sought", []):
            if s:
                solution_counter[s] += 1

        for h in item.get("delegated_agency_hooks", []):
            if h:
                agency_counter[h] += 1

        scores = item.get("scores", {})
        if isinstance(scores.get("delegated_agency"), (int, float)):
            delegated_vals.append(scores["delegated_agency"])
        if isinstance(scores.get("fear_intensity"), (int, float)):
            fear_vals.append(scores["fear_intensity"])
        if isinstance(scores.get("superiority_intensity"), (int, float)):
            superiority_vals.append(scores["superiority_intensity"])
        if isinstance(scores.get("polarization_risk"), (int, float)):
            polarization_vals.append(scores["polarization_risk"])

    delegated_mean = safe_mean(delegated_vals)
    fear_mean = safe_mean(fear_vals)
    superiority_mean = safe_mean(superiority_vals)
    polarization_mean = safe_mean(polarization_vals)
    exploration_mean = safe_mean(exploration_scores)
    expansion_mean = safe_mean(expansion_scores)

    fixation_proxy = None
    if None not in (fear_mean, delegated_mean, polarization_mean, exploration_mean):
        fixation_proxy = round(
            fear_mean * 0.35
            + delegated_mean * 0.35
            + polarization_mean * 0.20
            + (100 - exploration_mean) * 0.10,
            2
        )

    phase_notes = []
    if fear_mean is not None and exploration_mean is not None and fear_mean > exploration_mean:
        phase_notes.append("Fear exceeds exploration.")
    if delegated_mean is not None and delegated_mean >= 60:
        phase_notes.append("Delegated agency remains elevated.")

    if fixation_proxy is None:
        dominant_mode = None
    elif fixation_proxy >= 60:
        dominant_mode = "fixation leaning"
    else:
        dominant_mode = "exploratory leaning"

    all_failed = len(success_rows) == 0

    summary = {
        "week_id": rows[0]["batch_id"][:8] if rows and rows[0].get("batch_id") else None,
        "source_batch_id": rows[0]["batch_id"] if rows and rows[0].get("batch_id") else None,
        "n_runs_total": len(rows),
        "n_runs_success": len(success_rows),
        "n_runs_error": len(error_rows),
        "error_types": dict(error_counter),
        "item_level_summary": {
            "n_items_total": len(all_items),
            "anxiety_labels_top": anxiety_counter.most_common(5),
            "solutions_sought_top": solution_counter.most_common(5),
            "delegated_agency_hooks_top": agency_counter.most_common(5),
        },
        "score_summary": {
            "delegated_agency_mean": delegated_mean,
            "fear_intensity_mean": fear_mean,
            "superiority_intensity_mean": superiority_mean,
            "polarization_risk_mean": polarization_mean,
            "exploration_mean": exploration_mean,
            "expansion_mean": expansion_mean,
        },
        "phase_estimate": {
            "dominant_mode": dominant_mode,
            "fixation_proxy": fixation_proxy,
            "notes": phase_notes,
        },
        "method_notes": (
            ["Summary unavailable because all runs failed."]
            if all_failed else
            [
                "Counts are derived from model-generated observations.",
                "This is not a direct corpus frequency measurement."
            ]
        ),
    }

    source_batch_id = summary["source_batch_id"] or "unknown_batch"
    summary_path = os.path.join(OUT_DIR, f"weekly_summary_{source_batch_id}.json")
    latest_summary_path = os.path.join(OUT_DIR, "latest_summary.json")

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with open(latest_summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Wrote: {summary_path}")
    print(f"Wrote: {latest_summary_path}")


if __name__ == "__main__":
    main()
