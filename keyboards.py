from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Мои задачи"),
            KeyboardButton(text="🆕 Создать задачу")
        ],
        [
            KeyboardButton(text="💼 Мои организации"),
            KeyboardButton(text="🆕 Создать организацию")
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
            KeyboardButton(text="ℹ️ О боте")
        ]
    ]
)

time = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Месяц"),
            KeyboardButton(text="Неделя")
        ],
        [
            KeyboardButton(text="2 дня"),
            KeyboardButton(text="1 день")
        ],
        [
            KeyboardButton(text="2 часа"),
            KeyboardButton(text="1 час")
        ],
        [
            KeyboardButton(text="30 минут"),
            KeyboardButton(text="15 минут")
        ],
        [
            KeyboardButton(text="10 минут"),
            KeyboardButton(text="В момент события")
        ]
    ]
)