# bot.py
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from arbitrage import check_arbitrage
from spread_threshold import SpreadThresholdManager

BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

spread_manager = SpreadThresholdManager()

# Кнопки порога спреда
def get_spread_keyboard(user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for val in [1, 2, 3, 4]:
        text = f"{val}%"
        # Выделяем выбранный порог жирным (если выбрано)
        if spread_manager.get_threshold(user_id) == val:
            text = f"✅ {text}"
        keyboard.insert(InlineKeyboardButton(text=text, callback_data=f"spread_{val}"))
    return keyboard

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if spread_manager.get_threshold(user_id) is None:
        spread_manager.set_threshold(user_id, 3)  # По умолчанию 3%
    await message.answer(
        "Привет! Выбери порог спреда для уведомлений:",
        reply_markup=get_spread_keyboard(user_id)
    )

@dp.callback_query(lambda c: c.data and c.data.startswith("spread_"))
async def spread_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    value = int(callback.data.split("_")[1])
    spread_manager.set_threshold(user_id, value)
    await callback.message.edit_text(
        f"Выбран порог спреда: {value}%",
        reply_markup=get_spread_keyboard(user_id)
    )
    await callback.answer(f"Порог спреда изменён на {value}%")

# Здесь добавлять запуск проверки арбитража с выбранным порогом
# и отправку сообщений пользователю

if __name__ == "__main__":
    import asyncio
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
