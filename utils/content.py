import json
from config import CONTENT_FILE

def get_content() -> dict:
    """Динамически читает JSON-файл при каждом обращении."""
    try:
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("❌ Ошибка парсинга data.json! Проверьте синтаксис.")
        return {}