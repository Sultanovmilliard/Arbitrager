from keep_alive import keep_alive
import asyncio
from bot import run_bot

keep_alive()

if __name__ == "__main__":
    asyncio.run(run_bot())
