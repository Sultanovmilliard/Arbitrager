import aiohttp
import asyncio
import logging

from aiogram import Bot

BYBIT_P2P_URL = "https://api2.bybit.com/fiat/otc/item/online"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}


async def fetch_bybit(session, amount_rub: int, side: str):
    payload = {
        "userId": "",
        "tokenId": "USDT",
        "currencyId": "RUB",
        "payment": [],
        "side": side,
        "size": 10,
        "page": 1,
        "amount": str(amount_rub),
        "authMaker": False,
        "canTrade": True
    }
    try:
        async with session.post(BYBIT_P2P_URL, headers=HEADERS, json=payload, timeout=10) as response:
            data = await response.json()
            return data.get("result", {}).get("items", [])
    except Exception as e:
        logging.warning(f"Ошибка при запросе к ByBit: {e}")
        return []


def format_deal_notification(amount_rub: int, seller_nick: str, buyer_nick: str,
                             seller_price: float, buyer_price: float,
                             profit_percent: float, profit_rub: float) -> str:
    seller_link = f"https://www.bybit.com/user/{seller_nick}"
    buyer_link = f"https://www.bybit.com/user/{buyer_nick}"

    return (
        f"📊 Арбитраж найден по условиям ({amount_rub:,} ₽)\n\n"
        f"👤 [Продавец]({seller_link})       🧑 [Покупатель]({buyer_link})\n"
        f"🌕 Купить USDT: {seller_price:.2f} ₽         🌑 Продать USDT: {buyer_price:.2f} ₽\n\n"
        f"🌗 Спред: 🟢 +{profit_percent:.2f}% (профит ~{profit_rub:,.0f} ₽)"
    )


async def check_arbitrage(bot: Bot, user_id: int, amount_rub: int):
    async with aiohttp.ClientSession() as session:
        buy_offers = await fetch_bybit(session, amount_rub, side="Buy")
        sell_offers = await fetch_bybit(session, amount_rub, side="Sell")

        if not buy_offers or not sell_offers:
            logging.warning("Не удалось получить данные с ByBit.")
            return

        best_seller = sell_offers[0]
        best_buyer = buy_offers[0]

        seller_price = float(best_seller["price"])
        buyer_price = float(best_buyer["price"])

        profit_percent = ((buyer_price - seller_price) / seller_price) * 100
        profit_rub = (buyer_price - seller_price) * (amount_rub / seller_price)

        if profit_percent >= 3:
            seller_nick = best_seller.get("nickName", "unknown_seller")
            buyer_nick = best_buyer.get("nickName", "unknown_buyer")

            text = format_deal_notification(
                amount_rub=amount_rub,
                seller_nick=seller_nick,
                buyer_nick=buyer_nick,
                seller_price=seller_price,
                buyer_price=buyer_price,
                profit_percent=profit_percent,
                profit_rub=profit_rub
            )

            await bot.send_message(user_id, text, parse_mode="Markdown")
