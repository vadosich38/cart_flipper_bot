from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup
from bot_set.texts import bot_texts
from DBPackage.DBclass import DBMethods


def get_collections_paginator_ikb(collection_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    nav_buttons = [
        InlineKeyboardButton(text='<<', callback_data='previous'),
        InlineKeyboardButton(text='Редактировать', callback_data="collection_edit"),
        InlineKeyboardButton(text='>>', callback_data='next'),
    ]

    builder.row(*nav_buttons)

    if DBMethods.is_collection_active(collection_id=collection_id):
        collection_mode_text = "Деактивировать 🛑"
        collection_mode_callback_data = "deactivate"
    else:
        collection_mode_text = "Активировать ✅"
        collection_mode_callback_data = "activate"

    builder.row(InlineKeyboardButton(text=collection_mode_text, callback_data=collection_mode_callback_data))

    builder.row(InlineKeyboardButton(text='Вернуться в меню ⬅️',
                                     callback_data='collections_paginator_menu'),
                InlineKeyboardButton(text="Добавить коллекцию ➕", callback_data="add_new_collection"))
    builder.row(InlineKeyboardButton(text="Удалить коллекцию ❌", callback_data="del_collection"))
    return builder.as_markup(resize_keyboard=True)
