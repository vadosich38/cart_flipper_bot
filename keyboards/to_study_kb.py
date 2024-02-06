from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_to_study_notification_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Учиться 🧑‍🏫"), KeyboardButton(text="Напомини позже 🤖")]
        ], resize_keyboard=True, one_time_keyboard=True
    )

    return kb
