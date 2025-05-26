from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import aiohttp

TOKEN = "7623579455:AAHl_qRDh3Qcz9YRBhPRR7aXasIheVVYtzw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_settings = {}

# Кнопки выбора суммы
amount_buttons = [
    InlineKeyboardButton(text="10,000 ₽", callback_data="amount_10000"),
    InlineKeyboardButton(text="30,000 ₽", callback_data="amount_30000"),
    InlineKeyboardButton(text="50,000 ₽", callback_data="amount_50000"),
    InlineKeyboardButton(text="100,000 ₽", callback_data="amount_100000"),
]
amount_kb = InlineKeyboardMarkup(row_width=2)
amount_kb.add(*amount_buttons)

# Кнопки выбора порога спреда
spread_buttons = [
    InlineKeyboardButton(text="1%", callback_data="spread_1"),
    InlineKeyboardButton(text="2%", callback_data="spread_2"),
    InlineKeyboardButton(text="3%", callback_data="spread_3"),
    InlineKeyboardButton(text="4%", callback_data="spread_4"),
]
spread_kb = InlineKeyboardMarkup(row_width=4)
spread_kb.add(*spread_buttons)

# Кнопки выбора интервала проверки
interval_buttons = [
    InlineKeyboardButton(text="10 секунд", callback_data="interval_10"),
    InlineKeyboardButton(text="30 секунд", callback_data="interval_30"),
    InlineKeyboardButton(text="1 минута", callback_data="interval_60"),
]
interval_kb = InlineKeyboardMarkup(row_width=3)
interval_kb.add(*interval_buttons)

BYBIT_P2P_API = "https://api.bybit.com/spot/v1/p2p/order-list"

async def fetch_bybit_p2p_orders(side: str, amount_rub: int, pay_types="Tinkoff", page=1, rows=50):
    params = {
        "side": side,
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
    sellers = await fetch_bybit_p2p_orders(side="sell", amount_rub=amount_rub)
    buyers = await fetch_bybit_p2p_orders(side="buy", amount_rub=amount_rub)

    if not sellers or not buyers:
        await bot.send_message(user_id, "Объявления с ByBit P2P не найдены.")
        return

    profitable_offers = []

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

            if b_price <= s_price:
                continue

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

    msg = f"📊 Арбитраж найден по условиям ({amount_rub:,} ₽)\n\n"

    for offer in profitable_offers:
        msg += (
            f"👤 [Продавец]({offer['seller_url']})     🧑 [Покупатель]({offer['buyer_url']})\n"
            f"🌕 Купить USDT: {offer['price_sell']:.2f} ₽     🌑 Продать USDT: {offer['price_buy']:.2f} ₽\n"
            f"🌗 Спред: 🟢 +{offer['spread']:.2f}% (профит ~{int(offer['profit_rub']):,} ₽)\n\n"
        )

    await bot.send_message(user_id, msg, parse_mode="Markdown")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_settings[user_id] = {
        "amount_rub": 10000,
        "spread_threshold": 3,
        "interval": 60,
    }
    await message.answer(
        "Привет! Выберите сумму для арбитража:",
        reply_markup=amount_kb
    )

@dp.callback_query(F.data.startswith("amount_"))
async def amount_chosen(call: CallbackQuery):
    user_id = call.from_user.id
    amount = int(call.data.split("_")[1])
    user_settings.setdefault(user_id, {})["amount_rub"] = amount
    await call.message.answer(
        f"Вы выбрали сумму: {amount:,} ₽\nТеперь выберите порог спреда для уведомлений:",
        reply_markup=spread_kb
    )
    await call.answer()

@dp.callback_query(F.data.startswith("spread_"))
async def spread_chosen(call: CallbackQuery):
    user_id = call.from_user.id
    spread = int(call.data.split("_")[1])
    user_settings.setdefault(user_id, {})["spread_threshold"] = spread
    await call.message.answer(
        f"Порог спреда установлен: {spread}%\nВыберите интервал проверки арбитража:",
        reply_markup=interval_kb
    )
    await call.answer()

@dp.callback_query(F.data.startswith("interval_"))
async def interval_chosen(call: CallbackQuery):
    user_id = call.from_user.id
    interval = int(call.data.split("_")[1])
    user_settings.setdefault(user_id, {})["interval"] = interval
    await call.message.answer(
        f"Интервал проверки установлен: {interval} секунд.\nТеперь бот будет автоматически проверять арбитраж."
    )
    await call.answer()
    asyncio.create_task(arbitrage_loop(user_id))

async def arbitrage_loop(user_id: int):
    while True:
        settings = user_settings.get(user_id)
        if not settings:
            break
        try:
            await check_arbitrage(
                bot,
                user_id,
                amount_rub=settings["amount_rub"],
                spread_threshold_percent=settings["spread_threshold"]
            )
        except Exception as e:
            await bot.send_message(user_id, f"Ошибка при проверке арбитража: {e}")
        await asyncio.sleep(settings["interval"])

@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    user_id = message.from_user.id
    if user_id in user_settings:
        del user_settings[user_id]
    await message.answer("Авто-проверка арбитража остановлена.")
