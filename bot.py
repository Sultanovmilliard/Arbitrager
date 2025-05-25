
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Хранилище выбранной суммы (по user_id)
user_amounts = {}

# Главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("💰Сделки"))
    return markup

# Меню выбора суммы
def amount_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton("10к–10к"), KeyboardButton("20к–20к")
    )
    markup.row(
        KeyboardButton("30к–30к"), KeyboardButton("50к–50к")
    )
    markup.row(
        KeyboardButton("100к–100к")
    )
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для арбитража. Выбери действие:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: message.text == "💰Сделки")
def show_amount_menu(message):
    bot.send_message(
        message.chat.id,
        "Выбери диапазон суммы, по которой искать арбитраж:",
        reply_markup=amount_menu()
    )

@bot.message_handler(func=lambda message: message.text in ["10к–10к", "20к–20к", "30к–30к", "50к–50к", "100к–100к"])
def set_amount(message):
    user_id = message.from_user.id
    selected = message.text.split("–")[0].replace("к", "000")
    try:
        amount = int(selected)
        user_amounts[user_id] = amount
        bot.send_message(
            message.chat.id,
            f"Вы выбрали сумму: {amount:,} ₽.\nТеперь я ищу арбитраж только по этой сумме.",
            reply_markup=main_menu()
        )
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Не удалось распознать сумму. Пожалуйста, выбери из списка."
        )

# Запуск
print("Bot is running...")
bot.infinity_polling()
