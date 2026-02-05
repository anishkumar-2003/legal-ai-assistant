import json

KB_FILE = "data/knowledge_base.json"

def update_kb(issue):
    try:
        with open(KB_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[issue] = data.get(issue, 0) + 1

    with open(KB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_kb():
    try:
        with open(KB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
