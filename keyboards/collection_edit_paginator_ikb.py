from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_set.texts import bot_texts


def get_collection_edit_menu_ikb() -> InlineKeyboardMarkup:
    #TODO: activate_btn меняется в зависимости от действущего статуса коллекции.
    # Если коллекция сейчас активна текст будет "Деактивировать коллекцию 🟥"
    # Если коллекцтя сейчас не активна, текст будет "Активировать коллекцию 🟩"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=bot_texts['<<'], callback_data='<<'),
                InlineKeyboardButton(text=">>", callback_data=">>"))

    builder.row(
        InlineKeyboardButton(text="Удалить ✖️", callback_data='delete_pair'),
        InlineKeyboardButton(text="Повернуть ➰", callback_data='flipp_cart'),
        InlineKeyboardButton(text="Изменить ⭕️", callback_data="edit_pair")
    )

    collection_mode_text = ""
    builder.row(InlineKeyboardButton(text="Добавить новую карточку 📂", callback_data="add_new_card"),
                InlineKeyboardButton(text=collection_mode_text, callback_data=collection_mode_text))

    builder.row(InlineKeyboardButton(text="Вернуться назад 🔙", callback_data='back_to_collections'))
    return builder.as_markup(resize_keyboard=True)
