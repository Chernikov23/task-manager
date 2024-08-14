from aiogram import F, Bot, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from models import User
from keyboards import *
from bot import bot
import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD_BROADCAST = os.getenv('PASSWORD')

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
    
class Form(StatesGroup):
    message = State()
    password = State()
    
    
DATABASE_NAME = "users"
USER = "chernikov"
PASSWORD = "sasha289"
HOST = "localhost"
PORT = "5432"

async def clear_table():
    conn = None
    try:
        conn = await asyncpg.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE_NAME)
        await conn.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
    finally:
        if conn:
            await conn.close()

@rt.message(Command('cleardb'))
async def clear_db(msg: Message):
    await clear_table()
    await msg.answer(f"Все данные из таблицы 'users' были успешно удалены.")


@rt.message(CommandStart())
async def start(msg: Message):
    tg_id = msg.from_user.id
    name = msg.from_user.full_name
    user = await User.get_or_none(tg_id=tg_id)
    if not user:
        user = await User.create(tg_id=tg_id, name=name)
        await msg.answer(f"Привет, {name}! Ты успешно зарегистрирован.")
    else:
        await msg.answer(f"Привет снова, {name}!")
        
    
@rt.message(Command('broadcast'))
async def start_broadcast(msg: Message, state: FSMContext):
    await msg.answer('Введите пароль')
    await state.set_state(Form.password)
    
@rt.message(Form.password)
async def check_password(msg: Message, state: FSMContext):
    if msg.text == PASSWORD_BROADCAST:
        await msg.answer("СОобщение введите")
        await state.set_state(Form.message)
    else:
        await msg.answer('Password is incorrect')
        return
    
async def send_notifications_to_all_users(message_text: str):
    users = await User.all()
    if not users:
        print("В базе данных нет пользователей.")
        return
    for user in users:
        try:
            await bot.send_message(chat_id=user.tg_id, text=message_text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user.tg_id}: {e}")
    

@rt.message(Form.message)
async def start_mailing(msg: Message, state: FSMContext):
    await state.clear()
    await send_notifications_to_all_users(msg.text)
    await msg.answer('Рассылка окончена')