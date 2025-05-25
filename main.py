import asyncio
from bot import dp, bot
from keep_alive import keep_alive

async def run_bot():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())
