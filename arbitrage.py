import requests

def get_bybit_p2p_price(amount, trade_type):
    url = "https://api.bybit.com/fiat/otc/item/online"
    params = {
        "userId": "",
        "tokenId": "USDT",
        "currencyId": "RUB",
        "payment": "",
        "side": 1 if trade_type == "SELL" else 0,
        "size": str(amount),
        "page": 1,
        "rows": 10
    }
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.bybit.com"
    }

    print(f"[BYBIT] Запрос на сумму: {amount}")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"[BYBIT STATUS] {response.status_code}")
        print(f"[BYBIT RESPONSE]: {response.text}")

        data = response.json()
        items = data.get("result", {}).get("items", [])
        if not items:
            print("[BYBIT] Пусто, нет объявлений.")
            return None
        return float(items[0]["price"])

    except Exception as e:
        print(f"[BYBIT ERROR] {e}")
        return None


def find_arbitrage(amount):
    try:
        buy_price = get_bybit_p2p_price(amount, "BUY")
        sell_price = get_bybit_p2p_price(amount, "SELL")

        if buy_price is None or sell_price is None:
            return "Недостаточно данных с биржи для расчёта арбитража."

        spread = (sell_price - buy_price) / buy_price * 100

        if spread >= 3:
            return (
                f"Найдена арбитражная возможность:\n\n"
                f"Купить USDT на ByBit за {buy_price:.2f} ₽\n"
                f"Продать USDT на ByBit за {sell_price:.2f} ₽\n"
                f"Спред: {spread:.2f}%"
            )
        else:
            return f"Спред: {spread:.2f}%. Сделка невыгодна."
    except Exception as e:
        return f"Ошибка при получении арбитража: {e}"
