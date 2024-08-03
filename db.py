import sqlite3

conn = sqlite3.connect('db.db') # создает соединение с базой данных. Если файл example.db не существует, он будет создан.

cursor = conn.cursor() # создает объект курсора, который используется для выполнения SQL-запросов.

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        language TEXT NOT NULL
    )
""")
conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        task_name TEXT NOT NULL,
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        deadline TEXT,
        reminder INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")
conn.commit()

def create_user(id, nickname, language):
    cursor.execute('SELECT 1 FROM users WHERE id = ?', (id,))
    user_exists = cursor.fetchone()
    if user_exists:
        return "Welcome back"
    else:
        cursor.execute('INSERT INTO users (id, username, language) VALUES (?,?,?)', (id, nickname, language))
        conn.commit()
        return "You've just registered"


def create_task(user_id, name, description, deadline, reminder):
    cursor.execute('INSERT INTO tasks (user_id, task_name, description, deadline, reminder) VALUES (?,?,?,?,?)', (user_id, name, description, deadline, reminder))
    conn.commit()
    return "Задача успешно создана"

def get_tasks(user_id):
    cursor.execute('SELECT task_name, task_id, description, status, deadline, reminder FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    return tasks