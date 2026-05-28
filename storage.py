import json
import os

STORAGE_FILE = os.path.join(os.path.dirname(__file__), "user_data.json")

DEFAULT_DATA = {
    "location": "",
    "user_name": "",
    "user_phone": "",
    "contact1": "",
    "contact2": "",
    "contact3": "",
    "blood_group": "",
    "allergies": "",
    "medical_conditions": "",
    "lang": "en",
    "auto_crash_enabled": False,
    "crash_threshold": 25.0,
}

def load_user_data() -> dict:
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return {**DEFAULT_DATA, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_DATA.copy()

def save_user_data(data: dict):
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass
