from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_button_create_first_collection() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать первую коллекцию 🧑‍🎨", callback_data="add_new_collection")]
        ]
    )

    return ikb
