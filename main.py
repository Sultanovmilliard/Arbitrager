import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.menu import register_menu_handlers
from arbitrage import start_arbitrage_monitoring
from keep_alive import keep_alive


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация хендлеров
    register_menu_handlers(dp)

    # Запускаем keep-alive сервер
    keep_alive()

    # Запуск фоновой задачи (мониторинг арбитража)
    asyncio.create_task(start_arbitrage_monitoring(bot))

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
