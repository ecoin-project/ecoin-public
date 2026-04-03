import os
import json
import glob
import csv
from collections import Counter
from statistics import mean

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, "outputs")
SAMPLES_DIR = os.path.join(ROOT, "samples")

USE_MANUAL_SAMPLE = os.getenv("USE_MANUAL_SAMPLE", "0") == "1"
MANUAL_BATCH_ID = os.getenv("MANUAL_BATCH_ID", "manual_batch_001")
MASTER_SUMMARY_PATH = os.path.join(OUT_DIR, "master_summary.csv")


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
    lower = err_text.lower()

    if "insufficient_quota" in err_text:
        return "insufficient_quota"
    if "rate_limit" in err_text:
        return "rate_limit"
    if "429" in err_text:
        return "http_429_other"
    if "401" in err_text:
        return "auth_error"
    if "timeout" in lower:
        return "timeout"
    return "other"


def load_manual_samples_as_rows():
    batch_samples_dir = os.path.join(SAMPLES_DIR, MANUAL_BATCH_ID)
    paths = sorted(glob.glob(os.path.join(batch_samples_dir, "sample_*.json")))
    if not paths:
        return None

    rows = []
    for i, path in enumerate(paths, start=1):
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)

        rows.append({
            "run_id": f"manual_sample_{i:03d}",
            "batch_id": MANUAL_BATCH_ID,
            "ts_utc": f"2026-03-18T00:00:{i:02d}+00:00",
            "model": "manual_chat_sample",
            "temperature": 0.2,
            "prompt_file": "manual_sample",
            "output_text": json.dumps(obj, ensure_ascii=False),
            "source_file": os.path.basename(path)
        })

    return rows


def extract_solution_modes(items):
    counter = Counter()
    for item in items:
        for s in item.get("solutions_sought", []):
            text = (s or "").lower()

            if any(word in text for word in [
                "app", "dashboard", "tool", "tracker", "copilot",
                "assistant", "map", "calculator", "platform", "filter"
            ]):
                counter["automation/monitoring"] += 1

            if any(word in text for word in [
                "course", "training", "coach", "framework", "tutorial",
                "literacy", "guide", "explainer", "newsletter"
            ]):
                counter["outsourced expertise"] += 1

            if any(word in text for word in [
                "community", "identity", "early adopter", "builder",
                "operator", "aspirational"
            ]):
                counter["identity signaling"] += 1

            if any(word in text for word in [
                "event", "meetup", "offline", "club", "neighborhood", "group"
            ]):
                counter["offline/community"] += 1

            if any(word in text for word in [
                "planning", "preparedness", "continuity", "resilience",
                "relocation", "retirement"
            ]):
                counter["resilience planning"] += 1

    return counter


def top_n_or_blank(values, n=3):
    result = list(values)[:n]
    while len(result) < n:
        result.append("")
    return result


