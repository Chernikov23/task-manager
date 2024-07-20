import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from db import init_db
from handlers import register_handlers
from scheduler import start_scheduler
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_handlers(dp)

    await init_db()
    asyncio.create_task(start_scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
