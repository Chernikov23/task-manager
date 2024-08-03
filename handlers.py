from aiogram import F, Bot, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db import *
from keyboards import *


rt = Router()

times = {
    "Месяц": 43200,
    "Неделя": 10080,
    "2 дня": 2880,
    "1 день": 1440,
    "2 часа": 120,
    "1 час": 60,
    "30 минут": 30,
    "15 минут": 15,
    "10 минут": 10,
    "В момент события": 0
}


class Task(StatesGroup):
    name = State()
    description = State()
    deadline = State()
    reminder = State()


@rt.message(CommandStart())
async def start(msg: Message):
    await msg.answer(create_user(msg.from_user.id, msg.from_user.username, msg.from_user.language_code), reply_markup=main)
    
@rt.message(F.text == '🆕 Создать задачу')
async def start_creating_task(msg: Message, state: FSMContext):
    await msg.answer("Введите название задачи:")
    await state.set_state(Task.name)
    
@rt.message(Task.name)
async def set_name(msg: Message, state: FSMContext):
    name = msg.text
    await state.update_data(name=name)
    await msg.answer("Введите описание задачи:")
    await state.set_state(Task.description)
    
@rt.message(Task.description)
async def process_task_description(msg: Message, state: FSMContext):
    description = msg.text
    await state.update_data(description=description)
    await msg.answer("Введите дедлайн в формате ДД.ММ.ГГ ЧЧ:ММ:")
    await state.set_state(Task.deadline)

@rt.message(Task.deadline)
async def process_task_deadline(msg: Message, state: FSMContext):
    deadline = msg.text
    await state.update_data(deadline=deadline)
    await msg.answer("Введите время напоминания в минутах до дедлайна:")
    await state.set_state(Task.reminder)

@rt.message(Task.reminder)
async def process_task_reminder(msg: Message, state: FSMContext):
    reminder = int(msg.text)
    user_data = await state.get_data()
    description = user_data['description']
    deadline = user_data['deadline']
    name = user_data['name']
    response = create_task(msg.from_user.id, name, description, deadline, reminder)
    await msg.answer(response)
    await state.clear()
    
@rt.message(F.text == '📋 Мои задачи')
async def view_tasks_handler(msg: Message):
    tasks = get_tasks(msg.from_user.id)
    if not tasks:
        await msg.answer("У вас нет задач.")
    else:
        tasks_list = "\n".join([f"Task name: {task[0]}\nDescription: {task[2]}\nStatus: {task[3]}\nDeadline: {task[4]}\nReminder: {task[5]} minutes before\n\n" for task in tasks])
        await msg.answer(f"Ваши задачи:\n{tasks_list}")