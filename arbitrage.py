import asyncio
from aiogram import Bot
import aiohttp

# Словарь для хранения сделок пользователей
user_deals = {}

# Добавить сделку пользователю и запустить таймер, если нужно
async def add_deal_for_user(user_id: int, deal_info: str, bot: Bot):
    if user_id not in user_deals or user_deals[user_id] is None:
        user_deals[user_id] = []
        # Запускаем задачу отправки уведомления через 60 секунд
        asyncio.create_task(send_aggregated_deals(user_id, bot, wait_seconds=60))
    user_deals[user_id].append(deal_info)

# Отправить все сделки одним сообщением и очистить список
async def send_aggregated_deals(user_id: int, bot: Bot, wait_seconds: int = 60):
    await asyncio.sleep(wait_seconds)
    deals = user_deals.get(user_id, [])
    if deals:
        message_text = "📢 Найдены арбитражные сделки:\n\n" + "\n\n".join(deals)
        try:
            await bot.send_message(user_id, message_text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
        # Очистить сделки после отправки
        user_deals[user_id] = []

# Функция проверки арбитража (пример)
async def check_arbitrage(bot: Bot, user_id: int, amount_rub: int):
    # Здесь вставляй свой код для получения данных с API бирж
    # Для примера используем фиктивные данные:
    deals_found = [
        {
            "seller_nick": "seller1",
            "buyer_nick": "buyer1",
            "seller_url": "https://bybit.com/seller1",
            "buyer_url": "https://bybit.com/buyer1",
            "price_buy": 89.5,
            "price_sell": 93.2,
            "profit_percent": 4.14,
            "profit_rub": 2200,
        },
        {
            "seller_nick": "seller2",
            "buyer_nick": "buyer2",
            "seller_url": "https://bybit.com/seller2",
            "buyer_url": "https://bybit.com/buyer2",
            "price_buy": 89.6,
            "price_sell": 92.8,
            "profit_percent": 3.54,
            "profit_rub": 1800,
        }
    ]

    for deal in deals_found:
        text = (
            f"👤 Продавец: [продавец]({deal['seller_url']})     "
            f"🧑 Покупатель: [покупатель]({deal['buyer_url']})\n"
            f"🌕 Купить USDT: {deal['price_buy']:.2f} ₽         "
            f"🌑 Продать USDT: {deal['price_sell']:.2f} ₽\n"
            f"🌗 Спред: 🟢 +{deal['profit_percent']:.2f}% "
            f"(профит ~{deal['profit_rub']} ₽)"
        )
        await add_deal_for_user(user_id, text, bot)
