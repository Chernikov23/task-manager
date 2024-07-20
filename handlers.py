from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from db import add_task, delete_task, list_tasks
from datetime import datetime, timedelta

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

async def start_handler(message: Message):
    await message.answer("Привет! Я менеджер задач. Используй команды /add, /delete и /list для управления задачами. Добавляй дедлайны в формате ДД-ММ ЧЧ:ММ и напоминания в виде: 5m, 15m, 30m, 1h, 2h, 1d, 2d, 1w, 1M.")

async def add_handler(message: Message):
    parts = message.text[len("/add "):].split(" ", 2)
    if len(parts) >= 2:
        task = parts[0]
        deadline_str = parts[1]
        remind_before = parts[2] if len(parts) == 3 else None

        try:
            deadline = datetime.strptime(deadline_str, "%d-%m %H:%M")
            await add_task(message.from_user.id, task, deadline, remind_before)
            await message.answer(f"Задача '{task}' добавлена с дедлайном {deadline_str}.")
        except ValueError:
            await message.answer("Неверный формат даты. Используй ДД-ММ ЧЧ:ММ.")
    else:
        await message.answer("Пожалуйста, укажи задачу и дедлайн в формате /add задача ДД-ММ ЧЧ:ММ напоминание (опционально).")

async def delete_handler(message: Message):
    try:
        task_id = int(message.text[len("/delete "):])
        await delete_task(task_id)
        await message.answer(f"Задача с ID {task_id} удалена.")
    except ValueError:
        await message.answer("Пожалуйста, укажи корректный ID задачи после команды /delete.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

async def list_handler(message: Message):
    tasks = await list_tasks(message.from_user.id)
    if tasks:
        tasks_list = "\n".join([f"{task_id}: {task} (Дедлайн: {deadline}, Напоминание: {remind_before})" for task_id, task, deadline, remind_before in tasks])
        await message.answer(f"Твои задачи:\n{tasks_list}")
    else:
        await message.answer("У тебя нет задач.")

def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command('start'))
    dp.message.register(add_handler, Command('add'))
    dp.message.register(delete_handler, Command('delete'))
    dp.message.register(list_handler, Command('list'))
