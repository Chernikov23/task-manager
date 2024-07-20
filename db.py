import aiosqlite
from datetime import datetime, timedelta

DATABASE = "tasks.db"

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                deadline TEXT,
                remind_before TEXT
            )
        ''')
        await db.commit()

async def add_task(user_id: int, task: str, deadline: datetime = None, remind_before: str = None):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('INSERT INTO tasks (user_id, task, deadline, remind_before) VALUES (?, ?, ?, ?)', 
            (user_id, task, deadline.isoformat() if deadline else None, remind_before))
        await db.commit()

async def delete_task(task_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        await db.commit()

async def list_tasks(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT id, task, deadline, remind_before FROM tasks WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchall()
