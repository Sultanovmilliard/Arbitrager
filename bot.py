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
        [KeyboardButton("10k–10k"), KeyboardButton("20k–20k")],
        [KeyboardButton("30k–30k"), KeyboardButton("50k–50k")],
        [KeyboardButton("100k–100k")]
    ]
)

@dp.message()
async def handle_message(message: types.Message):
    if message.text == "💰 Сделки":
        await message.answer("Выбери диапазон суммы, по которой искать арбитраж:", reply_markup=amount_menu)
    elif "k–" in message.text:
        try:
            raw = message.text.split("–")[0].replace("k", "000")
            amount = int(raw)
            await message.answer(f"Вы выбрали сумму: {amount:,} ₽.\nТеперь я ищу арбитраж по этой сумме...")
            result = await find_arbitrage(amount, message.from_user.id)
            await message.answer(result)
        except Exception as e:
            await message.answer(f"Ошибка при распознавании суммы: {e}")
    else:
        await message.answer("Нажми кнопку 👇", reply_markup=main_menu)

async def run_bot():
    await dp.start_polling(bot)
