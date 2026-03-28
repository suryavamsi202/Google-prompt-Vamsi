import json, os
from datetime import datetime

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(input_data: dict, output_data: dict):
    history = load_history()
    history.insert(0, {
        "id": len(history) + 1,
        "timestamp": datetime.now().isoformat(),
        "input_type": input_data.get("input_type", "text"),
        "context": input_data.get("context", "general"),
        "input": input_data,
        "output": output_data
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:50], f, indent=2)
