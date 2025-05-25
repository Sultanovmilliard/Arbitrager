import asyncio
import logging
from aiogram import Bot
from config import CHECK_INTERVAL, MIN_PROFIT_PERCENT

# 💡 Псевдо-функция: тут ты подставишь свой реальный ByBit API запрос
async def get_bybit_arbitrage_opportunity(amount: int):
    """
    Возвращает сделку с профитом выше порога, если найдена.
    Формат: {"price": ..., "seller": ..., "profit": ...}
    """
    # Здесь должен быть запрос к API ByBit
    # Для отладки — просто имитируем профит
    import random
    fake_profit = round(random.uniform(1, 5), 2)
    if fake_profit >= MIN_PROFIT_PERCENT:
        return {
            "price": 89.5,
            "seller": "test_seller",
            "profit": fake_profit
        }
    return None

# Словарь активных пользователей и их выбранных сумм
user_amounts = {}

async def start_arbitrage_monitoring(bot: Bot):
    while True:
        for user_id, amount in user_amounts.items():
            try:
                result = await get_bybit_arbitrage_opportunity(amount)
                if result:
                    text = (
                        f"💰 Арбитраж найден!\n\n"
                        f"Продавец: {result['seller']}\n"
                        f"Курс: {result['price']} ₽/USDT\n"
                        f"Профит: {result['profit']}%"
                    )
                    await bot.send_message(user_id, text)
            except Exception as e:
                logging.exception(f"Ошибка при проверке арбитража для {user_id}: {e}")
        await asyncio.sleep(CHECK_INTERVAL)
