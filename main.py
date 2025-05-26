import asyncio
from aiogram import Bot, Dispatcher
from bot import router
from config import BOT_TOKEN

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    dp.include_router(router)
    await dp.start_polling()  # без параметров

if __name__ == "__main__":
    asyncio.run(main())
