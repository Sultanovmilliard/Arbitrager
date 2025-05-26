import asyncio
from bot import dp, bot

async def main():
    print("Бот запускается...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
