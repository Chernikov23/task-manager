import asyncio
from aiogram import Bot, Dispatcher
import logging
import handlers
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode="MarkDown"))
dp = Dispatcher() 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Бот запущен и работает...")

async def main():  
    
    dp.include_routers(
        handlers.rt
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())