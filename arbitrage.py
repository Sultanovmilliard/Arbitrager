import aiohttp

BYBIT_P2P_API = "https://api.bybit.com/spot/v1/p2p/order-list"

async def fetch_bybit_p2p_orders(side: str, amount_rub: int, pay_types="Tinkoff", page=1, rows=50):
    params = {
        "side": side,               # "sell" — продают USDT (чтобы купить USDT), "buy" — покупают USDT (чтобы продать USDT)
        "payment_method": pay_types,
        "asset": "USDT",
        "fiat": "RUB",
        "page": page,
        "rows": rows,
        "amount": amount_rub
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(BYBIT_P2P_API, params=params) as resp:
            data = await resp.json()
            if data.get("retCode") != 0:
                return []
            return data["result"]["data"]

async def check_arbitrage(bot, user_id, amount_rub, spread_threshold_percent):
    # Получаем продавцов (продают USDT, чтобы купить рубли)
    sellers = await fetch_bybit_p2p_orders(side="sell", amount_rub=amount_rub)
    # Получаем покупателей (покупают USDT, чтобы продать рубли)
    buyers = await fetch_bybit_p2p_orders(side="buy", amount_rub=amount_rub)

    if not sellers or not buyers:
        await bot.send_message(user_id, "Объявления с ByBit P2P не найдены.")
        return

    profitable_offers = []

    # Перебираем пары продавец-покупатель
    for s_offer in sellers:
        s_adv = s_offer["advertisement"]
        s_price = float(s_adv["price"])
        s_nick = s_adv["advertiserNickName"]
        s_url = f"https://t.me/{s_nick}"

        for b_offer in buyers:
            b_adv = b_offer["advertisement"]
            b_price = float(b_adv["price"])
            b_nick = b_adv["advertiserNickName"]
            b_url = f"https://t.me/{b_nick}"

            # Спред в процентах
            if b_price <= s_price:
                continue  # Нет арбитража, покупатель не платит больше, чем продавец просит

            spread = ((b_price - s_price) / s_price) * 100
            profit_rub = (b_price - s_price) * amount_rub

            if spread >= spread_threshold_percent:
                profitable_offers.append({
                    "seller_nick": s_nick,
                    "seller_url": s_url,
                    "buyer_nick": b_nick,
                    "buyer_url": b_url,
                    "price_sell": s_price,
                    "price_buy": b_price,
                    "spread": spread,
                    "profit_rub": profit_rub
                })

    if not profitable_offers:
        await bot.send_message(user_id, f"Арбитраж не найден по сумме {amount_rub:,} ₽ и порогу {spread_threshold_percent}%.")
        return

    # Формируем сообщение с группировкой всех выгодных сделок
    msg = f"📊 Арбитраж найден по условиям ({amount_rub:,} ₽)\n\n"

    for offer in profitable_offers:
        msg += (
            f"👤 [Продавец]({offer['seller_url']})     🧑 [Покупатель]({offer['buyer_url']})\n"
            f"🌕 Купить USDT: {offer['price_sell']:.2f} ₽     🌑 Продать USDT: {offer['price_buy']:.2f} ₽\n"
            f"🌗 Спред: 🟢 +{offer['spread']:.2f}% (профит ~{int(offer['profit_rub']):,} ₽)\n\n"
        )

    await bot.send_message(user_id, msg, parse_mode="Markdown")
