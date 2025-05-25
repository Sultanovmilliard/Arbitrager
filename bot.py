import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from arbitrage import find_arbitrage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_amounts = {}

# Главное меню
main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="💰Сделки")]
    ]
)

# Меню выбора суммы
amount_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="10к–10к"), KeyboardButton(text="20к–20к")],
        [KeyboardButton(text="30к–30к"), KeyboardButton(text="50к–50к")],
        [KeyboardButton(text="100к–100к")]
    ]
)

@dp.message()
async def handle_message(message: types.Message):
    if message.text == "/start":
        await message.answer(
            "Привет! Я бот для арбитража. Выбери действие:",
            reply_markup=main_menu
        )
    elif message.text == "💰Сделки":
        await message.answer(
            "Выбери диапазон суммы, по которой искать арбитраж:",
            reply_markup=amount_menu
        )
    elif message.text in ["10к–10к", "20к–20к", "30к–30к", "50к–50к", "100к–100к"]:
        amount_text = message.text.split("–")[0].replace("к", "000")
        try:
            amount = int(amount_text)
            user_id = message.from_user.id
            user_amounts[user_id] = amount
            await message.answer(
                f"Вы выбрали сумму: {amount:,} ₽.\nТеперь я ищу арбитраж по этой сумме...",
                reply_markup=main_menu
            )
        except ValueError:
            await message.answer("Ошибка при распознавании суммы. Попробуйте ещё раз.")
    else:
        await message.answer("Пожалуйста, выбери действие из меню.")

# Фоновая задача: проверка арбитража каждую минуту
async def check_arbitrage_loop():
    while True:
        for user_id, amount in user_amounts.items():
            result = find_arbitrage(amount)
            if "Спред" in result and "%" in result:
                try:
                    spread_value = float(result.split("Спред: ")[1].split("%")[0])
                    if spread_value >= 3:
                        await bot.send_message(chat_id=user_id, text=result)
                except Exception:
                    pass
        await asyncio.sleep(60)

async def run_bot():
    asyncio.create_task(check_arbitrage_loop())
    await dp.start_polling(bot)
