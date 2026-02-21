import os
import json
from datetime import datetime

# 出力フォルダ作成
os.makedirs("outputs", exist_ok=True)

timestamp = datetime.utcnow().isoformat()

data = {
    "timestamp": timestamp,
    "structural_score": 0.0,
    "note": "Weekly structural observation seed"
}

filename = f"outputs/observation_{timestamp}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"Created {filename}")
