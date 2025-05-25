from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from arbitrage import user_amounts

router = Router()

# Клавиатура выбора суммы
def get_amount_keyboard():
    buttons = [
        [InlineKeyboardButton(text="10 000 ₽", callback_data="amount_10000")],
        [InlineKeyboardButton(text="20 000 ₽", callback_data="amount_20000")],
        [InlineKeyboardButton(text="50 000 ₽", callback_data="amount_50000")],
        [InlineKeyboardButton(text="100 000 ₽", callback_data="amount_100000")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(F.text == "💰Сделки")
async def show_amount_menu(message: Message):
    await message.answer("Выберите сумму для арбитража:", reply_markup=get_amount_keyboard())

@router.callback_query(F.data.startswith("amount_"))
async def handle_amount_selection(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    user_amounts[user_id] = amount
    await callback.answer(f"Вы выбрали {amount:,} ₽", show_alert=True)
    await callback.message.answer(f"✅ Буду искать арбитраж по сумме {amount:,} ₽.")
