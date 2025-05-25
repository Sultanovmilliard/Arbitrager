import aiohttp

async def find_arbitrage(amount, user_id=None):
    try:
        print(f"[ARBITRAGE] Запрос на сумму: {amount}")
        url = "https://www.bybit.com/fiat/otc/item/online"
        params = {
            "tokenId": "USDT",
            "currencyId": "RUB",
            "payment": "",
            "side": 0,
            "size": str(amount),
            "page": 1,
            "rows": 10
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as resp:
                print(f"[BYBIT STATUS] {resp.status}")
                if resp.status != 200:
                    return "Ошибка при получении цены с ByBit."

                data = await resp.json()
                items = data.get("result", {}).get("items", [])
                if not items:
                    return "Нет доступных объявлений на ByBit."

                price = float(items[0]["price"])
                return (
                    f"Найдена цена на ByBit:\n"
                    f"Продажа USDT за {price:.2f} ₽\n"
                    f"(по сумме {amount:,} ₽)"
                )

    except Exception as e:
        return f"Ошибка при получении арбитража: {e}"
