import json
import os


# === JSON-HELPER ===

_JSON_PATH = "daten.json"

def json_read(key):
    return json_get_all().get(key)

def json_get_all():
    if not os.path.exists(_JSON_PATH):
        return None
    with open(_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def json_write(key, value):
    data = {}
    if os.path.exists(_JSON_PATH):
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[key] = value
    with open(_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def json_delete(key):
    if not os.path.exists(_JSON_PATH):
        return
    with open(_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if key in data:
        del data[key]
        with open(_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

