import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

LOCAL_FOLDER = os.getenv("LOCAL_FOLDER")
REMOTE_FOLDER = os.getenv("REMOTE_FOLDER")
YA_TOKEN = os.getenv("YA_TOKEN")
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL", "60"))
LOG_FILE = os.getenv("LOG_FILE")

DATE_FORMAT = "%d.%m.%Y"
