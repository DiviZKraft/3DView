import os

def save_last_path(path, filename="last_path.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(path)
    except Exception as e:
        print("Не вдалося зберегти шлях:", e)

def load_last_path(filename="last_path.txt"):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception as e:
        print("Не вдалося завантажити шлях:", e)
    return ""
