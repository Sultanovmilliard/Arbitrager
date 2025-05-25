import aiohttp
import asyncio
from aiogram import Bot

BYBIT_P2P_API = "https://api.bybit.com/spot/v1/public/p2p/order/list"

async def fetch_bybit_p2p_orders(session, side: str, amount: int):
    params = {
        "coin": "USDT",
        "fiat": "RUB",
        "side": side,
        "amount": amount,
        "page": 1,
        "limit": 50,
    }
    async with session.get(BYBIT_P2P_API, params=params, timeout=10) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return data.get("result", {}).get("data", [])

async def get_arbitrage_opportunities(amount: int):
    async with aiohttp.ClientSession() as session:
        sellers = await fetch_bybit_p2p_orders(session, "sell", amount)
        buyers = await fetch_bybit_p2p_orders(session, "buy", amount)

        opportunities = []
        for seller in sellers:
            for buyer in buyers:
                sell_price = float(seller['price'])
                buy_price = float(buyer['price'])
                if buy_price <= sell_price:
                    continue
                profit_percent = (buy_price - sell_price) / sell_price * 100
                if profit_percent < 3:
                    continue
                opportunities.append({
                    "seller_nick": seller["advertiser"]["nickName"],
                    "seller_url": f"https://www.bybit.com/ru-RU/p2p/advertiser/{seller['advertiser']['userId']}",
                    "buyer_nick": buyer["advertiser"]["nickName"],
                    "buyer_url": f"https://www.bybit.com/ru-RU/p2p/advertiser/{buyer['advertiser']['userId']}",
                    "sell_price": sell_price,
                    "buy_price": buy_price,
                    "profit_percent": profit_percent,
                    "amount": amount,
                })
        return opportunities

async def check_and_notify(bot: Bot, user_id: int, amount: int):
    opportunities = await get_arbitrage_opportunities(amount)
    if not opportunities:
        return

    # Формируем единое сообщение с несколькими сделками (умное сгруппирование)
    messages = []
    for opp in opportunities:
        msg = (
            f"👤 Продавец: [{opp['seller_nick']}]({opp['seller_url']})    "
            f"🧑 Покупатель: [{opp['buyer_nick']}]({opp['buyer_url']})\n"
            f"🌕 Купить USDT: {opp['sell_price']:.2f} ₽     "
            f"🌑 Продать USDT: {opp['buy_price']:.2f} ₽\n"
            f"🌗 Спред: 🟢 +{opp['profit_percent']:.2f}% (профит ~{int(opp['profit_percent'] / 100 * opp['amount'])} ₽)\n"
            "------------------------\n"
        )
        messages.append(msg)

    full_message = f"💰 *Арбитраж найден по условиям ({amount} ₽)*\n\n" + "".join(messages)

    await bot.send_message(user_id, full_message, parse_mode="Markdown")
