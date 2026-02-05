import json
from datetime import datetime

LOG_FILE = "logs/audit_log.json"

def log_event(action, filename):
    entry = {
        "timestamp": str(datetime.now()),
        "action": action,
        "file": filename
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)
