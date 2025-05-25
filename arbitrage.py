import requests

def get_bybit_price(amount: int, trade_type: str):
    url = "https://api2.bybit.com/fiat/otc/item/online"
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

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, f"[BYBIT STATUS] {response.status_code}"

        data = response.json().get("result", {}).get("items", [])
        if not data:
            return None, "[BYBIT] Нет объявлений"
        return float(data[0]["price"]), None
    except Exception as e:
        return None, f"[BYBIT ERROR] {e}"

def find_arbitrage(amount):
    buy_price, buy_error = get_bybit_price(amount, "BUY")
    sell_price, sell_error = get_bybit_price(amount, "SELL")

    if buy_error or sell_error:
        return "Недостаточно данных с биржи для расчёта арбитража."

    spread = (sell_price - buy_price) / buy_price * 100
    if spread >= 3:
        return (
            f"🔍 Арбитраж найден!\n"
            f"Купить по: {buy_price:.2f} ₽\n"
            f"Продать по: {sell_price:.2f} ₽\n"
            f"📊 Профит: {spread:.2f}%"
        )
    return f"Спред: {spread:.2f}% — ниже 3%, арбитраж невыгоден."
