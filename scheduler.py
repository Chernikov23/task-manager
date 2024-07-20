import asyncio
import aiosqlite
from datetime import datetime, timedelta
from aiogram import Bot
from aiocron import crontab
from db import DATABASE

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

REMIND_OPTIONS = {
    "5m": timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "30m": timedelta(minutes=30),
    "1h": timedelta(hours=1),
    "2h": timedelta(hours=2),
    "1d": timedelta(days=1),
    "2d": timedelta(days=2),
    "1w": timedelta(weeks=1),
    "1M": timedelta(days=30)
}

bot = Bot(token=TOKEN)

async def send_reminder(user_id: int, task: str, reminder: str):
    await bot.send_message(user_id, f"Напоминание: {task} (за {reminder} до дедлайна)")

async def check_reminders():
    async with aiosqlite.connect(DATABASE) as db:
        now = datetime.now()
        async with db.execute('SELECT user_id, task, deadline, remind_before FROM tasks WHERE deadline IS NOT NULL') as cursor:
            tasks = await cursor.fetchall()
            for user_id, task, deadline_str, remind_before in tasks:
                deadline = datetime.fromisoformat(deadline_str)
                if remind_before in REMIND_OPTIONS:
                    remind_time = deadline - REMIND_OPTIONS[remind_before]
                    if now >= remind_time and now < deadline:
                        await send_reminder(user_id, task, remind_before)

@crontab('*/1 * * * *')
async def scheduled_reminders():
    await check_reminders()

async def start_scheduler():
    await scheduled_reminders.start()

if __name__ == "__main__":
    asyncio.run(start_scheduler())
