from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_yes_no_ikb() -> InlineKeyboardMarkup:
    yn_ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да 🟩", callback_data="yes")],
            [InlineKeyboardButton(text="Нет 🟥", callback_data="no")]
        ]
    )

    return yn_ikb
