import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.menu import router
from arbitrage import start_arbitrage_monitoring
from keep_alive import keep_alive

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    keep_alive()
    asyncio.create_task(start_arbitrage_monitoring(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
