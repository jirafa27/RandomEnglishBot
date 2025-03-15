import os
from dotenv import load_dotenv


load_dotenv()


ENV = os.getenv("ENV")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
