import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

from arbitrage import find_arbitrage_opportunities

BOT_TOKEN = "ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН"
CHECK_INTERVAL_MINUTES = 5

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_ids = set()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_ids.add(message.chat.id)
    await message.answer("Привет! Я бот для мониторинга P2P-арбитража.\nКоманда /check — ручная проверка.")

@dp.message(Command("check"))
async def cmd_check(message: Message):
    await send_opportunities_to_user(message.chat.id)

async def send_opportunities_to_user(chat_id: int):
    opportunities = find_arbitrage_opportunities(min_spread=3)
    if not opportunities:
        await bot.send_message(chat_id, "Нет актуальных арбитражных возможностей с доходом выше 3%")
    else:
        for opp in opportunities:
            text = (
                f"Купить на <b>{opp['from']}</b> за <code>{opp['buy_price']}</code>\n"
                f"Продать на <b>{opp['to']}</b> за <code>{opp['sell_price']}</code>\n"
                f"<b>Спред:</b> {opp['spread']}%"
            )
            await bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)

async def scheduled_checker():
    while True:
        if user_ids:
            for user_id in user_ids:
                await send_opportunities_to_user(user_id)
        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)

async def main():
    asyncio.create_task(scheduled_checker())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
