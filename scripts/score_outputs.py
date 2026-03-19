import json
from pathlib import Path
from collections import Counter
from statistics import mean

SAMPLES_DIR = Path("samples")
OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)

BATCH_ID = "manual_batch_001"
OUTPUT_FILE = OUTPUTS_DIR / f"weekly_summary_{BATCH_ID}.json"


def safe_mean(values):
    return round(mean(values), 2) if values else 0.0


def compute_fixation_proxy(mean_fear, mean_delegated, mean_polarization, mean_exploration):
    value = (
        mean_fear * 0.35
        + mean_delegated * 0.35
        + mean_polarization * 0.20
        + (100 - mean_exploration) * 0.10
    )
    return round(value, 2)


def load_sample_files():
    return sorted(SAMPLES_DIR.glob("sample_*.json"))


def extract_solution_modes(item):
    results = []
    for s in item.get("solutions_sought", []):
        text = s.lower()

        if any(word in text for word in ["app", "dashboard", "tool", "platform", "copilot", "assistant"]):
            results.append("automation")
        if any(word in text for word in ["coach", "course", "training", "framework", "literacy", "guide", "tutorial"]):
            results.append("outsourced expertise")
        if any(word in text for word in ["community", "identity", "early adopter", "builder", "operator"]):
            results.append("identity signaling")
        if any(word in text for word in ["tracker", "map", "score", "calculator", "comparison"]):
            results.append("monitoring")
        if any(word in text for word in ["event", "meetup", "offline", "club", "community-oriented"]):
            results.append("offline/community")

    return results


def main():
    files = load_sample_files()

    all_items = []
    all_exploration = []
    all_expansion = []
    anxiety_counter = Counter()
    solution_counter = Counter()

    for file_path in files:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get("items", [])
        all_items.extend(items)

        mode_scores = data.get("mode_scores", {})
        if "exploration" in mode_scores:
            all_exploration.append(mode_scores["exploration"])
        if "expansion" in mode_scores:
            all_expansion.append(mode_scores["expansion"])

        for item in items:
            label = item.get("anxiety_label")
            if label:
                anxiety_counter[label] += 1

            for mode in extract_solution_modes(item):
                solution_counter[mode] += 1

    fear_values = []
    superiority_values = []
    delegated_values = []
    polarization_values = []

    for item in all_items:
        scores = item.get("scores", {})
        if "fear_intensity" in scores:
            fear_values.append(scores["fear_intensity"])
        if "superiority_intensity" in scores:
            superiority_values.append(scores["superiority_intensity"])
        if "delegated_agency" in scores:
            delegated_values.append(scores["delegated_agency"])
        if "polarization_risk" in scores:
            polarization_values.append(scores["polarization_risk"])

    mean_fear = safe_mean(fear_values)
    mean_superiority = safe_mean(superiority_values)
    mean_delegated = safe_mean(delegated_values)
    mean_polarization = safe_mean(polarization_values)
    mean_exploration = safe_mean(all_exploration)
    mean_expansion = safe_mean(all_expansion)
    mean_fixation_proxy = compute_fixation_proxy(
        mean_fear,
        mean_delegated,
        mean_polarization,
        mean_exploration,
    )

    summary = {
        "batch_id": BATCH_ID,
        "time_window_assumed": "last_3_to_12_months",
        "n_files": len(files),
        "n_items_total": len(all_items),
        "mean_fear_intensity": mean_fear,
        "mean_superiority_intensity": mean_superiority,
        "mean_delegated_agency": mean_delegated,
        "mean_polarization_risk": mean_polarization,
        "mean_exploration": mean_exploration,
        "mean_expansion": mean_expansion,
        "mean_fixation_proxy": mean_fixation_proxy,
        "top_anxiety_labels": [label for label, _ in anxiety_counter.most_common(3)],
        "top_solution_modes": [mode for mode, _ in solution_counter.most_common(3)],
        "source_files": [file_path.name for file_path in files],
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Saved summary to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
