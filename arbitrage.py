import random

def get_binance_p2p_price(side): return random.uniform(90, 100)
def get_bybit_p2p_price(side): return random.uniform(90, 100)
def get_okx_p2p_price(side): return random.uniform(90, 100)
def get_bitget_p2p_price(side): return random.uniform(90, 100)
def get_kucoin_p2p_price(side): return random.uniform(90, 100)

def find_arbitrage_opportunities(min_spread=3.0):
    exchanges = {
        "Binance": get_binance_p2p_price,
        "Bybit": get_bybit_p2p_price,
        "OKX": get_okx_p2p_price,
        "BitGet": get_bitget_p2p_price,
        "KuCoin": get_kucoin_p2p_price
    }
    prices = {name: {"BUY": f("BUY"), "SELL": f("SELL")} for name, f in exchanges.items()}
    results = []
    for buy_ex, buy_data in prices.items():
        for sell_ex, sell_data in prices.items():
            if buy_ex == sell_ex: continue
            buy_price, sell_price = buy_data["BUY"], sell_data["SELL"]
            spread = ((sell_price - buy_price) / buy_price) * 100
            if spread >= min_spread:
                results.append({
                    "from": buy_ex, "to": sell_ex,
                    "buy_price": round(buy_price, 2),
                    "sell_price": round(sell_price, 2),
                    "spread": round(spread, 2)
                })
    return results
