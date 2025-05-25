import aiohttp
import asyncio

BYBIT_API = "https://api.bybit.com/v2/public/tickers?symbol=USDTUSD"

async def fetch_bybit_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(BYBIT_API) as resp:
            data = await resp.json()
            return data

async def check_arbitrage(bot, user_id, amount_rub, spread_threshold):
    data = await fetch_bybit_data()
    # Здесь нужно заменить логику получения цены продавца и покупателя 
    # на реальные данные с ByBit (пример ниже — заглушка)
    # Предположим, data['result'] содержит нужные объявления

    # Пример заглушки для теста
    offers = [
        {
            'seller': '@bybit_seller',
            'buyer': '@bybit_buyer',
            'price_sell': 89.5,
            'price_buy': 93.2,
            'profit_percent': 4.14,
            'profit_rub': (93.2 - 89.5) * amount_rub,
            'url_sell': 'https://t.me/bybit_seller',
            'url_buy': 'https://t.me/bybit_buyer'
        }
    ]

    # Фильтруем по порогу спреда
    profitable_offers = [o for o in offers if o['profit_percent'] >= spread_threshold]

    if profitable_offers:
        # Формируем сообщение с группировкой
        msg = f"📊 Арбитраж найден по условиям ({amount_rub:,} ₽)\n\n"
        for o in profitable_offers:
            msg += (
                f"👤 [Продавец]({o['url_sell']})     🧑 [Покупатель]({o['url_buy']})\n"
                f"🌕 Купить USDT: {o['price_sell']} ₽     🌑 Продать USDT: {o['price_buy']} ₽\n"
                f"🌗 Спред: 🟢 +{o['profit_percent']:.2f}% (профит ~{int(o['profit_rub']):,} ₽)\n\n"
            )
        await bot.send_message(user_id, msg, parse_mode='Markdown')
