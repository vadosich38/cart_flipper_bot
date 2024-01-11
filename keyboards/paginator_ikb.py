from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup
from bot_set.texts import bot_texts


def get_cards_paginator_ikb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=bot_texts['paginator_show_value'], callback_data='paginator_show_value'))
    nav_buttons = [
        InlineKeyboardButton(text=bot_texts['paginator_learned'], callback_data='paginator_learned'),
        InlineKeyboardButton(text=bot_texts['paginator_not_learned'], callback_data='paginator_not_learned'),
    ]
    builder.row(*nav_buttons)
    builder.row(InlineKeyboardButton(text=bot_texts['paginator_menu'], callback_data='paginator_menu'))
    return builder.as_markup(resize_keyboard=True)


def get_exit_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=bot_texts['paginator_menu'],
                                                                       callback_data='paginator_menu')]])
