from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AMOUNT_OPTIONS, SPREAD_OPTIONS, INTERVAL_OPTIONS

def amount_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=f"{amount // 1000}к ₽", callback_data=f"amount_{amount}") for amount in AMOUNT_OPTIONS]
    kb.add(*buttons)
    return kb

def spread_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=f"{spread}%", callback_data=f"spread_{spread}") for spread in SPREAD_OPTIONS]
    kb.add(*buttons)
    return kb

def interval_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=f"{interval} сек", callback_data=f"interval_{interval}") for interval in INTERVAL_OPTIONS]
    kb.add(*buttons)
    return kb
