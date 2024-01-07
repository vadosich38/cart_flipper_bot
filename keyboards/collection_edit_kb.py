from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_collection_edit_menu_kb() -> ReplyKeyboardMarkup:
    #TODO: activate_btn меняется в зависимости от действущего статуса коллекции.
    # Если коллекция сейчас активна текст будет "Деактивировать коллекцию 🟥"
    # Если коллекцтя сейчас не активна, текст будет "Активировать коллекцию 🟩"
    activate_btn = ""

    coll_edit_menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить новую карточку 📂")],
            [KeyboardButton(text=activate_btn)]
        ]
    )

    return coll_edit_menu_kb
