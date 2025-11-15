import os
import json
from datetime import datetime

# Compute project root ONCE
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def write_json_log(session_id, message):
    """Writes structured JSON logs using absolute path."""

    log_dir = os.path.join(PROJECT_ROOT, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_entry = {
        "timestamp": str(datetime.now()),
        "session_id": session_id,
        "message": message,
    }

    log_path = os.path.join(log_dir, f"{session_id}.log.json")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
