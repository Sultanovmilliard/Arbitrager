import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные окружения из файла .env

BOT_TOKEN = os.getenv("BOT_TOKEN")  # токен Telegram-бота

# По умолчанию — порог спреда 3%
DEFAULT_SPREAD_THRESHOLD = float(os.getenv("DEFAULT_SPREAD_THRESHOLD", 3.0))

# Частота проверки арбитража (в секундах)
DEFAULT_CHECK_INTERVAL = int(os.getenv("DEFAULT_CHECK_INTERVAL", 60))

# Прочие параметры, если нужны — например, ID администратора
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))

# Другие настройки, например, API URL ByBit, если хочешь сделать универсально
BYBIT_P2P_API_URL = "https://api.bybit.com/spot/v1/p2p/order-list"
