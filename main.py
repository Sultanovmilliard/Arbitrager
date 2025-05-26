import asyncio
from aiogram import Dispatcher
from bot import dp

async def main():
    print("Бот запущен!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
