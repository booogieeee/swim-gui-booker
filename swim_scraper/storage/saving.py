import json
from pathlib import Path

"""
reminder format:
"id": {
    "days": days,
    "location": location,
    "time": time
}
"""

BASE_DIRECTORY = Path(__file__).resolve().parent # gets projects directory to access file
FILE = BASE_DIRECTORY/"reminders.json"

def load_reminders():
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data

def save_reminders(reminders):
    with open(FILE, "w") as f:
        json.dump(reminders, f, indent=2)