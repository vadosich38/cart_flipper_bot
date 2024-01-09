from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup


def cards_paginator_kb(current_page: int, total_pages: int, checked=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not checked:
        builder.row(InlineKeyboardButton(text='Show_value', callback_data='paginator_show_value'))
    else:
        builder.row(InlineKeyboardButton(text='Learned', callback_data='paginator_learned'))
    nav_buttons = [
        InlineKeyboardButton(text='<<' if current_page > 0 else '', callback_data='paginator_back'
                                                                if current_page > 0 else None),
        InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data=None),
        InlineKeyboardButton(text='>>' if current_page < total_pages else '', callback_data='paginator_forward'
                                                                    if current_page < total_pages else None),
    ]
    builder.row(*nav_buttons)
    builder.row(InlineKeyboardButton(text='Back to menu', callback_data='paginator_menu'))
    return builder.as_markup(resize_keyboard=True)


def exit_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back to menu',
                                                                       callback_data='paginator_menu')]])
