from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_cancel_kb() -> ReplyKeyboardMarkup:
    cancel_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отменить 🔴")]
        ]
    )

    return cancel_kb
