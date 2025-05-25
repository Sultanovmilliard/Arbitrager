import os

# Вставь свой токен Telegram-бота
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7623579455:AAHl_qRDh3Qcz9YRBhPRR7aXasIheVVYtzw"

# Значения сумм, которые будут в кнопках
AVAILABLE_AMOUNTS = [10000, 20000, 50000, 100000]

# Минимальный спред, с которого начинается уведомление
MIN_PROFIT_PERCENT = 3.0

# Интервал проверки (в секундах)
CHECK_INTERVAL = 60
