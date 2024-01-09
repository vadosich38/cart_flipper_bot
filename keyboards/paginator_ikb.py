from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup


def get_cards_paginator_ikb(current_page: int, total_pages: int, checked=False) -> InlineKeyboardMarkup:
    #TODO: пагинатор должен листать элементы по кругу как вертушка
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


#TODO: для чего эта функция?
# можно ее заменить на cancel_kb в папке клавиатур?
def get_exit_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back to menu',
                                                                       callback_data='paginator_menu')]])
