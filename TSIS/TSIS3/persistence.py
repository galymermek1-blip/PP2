import json
import os

BASE_DIR = os.path.dirname(__file__)

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "medium"
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        except:
            pass
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_score(name, score, distance):
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)