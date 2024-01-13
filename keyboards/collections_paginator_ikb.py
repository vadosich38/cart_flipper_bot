from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup
from bot_set.texts import bot_texts


def get_collections_paginator_ikb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    nav_buttons = [
        InlineKeyboardButton(text='<<', callback_data='previous'),
        InlineKeyboardButton(text='Редактировать', callback_data="collection_edit"),
        InlineKeyboardButton(text='>>', callback_data='next'),
    ]

    builder.row(*nav_buttons)
    builder.row(InlineKeyboardButton(text=bot_texts['Вернуться в главное меню ⬅️'],
                                     callback_data='collections_paginator_menu'),
                InlineKeyboardButton(text="Добавить новую коллекцию ➕", callback_data="add_new_collection"))
    return builder.as_markup(resize_keyboard=True)