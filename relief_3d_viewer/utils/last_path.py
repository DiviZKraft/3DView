import os
import json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".3dviewer_last_path.json")

def save_last_opened_path(path):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"last_path": path}, f)
    except Exception as e:
        print(f"Не вдалося зберегти останній шлях: {e}")

def load_last_opened_path():
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("last_path")
    except Exception as e:
        print(f"Не вдалося завантажити останній шлях: {e}")
        return None