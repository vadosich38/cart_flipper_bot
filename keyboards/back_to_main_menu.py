from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_return_in_main_menu_kb() -> ReplyKeyboardMarkup:
    return_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в главное меню 🟥")]
        ], resize_keyboard=True
    )

    return return_kb