def append_to_master_summary(summary):
    os.makedirs(OUT_DIR, exist_ok=True)

    headers = [
        "batch_id",
        "time_window_assumed",
        "n_files",
        "n_items_total",
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
        "top_anxiety_label_1",
        "top_anxiety_label_2",
        "top_anxiety_label_3",
        "top_solution_mode_1",
        "top_solution_mode_2",
        "top_solution_mode_3",
        "top_functional_emotion_proxy_1",
        "top_functional_emotion_proxy_2",
        "top_functional_emotion_proxy_3",
        "dominant_mode",
        "dominant_pressure_mode"
    ]

    sidecar_summary = summary.get("sidecar_summary", {})
    top_anxieties = top_n_or_blank(summary.get("top_anxiety_labels", []), 3)
    top_solutions = top_n_or_blank(summary.get("top_solution_modes", []), 3)

    proxy_entries = sidecar_summary.get("top_functional_emotion_proxies", [])
    proxy_labels = []
    for entry in proxy_entries:
        if isinstance(entry, dict):
            proxy_labels.append(entry.get("label", ""))
        elif isinstance(entry, str):
            proxy_labels.append(entry)
    top_proxies = top_n_or_blank(proxy_labels, 3)

    row = {
        "batch_id": summary.get("batch_id", ""),
        "time_window_assumed": summary.get("time_window_assumed", ""),
        "n_files": summary.get("n_files", ""),
        "n_items_total": summary.get("n_items_total", ""),
        "mean_fear_intensity": summary.get("mean_fear_intensity", ""),
        "mean_superiority_intensity": summary.get("mean_superiority_intensity", ""),
        "mean_delegated_agency": summary.get("mean_delegated_agency", ""),
        "mean_polarization_risk": summary.get("mean_polarization_risk", ""),
        "mean_exploration": summary.get("mean_exploration", ""),
        "mean_expansion": summary.get("mean_expansion", ""),
        "mean_fixation_proxy": summary.get("mean_fixation_proxy", ""),
        "mean_preference_pressure_score": sidecar_summary.get("mean_preference_pressure_score", ""),
        "mean_shortcut_risk_score": sidecar_summary.get("mean_shortcut_risk_score", ""),
        "mean_emotional_delegation_score": sidecar_summary.get("mean_emotional_delegation_score", ""),
        "mean_pressure_gradient_score": sidecar_summary.get("mean_pressure_gradient_score", ""),
        "mean_pressure_activation": sidecar_summary.get("mean_pressure_activation", ""),
        "mean_closure_pressure": sidecar_summary.get("mean_closure_pressure", ""),
        "mean_emotional_offloading": sidecar_summary.get("mean_emotional_offloading", ""),
        "mean_shortcut_normalization": sidecar_summary.get("mean_shortcut_normalization", ""),
        "top_anxiety_label_1": top_anxieties[0],
        "top_anxiety_label_2": top_anxieties[1],
        "top_anxiety_label_3": top_anxieties[2],
        "top_solution_mode_1": top_solutions[0],
        "top_solution_mode_2": top_solutions[1],
        "top_solution_mode_3": top_solutions[2],
        "top_functional_emotion_proxy_1": top_proxies[0],
        "top_functional_emotion_proxy_2": top_proxies[1],
        "top_functional_emotion_proxy_3": top_proxies[2],
        "dominant_mode": summary.get("run_diagnostics", {}).get("dominant_mode", ""),
        "dominant_pressure_mode": sidecar_summary.get("dominant_pressure_mode", "")
    }

    existing_batch_ids = set()

    if os.path.exists(MASTER_SUMMARY_PATH):
        with open(MASTER_SUMMARY_PATH, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for existing in reader:
                existing_batch_ids.add(existing.get("batch_id", ""))

    if row["batch_id"] in existing_batch_ids:
        print(f"master_summary.csv already contains batch_id={row['batch_id']}; skip append.")
        return

    write_header = not os.path.exists(MASTER_SUMMARY_PATH)

    with open(MASTER_SUMMARY_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"Updated: {MASTER_SUMMARY_PATH}")


def main():
    if USE_MANUAL_SAMPLE:
        rows = load_manual_samples_as_rows()
        if not rows:
            print("USE_MANUAL_SAMPLE=1 but no manual samples found.")
            return
    else:
        raw_path = latest_raw_file()

        if raw_path:
            rows = load_jsonl(raw_path)
            if not rows:
                print("Raw file is empty.")
                return
        else:
            print("No raw file found.")
            return

    success_rows = [r for r in rows if "error" not in r]
    error_rows = [r for r in rows if "error" in r]

    error_counter = Counter()
    for r in error_rows:
        error_counter[classify_error(r.get("error", ""))] += 1

    all_items = []
    exploration_scores = []
    expansion_scores = []
    pressure_activation_scores = []
    closure_pressure_scores = []
    emotional_offloading_scores = []
    shortcut_normalization_scores = []
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

        sidecar_mode_scores = obj.get("sidecar_mode_scores", {})
        if isinstance(sidecar_mode_scores.get("pressure_activation"), (int, float)):
            pressure_activation_scores.append(sidecar_mode_scores["pressure_activation"])
        if isinstance(sidecar_mode_scores.get("closure_pressure"), (int, float)):
            closure_pressure_scores.append(sidecar_mode_scores["closure_pressure"])
        if isinstance(sidecar_mode_scores.get("emotional_offloading"), (int, float)):
            emotional_offloading_scores.append(sidecar_mode_scores["emotional_offloading"])
        if isinstance(sidecar_mode_scores.get("shortcut_normalization"), (int, float)):
            shortcut_normalization_scores.append(sidecar_mode_scores["shortcut_normalization"])

    if parse_error_count:
        error_counter["parse_error"] += parse_error_count

    anxiety_counter = Counter()
    delegated_hook_counter = Counter()
    emotion_proxy_counter = Counter()
    delegated_agency_mode_counter = Counter()
    shortcut_risk_counter = Counter()

    delegated_vals = []
    fear_vals = []
    superiority_vals = []
    polarization_vals = []

    preference_pressure_vals = []
    shortcut_risk_vals = []
    emotional_delegation_vals = []
    pressure_gradient_vals = []

    for item in all_items:
        label = item.get("anxiety_label")
        if label:
            anxiety_counter[label] += 1

        for h in item.get("delegated_agency_hooks", []):
            if h:
                delegated_hook_counter[h] += 1

        emotion_sidecar = item.get("emotion_mechanism_sidecar", {})
        primary_proxy = emotion_sidecar.get("functional_emotion_proxy_primary")
        if primary_proxy:
            emotion_proxy_counter[primary_proxy] += 1

        for proxy in emotion_sidecar.get("functional_emotion_proxy_secondary", []):
            if proxy:
                emotion_proxy_counter[proxy] += 1

        for mode in emotion_sidecar.get("delegated_agency_mode", []):
            if mode:
                delegated_agency_mode_counter[mode] += 1

        for risk in emotion_sidecar.get("shortcut_risks", []):
            if risk:
                shortcut_risk_counter[risk] += 1

        scores = item.get("scores", {})
        if isinstance(scores.get("delegated_agency"), (int, float)):
            delegated_vals.append(scores["delegated_agency"])
        if isinstance(scores.get("fear_intensity"), (int, float)):
            fear_vals.append(scores["fear_intensity"])
        if isinstance(scores.get("superiority_intensity"), (int, float)):
            superiority_vals.append(scores["superiority_intensity"])
        if isinstance(scores.get("polarization_risk"), (int, float)):
            polarization_vals.append(scores["polarization_risk"])

        if isinstance(scores.get("preference_pressure_score"), (int, float)):
            preference_pressure_vals.append(scores["preference_pressure_score"])
        if isinstance(scores.get("shortcut_risk_score"), (int, float)):
            shortcut_risk_vals.append(scores["shortcut_risk_score"])
        if isinstance(scores.get("emotional_delegation_score"), (int, float)):
            emotional_delegation_vals.append(scores["emotional_delegation_score"])
        if isinstance(scores.get("pressure_gradient_score"), (int, float)):
            pressure_gradient_vals.append(scores["pressure_gradient_score"])

    solution_mode_counter = extract_solution_modes(all_items)

    delegated_mean = safe_mean(delegated_vals)
    fear_mean = safe_mean(fear_vals)
    superiority_mean = safe_mean(superiority_vals)
    polarization_mean = safe_mean(polarization_vals)
    exploration_mean = safe_mean(exploration_scores)
    expansion_mean = safe_mean(expansion_scores)

    preference_pressure_mean = safe_mean(preference_pressure_vals)
    shortcut_risk_mean = safe_mean(shortcut_risk_vals)
    emotional_delegation_mean = safe_mean(emotional_delegation_vals)
    pressure_gradient_mean = safe_mean(pressure_gradient_vals)

    pressure_activation_mean = safe_mean(pressure_activation_scores)
    closure_pressure_mean = safe_mean(closure_pressure_scores)
    emotional_offloading_mean = safe_mean(emotional_offloading_scores)
    shortcut_normalization_mean = safe_mean(shortcut_normalization_scores)

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

    if pressure_activation_mean is None and closure_pressure_mean is None and emotional_offloading_mean is None:
        dominant_pressure_mode = None
    elif (
        pressure_activation_mean is not None
        and closure_pressure_mean is not None
        and pressure_activation_mean >= 65
        and closure_pressure_mean >= 60
    ):
        dominant_pressure_mode = "pressure-driven and closure-leaning"
    elif pressure_activation_mean is not None and pressure_activation_mean >= 60:
        dominant_pressure_mode = "pressure-driven but mixed"
    elif emotional_offloading_mean is not None and emotional_offloading_mean >= 60:
        dominant_pressure_mode = "emotionally offloaded"
    else:
        dominant_pressure_mode = "mixed / exploratory"

    pressure_notes = []
    top_proxy_labels = [label for label, _ in emotion_proxy_counter.most_common(5)]
    top_delegated_modes = [label for label, _ in delegated_agency_mode_counter.most_common(5)]

    if (
        preference_pressure_mean is not None
        and preference_pressure_mean >= 60
        and any(p in top_proxy_labels for p in ["cognitive_overload_escape", "uncertainty_intolerance"])
    ):
        pressure_notes.append("Solution preference narrows under overload and uncertainty pressure.")

    if (
        emotional_delegation_mean is not None
        and emotional_delegation_mean >= 60
        and any(m in top_delegated_modes for m in ["automated", "diagnostic", "interpretive"])
    ):
        pressure_notes.append("Emotional offloading appears elevated in expert-led or automated solution bundles.")

    sidecar_enabled = any([
        preference_pressure_mean is not None,
        shortcut_risk_mean is not None,
        emotional_delegation_mean is not None,
        pressure_gradient_mean is not None,
        pressure_activation_mean is not None,
        closure_pressure_mean is not None,
        emotional_offloading_mean is not None,
        shortcut_normalization_mean is not None,
        len(emotion_proxy_counter) > 0,
        len(delegated_agency_mode_counter) > 0,
        len(shortcut_risk_counter) > 0,
    ])

    if sidecar_enabled:
        sidecar_summary = {
            "enabled": True,
            "mean_preference_pressure_score": preference_pressure_mean,
            "mean_shortcut_risk_score": shortcut_risk_mean,
            "mean_emotional_delegation_score": emotional_delegation_mean,
            "mean_pressure_gradient_score": pressure_gradient_mean,
            "mean_pressure_activation": pressure_activation_mean,
            "mean_closure_pressure": closure_pressure_mean,
            "mean_emotional_offloading": emotional_offloading_mean,
            "mean_shortcut_normalization": shortcut_normalization_mean,
            "top_functional_emotion_proxies": [
                {"label": label, "count": count}
                for label, count in emotion_proxy_counter.most_common(5)
            ],
            "top_delegated_agency_modes": [
                {"label": label, "count": count}
                for label, count in delegated_agency_mode_counter.most_common(5)
            ],
            "top_shortcut_risks": [
                {"label": label, "count": count}
                for label, count in shortcut_risk_counter.most_common(5)
            ],
            "dominant_pressure_mode": dominant_pressure_mode,
            "pressure_notes": pressure_notes,
        }
    else:
        sidecar_summary = {"enabled": False}

    all_failed = len(success_rows) == 0
    batch_id = rows[0]["batch_id"] if rows and rows[0].get("batch_id") else "unknown_batch"

    weekly_summary = {
        "batch_id": batch_id,
        "time_window_assumed": "last_3_to_12_months",
        "n_files": len(rows),
        "n_items_total": len(all_items),
        "mean_fear_intensity": fear_mean,
        "mean_superiority_intensity": superiority_mean,
        "mean_delegated_agency": delegated_mean,
        "mean_polarization_risk": polarization_mean,
        "mean_exploration": exploration_mean,
        "mean_expansion": expansion_mean,
        "mean_fixation_proxy": fixation_proxy,
        "top_anxiety_labels": [label for label, _ in anxiety_counter.most_common(5)],
        "top_solution_modes": [label for label, _ in solution_mode_counter.most_common(5)],
        "sidecar_summary": sidecar_summary,
        "source_files": [r["source_file"] for r in rows if r.get("source_file")],
        "run_diagnostics": {
            "n_runs_total": len(rows),
            "n_runs_success": len(success_rows),
            "n_runs_error": len(error_rows),
            "error_types": dict(error_counter),
            "dominant_mode": dominant_mode,
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

    latest_summary = {
        "batch_id": batch_id,
        "time_window_assumed": "last_3_to_12_months",
        "n_files": len(rows),
        "n_items_total": len(all_items),
        "mean_fear_intensity": fear_mean,
        "mean_superiority_intensity": superiority_mean,
        "mean_delegated_agency": delegated_mean,
        "mean_polarization_risk": polarization_mean,
        "mean_exploration": exploration_mean,
        "mean_expansion": expansion_mean,
        "mean_fixation_proxy": fixation_proxy,
        "mean_preference_pressure_score": sidecar_summary.get("mean_preference_pressure_score"),
        "mean_shortcut_risk_score": sidecar_summary.get("mean_shortcut_risk_score"),
        "mean_emotional_delegation_score": sidecar_summary.get("mean_emotional_delegation_score"),
        "mean_pressure_gradient_score": sidecar_summary.get("mean_pressure_gradient_score"),
        "mean_pressure_activation": sidecar_summary.get("mean_pressure_activation"),
        "mean_closure_pressure": sidecar_summary.get("mean_closure_pressure"),
        "mean_emotional_offloading": sidecar_summary.get("mean_emotional_offloading"),
        "mean_shortcut_normalization": sidecar_summary.get("mean_shortcut_normalization"),
        "top_anxiety_labels": [label for label, _ in anxiety_counter.most_common(3)],
        "top_solution_modes": [label for label, _ in solution_mode_counter.most_common(3)],
        "top_functional_emotion_proxies": [
            entry["label"] for entry in sidecar_summary.get("top_functional_emotion_proxies", [])[:3]
        ],
        "dominant_mode": dominant_mode,
        "dominant_pressure_mode": sidecar_summary.get("dominant_pressure_mode"),
        "method_notes": (
            ["Summary unavailable because all runs failed."]
            if all_failed else
            [
                "Counts are derived from model-generated observations.",
                "This is not a direct corpus frequency measurement."
            ]
        ),
    }

    summary_path = os.path.join(OUT_DIR, f"weekly_summary_{batch_id}.json")
    latest_summary_path = os.path.join(OUT_DIR, "latest_summary.json")

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(weekly_summary, f, ensure_ascii=False, indent=2)

    with open(latest_summary_path, "w", encoding="utf-8") as f:
        json.dump(latest_summary, f, ensure_ascii=False, indent=2)

    append_to_master_summary(weekly_summary)

    print(f"Wrote: {summary_path}")
    print(f"Wrote: {latest_summary_path}")


if __name__ == "__main__":
    main()
