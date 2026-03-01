import os
import json
import time
import uuid
from datetime import datetime, timezone
from openai import OpenAI

N_RUNS = int(os.getenv("N_RUNS", "20"))
MODEL = os.getenv("MODEL", "gpt-4.1-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

ROOT = os.path.dirname(os.path.dirname(__file__))
PROMPT_PATH = os.path.join(ROOT, "prompts", "fixed_prompt.json")
OUT_DIR = os.path.join(ROOT, "outputs")

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def load_prompt():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)

def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    ensure_dirs()
    prompt = load_prompt()

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    batch_id = f"{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
    out_path = os.path.join(OUT_DIR, f"raw_{batch_id}.jsonl")

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
                "output_text": output_text,
            })

        except Exception as e:
            latency = time.time() - t0
            rows.append({
                "run_id": run_id,
                "batch_id": batch_id,
                "ts_utc": utc_now(),
                "model": MODEL,
                "temperature": TEMPERATURE,
                "latency_sec": latency,
                "error": str(e),
            })

        time.sleep(0.4)

    write_jsonl(out_path, rows)
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()
