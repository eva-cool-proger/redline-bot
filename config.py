import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Токен бота не найден! Убедитесь, что он есть в файле .env")

# Пути к файлам
DB_NAME = "redline.sqlite3"
CONTENT_FILE = "data.json"