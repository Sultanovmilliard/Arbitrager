from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

TOKEN = "YOUR_BOT_TOKEN_HERE"  # Вставь сюда токен

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_settings = {}

amount_buttons = [
    InlineKeyboardButton(text="10,000 ₽", callback_data="amount_10000"),
    InlineKeyboardButton(text="30,000 ₽", callback_data="amount_30000"),
    InlineKeyboardButton(text="50,000 ₽", callback_data="amount_50000"),
    InlineKeyboardButton(text="100,000 ₽", callback_data="amount_100000"),
]

spread_buttons = [
    InlineKeyboardButton(text="1%", callback_data="spread_1"),
    InlineKeyboardButton(text="2%", callback_data="spread_2"),
    InlineKeyboardButton(text="3%", callback_data="spread_3"),
    InlineKeyboardButton(text="4%", callback_data="spread_4"),
]

interval_buttons = [
    InlineKeyboardButton(text="10 секунд", callback_data="interval_10"),
    InlineKeyboardButton(text="30 секунд", callback_data="interval_30"),
    InlineKeyboardButton(text="1 минута", callback_data="interval_60"),
]

start_kb = InlineKeyboardMarkup(row_width=2)
start_kb.add(*amount_buttons)

spread_kb = InlineKeyboardMarkup(row_width=4)
spread_kb.add(*spread_buttons)

interval_kb = InlineKeyboardMarkup(row_width=3)
interval_kb.add(*interval_buttons)

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
        reply_markup=start_kb
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
            # Заготовка - замени на реальную проверку
            await bot.send_message(user_id, f"Проверяем арбитраж: сумма {settings['amount_rub']}, порог {settings['spread_threshold']}%")
        except Exception as e:
            await bot.send_message(user_id, f"Ошибка при проверке арбитража: {e}")
        await asyncio.sleep(settings["interval"])

@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    user_id = message.from_user.id
    if user_id in user_settings:
        del user_settings[user_id]
    await message.answer("Авто-проверка арбитража остановлена.")
