import asyncio
from bot import run_bot
from keep_alive import keep_alive

keep_alive()

if __name__ == "__main__":
    asyncio.run(run_bot())
