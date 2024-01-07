from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb() -> ReplyKeyboardMarkup:
    main_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Учиться 🧑‍🏫"),
             KeyboardButton(text="Коллекции 📜")]
        ]
    )

    return main_kb
