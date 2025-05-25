from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Временное хранилище выбора пользователя (замени на базу или Redis по необходимости)
user_settings = {}

# Кнопки выбора порога спреда
spread_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1%", callback_data="spread_1"),
        InlineKeyboardButton(text="2%", callback_data="spread_2"),
        InlineKeyboardButton(text="3%", callback_data="spread_3"),
        InlineKeyboardButton(text="4%", callback_data="spread_4"),
    ]
])

# Кнопки выбора интервала проверки
interval_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="10 секунд", callback_data="interval_10"),
        InlineKeyboardButton(text="30 секунд", callback_data="interval_30"),
        InlineKeyboardButton(text="1 минута", callback_data="interval_60"),
    ]
])

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_settings[message.from_user.id] = {
        "spread": 3,      # значение по умолчанию
        "interval": 60,   # 60 секунд по умолчанию
    }
    text = (
        "Добро пожаловать!\n\n"
        "Выберите порог спреда для уведомлений:"
    )
    await message.answer(text, reply_markup=spread_keyboard)

@router.callback_query(F.data.startswith("spread_"))
async def choose_spread(callback: CallbackQuery):
    user_id = callback.from_user.id
    spread_value = int(callback.data.split("_")[1])
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]["spread"] = spread_value

    await callback.answer(f"Порог спреда установлен: {spread_value}%")
    await callback.message.edit_text(
        f"Порог спреда установлен на {spread_value}%.\n\n"
        "Теперь выберите интервал проверки арбитража:",
        reply_markup=interval_keyboard
    )

@router.callback_query(F.data.startswith("interval_"))
async def choose_interval(callback: CallbackQuery):
    user_id = callback.from_user.id
    interval_value = int(callback.data.split("_")[1])
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id]["interval"] = interval_value

    await callback.answer(f"Интервал проверки установлен: {interval_value} секунд")
    await callback.message.edit_text(
        f"Интервал проверки установлен на {interval_value} секунд.\n\n"
        "Настройки сохранены. Вы будете получать уведомления по выбранным параметрам."
    )

# Функция для получения настроек пользователя (можно использовать в arbitrage.py)
def get_user_settings(user_id: int):
    return user_settings.get(user_id, {"spread": 3, "interval": 60})
