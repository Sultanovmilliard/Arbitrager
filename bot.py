from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
import asyncio
from config import BOT_TOKEN, ADMIN_USER_ID, DEFAULT_AMOUNT_RUB, DEFAULT_SPREAD_THRESHOLD, DEFAULT_CHECK_INTERVAL
from menu import amount_menu, spread_menu, interval_menu
from arbitrage import check_arbitrage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранение настроек пользователя (можно потом заменить на БД)
user_settings = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_settings[message.from_user.id] = {
        "amount_rub": DEFAULT_AMOUNT_RUB,
        "spread_threshold": DEFAULT_SPREAD_THRESHOLD,
        "interval": DEFAULT_CHECK_INTERVAL
    }
    await message.answer(
        "Привет! Выберите сумму для арбитража:",
        reply_markup=amount_menu()
    )

@dp.callback_query(Text(startswith="amount_"))
async def amount_chosen(call: CallbackQuery):
    amount = int(call.data.split("_")[1])
    user_id = call.from_user.id
    user_settings.setdefault(user_id, {})["amount_rub"] = amount
    await call.message.answer(f"Сумма выбрана: {amount} ₽\nТеперь выберите порог спреда:", reply_markup=spread_menu())
    await call.answer()

@dp.callback_query(Text(startswith="spread_"))
async def spread_chosen(call: CallbackQuery):
    spread = int(call.data.split("_")[1])
    user_id = call.from_user.id
    user_settings.setdefault(user_id, {})["spread_threshold"] = spread
    await call.message.answer(f"Порог спреда выбран: {spread}%\nТеперь выберите интервал проверки:", reply_markup=interval_menu())
    await call.answer()

@dp.callback_query(Text(startswith="interval_"))
async def interval_chosen(call: CallbackQuery):
    interval = int(call.data.split("_")[1])
    user_id = call.from_user.id
    user_settings.setdefault(user_id, {})["interval"] = interval
    await call.message.answer(f"Интервал проверки установлен: {interval} секунд\nАрбитраж начнёт проверяться автоматически.")
    await call.answer()

async def arbitrage_loop():
    while True:
        for user_id, settings in user_settings.items():
            try:
                await check_arbitrage(bot, user_id,
                                      settings.get("amount_rub", DEFAULT_AMOUNT_RUB),
                                      settings.get("spread_threshold", DEFAULT_SPREAD_THRESHOLD))
            except Exception as e:
                print(f"Error in arbitrage check for user {user_id}: {e}")
        # Берём максимальный интервал из всех пользователей, чтобы не перегружать цикл
        max_interval = max(settings.get("interval", DEFAULT_CHECK_INTERVAL) for settings in user_settings.values())
        await asyncio.sleep(max_interval)

if __name__ == "__main__":
    import asyncio
    async def main():
        await dp.start_polling()

    asyncio.create_task(arbitrage_loop())
    asyncio.run(main())
