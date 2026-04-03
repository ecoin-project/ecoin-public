import os
import json
import time
import uuid
import csv
from datetime import datetime, timezone
from openai import OpenAI

N_RUNS = int(os.getenv("N_RUNS", "20"))
MODEL = os.getenv("MODEL", "gpt-4.1-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

ROOT = os.path.dirname(os.path.dirname(__file__))
PROMPT_FILE = os.getenv("PROMPT_FILE", "fixed_prompt.json")
PROMPT_PATH = os.path.join(ROOT, "prompts", PROMPT_FILE)
OUT_DIR = os.path.join(ROOT, "outputs")

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def load_prompt():
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_PATH}")
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)

def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def write_txt(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for i, r in enumerate(rows, 1):
            f.write(f"=== Run {i} ===\n")
            f.write(f"run_id: {r.get('run_id', '')}\n")
            f.write(f"batch_id: {r.get('batch_id', '')}\n")
            f.write(f"ts_utc: {r.get('ts_utc', '')}\n")
            f.write(f"model: {r.get('model', '')}\n")
            f.write(f"temperature: {r.get('temperature', '')}\n")
            f.write(f"latency_sec: {r.get('latency_sec', '')}\n")
            f.write(f"prompt_file: {r.get('prompt_file', '')}\n")

            if "error" in r:
                f.write("error:\n")
                f.write(str(r.get("error", "")) + "\n")
            else:
                f.write("output_text:\n")
                f.write(str(r.get("output_text", "")) + "\n")

            f.write("\n")

def write_csv(path, rows):
    fieldnames = [
        "run_id",
        "batch_id",
        "ts_utc",
        "model",
        "temperature",
        "latency_sec",
        "prompt_file",
        "output_text",
        "error",
    ]

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "run_id": r.get("run_id", ""),
                "batch_id": r.get("batch_id", ""),
                "ts_utc": r.get("ts_utc", ""),
                "model": r.get("model", ""),
                "temperature": r.get("temperature", ""),
                "latency_sec": r.get("latency_sec", ""),
                "prompt_file": r.get("prompt_file", ""),
                "output_text": r.get("output_text", ""),
                "error": r.get("error", ""),
            })

def main():
    ensure_dirs()
    prompt = load_prompt()

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    batch_id = f"{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
    jsonl_path = os.path.join(OUT_DIR, f"raw_{batch_id}.jsonl")
    txt_path = os.path.join(OUT_DIR, f"summary_{batch_id}.txt")
    csv_path = os.path.join(OUT_DIR, f"summary_{batch_id}.csv")
    latest_txt_path = os.path.join(OUT_DIR, "latest_output.txt")
    latest_csv_path = os.path.join(OUT_DIR, "latest_output.csv")

    rows = []

    for i in range(N_RUNS):
        run_id = f"{batch_id}_{i+1:03d}"
        t0 = time.time()

        try:
            resp = client.responses.create(
                model=MODEL,
                temperature=TEMPERATURE,
                input=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                ],
            )

            latency = time.time() - t0
            output_text = getattr(resp, "output_text", None)

            rows.append({
                "run_id": run_id,
                "batch_id": batch_id,
                "ts_utc": utc_now(),
                "model": MODEL,
                "temperature": TEMPERATURE,
                "latency_sec": latency,
                "prompt_file": PROMPT_FILE,
                "output_text": output_text,
            })

        except Exception as e:
            latency = time.time() - t0
            err_text = str(e)

            rows.append({
                "run_id": run_id,
                "batch_id": batch_id,
                "ts_utc": utc_now(),
                "model": MODEL,
                "temperature": TEMPERATURE,
                "latency_sec": latency,
                "prompt_file": PROMPT_FILE,
                "error": err_text,
            })

            if "insufficient_quota" in err_text:
                print("Quota exceeded. Stopping remaining runs.")
                break

        time.sleep(0.4)

    write_jsonl(jsonl_path, rows)
    write_txt(txt_path, rows)
    write_txt(latest_txt_path, rows)
    write_csv(csv_path, rows)
    write_csv(latest_csv_path, rows)

    print(f"Prompt file: {PROMPT_FILE}")
    print(f"Total records: {len(rows)}")
    print(f"Wrote: {jsonl_path}")
    print(f"Wrote: {txt_path}")
    print(f"Wrote: {csv_path}")
    print(f"Wrote: {latest_txt_path}")
    print(f"Wrote: {latest_csv_path}")

if __name__ == "__main__":
    main()
