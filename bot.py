import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from arbitrage import find_arbitrage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_amounts = {}

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="💰 Сделки")]]
)

amount_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("10к–10к"), KeyboardButton("20к–20к")],
        [KeyboardButton("30к–30к"), KeyboardButton("50к–50к")],
        [KeyboardButton("100к–100к")]
    ]
)

@dp.message()
async def handle_message(message: types.Message):
    if message.text == "💰 Сделки":
        await message.answer("Выбери диапазон суммы, по которой искать арбитраж:", reply_markup=amount_menu)
    elif message.text in ["10к–10к", "20к–20к", "30к–30к", "50к–50к", "100к–100к"]:
        amount = int(message.text.split("к")[0]) * 1000
        user_amounts[message.from_user.id] = amount
        await message.answer(f"Вы выбрали сумму: {amount:,} ₽. Теперь я ищу арбитраж по этой сумме...")

        result = find_arbitrage(amount)
        await message.answer(result, reply_markup=main_menu)
    else:
        await message.answer("Нажми кнопку ниже для начала.", reply_markup=main_menu)
