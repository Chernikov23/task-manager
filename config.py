from dotenv import load_dotenv
import os

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
DATABASE_NAME = os.getenv("DATABASE_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv("LOCALHOST")
PORT = os.getenv('PORT')
PASSWORD_BROADCAST = os.getenv('PASSWORD_BROADCAST')


TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
