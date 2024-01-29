from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb() -> ReplyKeyboardMarkup:
    main_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Учиться 🧑‍🏫"),
             KeyboardButton(text="Коллекции 📜")]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )

    return main_kb
