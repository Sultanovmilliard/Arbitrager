from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import AVAILABLE_AMOUNTS

router = Router()

# Генерация клавиатуры с суммами
def get_amount_keyboard():
    buttons = [
        [InlineKeyboardButton(text=f"{amount // 1000}k", callback_data=f"amount_{amount}")]
        for amount in AVAILABLE_AMOUNTS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(F.text == "💰Сделки")
async def show_deal_menu(message: Message):
    await message.answer("Выберите сумму для поиска арбитража:", reply_markup=get_amount_keyboard())

@router.callback_query(F.data.startswith("amount_"))
async def handle_amount_choice(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])
    await callback.answer()
    await callback.message.answer(f"Вы выбрали сумму {amount} ₽. Бот начнёт мониторинг и пришлёт уведомление при возможности арбитража.")
from arbitrage import user_amounts  # ✅

@router.callback_query(F.data.startswith("amount_"))
async def handle_amount_choice(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])
    user_amounts[callback.from_user.id] = amount  # ✅
    await callback.answer()
    await callback.message.answer(
        f"Вы выбрали сумму {amount} ₽. Бот начнёт мониторинг и пришлёт уведомление при возможности арбитража."
    )
