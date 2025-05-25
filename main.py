from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
from config import BOT_TOKEN
from keep_alive import keep_alive
from handlers import menu

from arbitrage import start_arbitrage_monitoring

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(menu.router)

    # Запуск автоарбитража
    asyncio.create_task(start_arbitrage_monitoring(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
